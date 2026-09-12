<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How do you secure a Kubernetes cluster

> [!abstract] Short answer
> Security layers in interview order: **authentication and authorization** (OIDC/certs for humans, per-workload ServiceAccounts with least-privilege RBAC); **workload isolation** (NetworkPolicies for the default-allow flat network, Pod Security admission instead of the removed PodSecurityPolicy, security contexts — runAsNonRoot, read-only root filesystem, dropped capabilities); **secret hygiene** (etcd encryption at rest, no secrets in env where avoidable); **admission control** as the enforcement point; and supply-chain basics — scanned images, pinned digests, no `latest`. The cluster API itself stays private, protected by TLS and audit logging.

## The layers that actually matter

Start from the two properties every layer defends: *who can act* and *what code can do*. Identity: human users through OIDC or client certs; every workload gets its own ServiceAccount, and default-anything is a finding ([[What is RBAC in Kubernetes]] — additive, namespace-scoped grants). Network: the Kubernetes network model is all-allow — pods reach pods across namespaces until **NetworkPolicies** deny it, and they need a CNI that implements them; the standard shape is default-deny ingress and egress per namespace, then allow-list ([[How does networking work in Kubernetes]]). Pod hardening: `securityContext` — `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, dropped `CAP_*`, read-only root fs; enforce cluster-wide with Pod Security admission (the `restricted` profile) rather than per-pod hope. Secrets: base64 is not encryption — enable etcd encryption at rest, prefer file mounts over env vars, rotate via external secret managers where the platform is not enough ([[What is the difference between a ConfigMap and a Secret in Kubernetes]]). Admission: ValidatingAdmissionWebhook and MutatingAdmissionWebhook are where policy engines (Kyverno, OPA Gatekeeper) block unscanned images, require labels, and inject sidecars [[What do admission controllers do in Kubernetes]].

## The API server and the supply chain

The control plane is the crown jewel: keep the API endpoint private or firewall it, disable anonymous auth, enable audit logging to a sink you actually watch, and treat kubeconfig files as root credentials. Supply chain: images from trusted registries, scanned (Trivy-style) in CI and at admission, referenced by digest for immutability, built with minimal bases ([[How do you reduce the size of a Docker image]] — small surfaces are small attack surfaces). The honest summary interviewers like: Kubernetes is secure by *configuration*, not by default — the defaults optimize operability, and the checklist is how you pay that debt down.

```d2
direction: right
req: "request / workload" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
authn: "authenticate\nOIDC, certs, SA tokens" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
authz: "authorize RBAC\nadditive, least privilege" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
adm: "admission\npolicy engines, PSA" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
run: "runtime hardening\nsecurityContext, NetworkPolicy, secrets at rest" {
  width: 380
  height: 100
  style.fill: "#e8f5e9"
}
req -> authn -> authz -> adm -> run
```

**Fig. 1.** Defense in depth is a pipeline: every stage must pass, and the runtime layer is where zero-trust networking and pod hardening live.

> [!warning] Common "it is fine" findings
> The recurring audit findings: `default` ServiceAccount running workloads (no identity, no revocation); pods with `privileged: true` "temporarily"; unencrypted etcd with Secrets inside ([[What is etcd in Kubernetes]]); a flat network with no default-deny — any compromised pod scans the whole cluster; and everyone `cluster-admin` because RBAC felt bureaucratic. Each is one YAML line to fix and one incident not to have.

> [!tip] Interview answer
> I secure a cluster in layers. Identity: OIDC for people, one least-privilege ServiceAccount per workload, RBAC additive grants, no wildcard verbs. Network: default-deny NetworkPolicies over the all-allow flat model, via a CNI that enforces them. Pods: securityContext — non-root, no privilege escalation, dropped capabilities, read-only filesystem — enforced by Pod Security admission, with policy webhooks for image scanning and digests. Secrets: etcd encryption at rest, file mounts over env vars. Plus private API endpoint, audit logs, and treating kubeconfigs as root credentials. Defaults are operable, not secure — the checklist is the security.
