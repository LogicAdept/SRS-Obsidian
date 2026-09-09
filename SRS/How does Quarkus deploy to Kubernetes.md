<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus deploy to Kubernetes?

> [!abstract] Short answer
> Three cooperating extensions: **`quarkus-kubernetes`** generates K8s manifests (Deployment, Service, probes wiring, RBAC) **at build time** into `target/kubernetes/`; **container-image extensions** (`quarkus-container-image-docker`, `-jib`, `-s2i`, `-buildpack`) build the image and optionally push it; and `quarkus-kubernetes-client`/config extensions handle in-cluster API access and ConfigMap/Secret binding. The command-line story: `quarkus deploy` (or `mvn quarkus:k8s:deploy` style goals) chains build-image, push and `kubectl apply` of the generated manifest.

## Manifest generation is a build step

With `quarkus-kubernetes` on the classpath, packaging emits `target/kubernetes/kubernetes.yml` (plus `openshift.yml` for the OpenShift flavor): a ServiceAccount, a Deployment with the container reference and **probes automatically wired to the health endpoints** when smallrye-health is present, and a Service with the exposed port — all annotated (`app.quarkus.io/quarkus-version`, `managed-by: quarkus`) so subsequent builds reconcile the same resources. Everything is configurable through `quarkus.kubernetes.*` — replicas, resources requests/limits, env vars, init containers, node selectors — and externalized configuration binds ConfigMaps/Secrets via `quarkus.kubernetes.config-map-volumes`/`secret-volumes` or env sources ([[What is the difference between build-time and runtime configuration in Quarkus]] is the reason app config is env-var friendly here). The image reference inside the Deployment comes from the container-image extension's group/artifact/tag settings.

```java
// Verified output of `mvn package -DskipTests` with quarkus-kubernetes + smallrye-health
// (Quarkus 3.39.2; abridged verbatim from target/kubernetes/kubernetes.yml):
//
// apiVersion: v1
// kind: ServiceAccount
// metadata:
//   annotations:
//     app.quarkus.io/quarkus-version: 3.39.2
//     app.quarkus.io/build-timestamp: 2026-09-09 - 23:15:17 +0000
//   labels:
//     app.kubernetes.io/name: quarkus-check
//     app.kubernetes.io/managed-by: quarkus
// ---
// kind: Deployment ... containers: ...
//   livenessProbe:
//     httpGet: { path: /q/health/live ... }
//   readinessProbe:
//     httpGet: { path: /q/health/ready ... }
//   startupProbe:
//     httpGet: { path: /q/health/started ... }
// The probe wiring appeared WITHOUT any k8s YAML written by hand - the health extension
// and kubernetes extension cooperate during augmentation ([[What is a Quarkus extension]]).
```

**Listing 1.** Generated, not authored: the Deployment's three probes point at `/q/health/live|ready|started` purely because both extensions were present — the build-time composition Quarkus is known for ([[What health checks does Quarkus expose]]).

```d2
direction: right
build: "mvn package\naugmentation" {
  width: 200
  height: 50
}
man: "quarkus-kubernetes\ntarget/kubernetes/*.yml" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
img: "container-image ext\ndocker | jib | s2i | buildpack" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
push: "push to registry" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
apply: "kubectl apply\n(quarkus deploy / k8s:deploy)" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
build -> man
build -> img -> push -> apply
man -> apply
```

**Fig. 1.** Manifests and image are both build outputs; the deploy step only reconciles them against the cluster — no templating engine in the default path ([[What is the Quarkus fast-jar packaging format]] describes what goes inside the image).

## Why the model fits Kubernetes

Resource-fit: small RSS and fast start make scale-from-zero pods responsive, and the `startupProbe` covers JVM warmup honestly instead of faking it with a huge `initialDelaySeconds`. Config-fit: runtime-config properties map to env vars with relaxed naming (`quarkus.datasource.jdbc.url` ← `QUARKUS_DATASOURCE_JDBC_URL`), which is exactly what ConfigMaps and Secrets inject. Health-fit: probes, health groups and metrics all land on /q/* paths the cluster scrapes. For richer orchestration (CRDs, operators) the kubernetes-client extension speaks the API from inside the app.

> [!warning] Generated manifests do not mean "no YAML knowledge needed"
> Two common failures: teams tune `quarkus.kubernetes.*` blind and never read the produced YAML — until resources requests are wrong and the pod gets OOM-killed or throttled; and image pull failures from a registry the manifest references but the cluster cannot reach (missing `registry`/`group` settings or a missing push step — generation does not push). Also, `quarkus deploy` requires the container-image build to be configured (`quarkus.container-image.build=true` is not on by default) — the classic first-run error is "manifest applied, image never existed".

> [!tip] Interview answer
> Deployment is three build-time pieces: quarkus-kubernetes generates Deployment, Service and RBAC into target/kubernetes and auto-wires the probes to /q/health when the health extension is present; a container-image extension — docker, jib, s2i or buildpack — builds and optionally pushes the image; and quarkus deploy applies the manifests. Config comes from env vars so ConfigMaps and Secrets bind naturally, and in the app I verified the generated Deployment had liveness, readiness and startup probes without hand-written YAML.
