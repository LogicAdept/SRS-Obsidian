<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is the difference between a ConfigMap and a Secret in Kubernetes

> [!abstract] Short answer
> Both are objects that inject configuration into pods — as environment variables, command arguments, or mounted files. A **ConfigMap** holds plain, non-sensitive data. A **Secret** is the sensitive sibling: values are base64-encoded on the API surface (obscured, not encrypted), access is gated by RBAC, and the platform adds hardening options — encryption at rest, `stringData` convenience, typed secrets for tokens and TLS. The difference is a trust and handling contract, not a schema.

## Same mechanics, different handling

Either object is referenced from a pod spec in two ways: `envFrom`/`valueFrom` to materialize entries as environment variables, or a volume mount to expose them as files — file mounts are the recommended shape for anything the app reloads, because kubelet propagates volume updates after a sync delay, while environment variables are frozen at container start and never update. Size is capped at 1 MiB each: configuration, not file storage. Secrets get the sensitive-data treatment: `data` holds base64, `stringData` accepts plain text at write time; types like `kubernetes.io/tls` or `dockerconfigjson` add shape validation; and since etcd is where both live ([[What is etcd in Kubernetes]]), the platform's real protections for Secrets are RBAC narrowing, **encryption at rest** (a kube-apiserver encryption-provider config, not a default), and disabling them from being logged by tooling. An `immutable: true` flag on either object prevents accidental rewrites and stops watch-storm churn ([[How do you secure a Kubernetes cluster]] — secrets are a threat-model question, not a base64 question).

```bash
./kubectl create secret generic db-cred --from-literal=password=s3cret --dry-run=client -o yaml
./kubectl create configmap app-conf --from-literal=log.level=info --dry-run=client -o yaml
```

**Listing 1.** kubectl v1.37.0, both generators side by side: the Secret's value lands base64-encoded (`s3cret` becomes `czNjcmV0`), the ConfigMap's stays plain — the API surface difference in one screen.

```
apiVersion: v1
data:
  password: czNjcmV0
kind: Secret
metadata:
  name: db-cred
---
apiVersion: v1
data:
  log.level: info
kind: ConfigMap
metadata:
  name: app-conf
```

```d2
direction: right
src: "ConfigMap / Secret" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
env: "as env vars\nfrozen at container start" {
  width: 280
  height: 100
  style.fill: "#fff3e0"
}
vol: "as mounted volume\nkubelet refreshes updates" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
rbac: "Secret extras\nRBAC, encryption at rest, typed kinds" {
  width: 340
  height: 100
  style.fill: "#ffebee"
}
src -> env
src -> vol
src -> rbac: "only for\nsecrets"
```

**Fig. 1.** One injection mechanism, one critical fork: files can be re-read after updates, environment cannot — and only Secrets carry the protection bundle.

> [!warning] base64 is not encryption
> The trap interviewers set: "Secrets are encrypted because they are base64" — decoding takes one flag, and anyone with pod-`get`/`secret`-list RBAC or API log access sees plaintext; without encryption-at-rest enabled, the plaintext is sitting in etcd too. The second trap: passing database credentials as ConfigMap "because it is easier to diff" — the object kind is part of the security stance (GitOps tooling, audit, and secret-rotation systems treat them differently). The third: env-var secrets leak through crash dumps, `kubectl describe`, and child processes — file mounts reduce the surface ([[How do you manage secrets in Docker at runtime]] is the same story one layer down).

> [!tip] Interview answer
> ConfigMap and Secret are the same injection mechanism — env vars or mounted files, 1 MiB cap, volume updates propagate while env vars never do. The difference is the trust contract: Secrets are base64-encoded on the wire, not encrypted; the real protections are RBAC, optional etcd encryption at rest, typed kinds like TLS or docker-registry, and handling discipline — file mounts over env, immutability where possible. ConfigMap for anything you could put in a Git diff, Secret for anything you would not.
