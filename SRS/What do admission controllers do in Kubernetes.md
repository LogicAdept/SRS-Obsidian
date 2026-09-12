<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What do admission controllers do in Kubernetes

> [!abstract] Short answer
> Admission controllers are **API server plugins that intercept requests after authentication and authorization but before persistence** — the enforcement and mutation stage of every write. Built-ins validate schema and quotas (`NamespaceLifecycle`, `ResourceQuota`, `LimitRanger`, `PodSecurity`) and can mutate objects (defaulting, sidecar injection). Clusters extend them with **webhooks**: a ValidatingAdmissionWebhook or MutatingAdmissionWebhook registers a service URL, and the API server POSTs every matching request to it — accept, reject with a message, or (for mutating) return a JSON patch. Policy engines (Kyverno, Gatekeeper) and sidecar injectors are just well-known webhook implementations.

## Where admission sits in the request pipeline

A write passes four gates: authenticate (who), authorize ([[What is RBAC in Kubernetes]] — may this identity do this verb), **admit** (is this write *correct and allowed by policy*), then persist ([[What are the main components of the Kubernetes architecture]] — etcd via the API server). Authorization knows identities and verbs but nothing about object content; admission is the content stage — where `privileged: true` gets rejected, missing labels get injected, and quotas get decremented. Mutating webhooks run first (reinvocation rules aside), then object schema validation, then validating webhooks — order matters when a mutation must happen before validation sees the final object. Failures have a dangerous knob: a webhook's `failurePolicy` is `Fail` or `Ignore` — `Fail` on a webhook that watches everything means the API server stops accepting writes when the webhook is down (a classic outage story), `Ignore` means policy silently vanishes during incidents; production picks `Fail` with tight selectors and self-hosted, HA webhook deployments.

## The policy-engine era

Nobody hand-rolls one webhook per rule anymore: Kyverno and OPA Gatekeeper register as webhooks and evaluate declarative policy bundles — require team labels, forbid `latest` tags, require resource limits, block `hostPath` ([[How do you secure a Kubernetes cluster]] treats this as the enforcement tier). Pod Security admission — the built-in replacement for the removed PodSecurityPolicy — is itself an admission controller enforcing profiles (`baseline`, `restricted`) per namespace. The interview-grade summary: admission is where cluster *policy* lives, as opposed to RBAC's *permissions* — permissions say who may ask; admission says which asks are acceptable.

```d2
direction: right
req: "authenticated,\nauthorized request" {
  width: 250
  height: 100
  style.fill: "#e3f2fd"
}
mut: "mutating admission\nbuilt-ins + webhooks: inject, default" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
val: "validating admission\nschema, quotas, PSA, webhooks" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
etcd: "persist to etcd" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
deny: "rejected\nwith a reason" {
  width: 180
  height: 80
  style.fill: "#ffebee"
}
req -> mut -> val
val -> etcd: "all pass"
val -> deny: "any fail"
```

**Fig. 1.** Mutation precedes validation; rejection is explicit and the reason surfaces in kubectl — that message is the policy engine speaking.

> [!warning] failurePolicy is a loaded gun
> The traps: a mutating webhook with `failurePolicy: Fail` and a selector too broad — its pod dies, and every write in the cluster (including pods that would restart the webhook) is refused: a self-inflicted outage loop. The opposite setting, `Ignore`, disables your security policy exactly during the incident when it matters. Others: mutating webhooks that mutate their own deployment (exclusion rules exist for a reason); policies tested only against happy-path YAML; and forgetting that `kubectl apply` surfaces admission rejections as errors — CI must treat them as first-class failures ([[What is the difference between kubectl apply and kubectl create]]).

> [!tip] Interview answer
> Admission controllers run inside the API server after authn and authz, before persistence: built-ins default and validate — namespaces, quotas, limit ranges, Pod Security — and webhooks extend them: a mutating webhook returns patches (sidecar injection, defaults), a validating one accepts or rejects with a reason. That stage is where cluster policy lives, which is why Kyverno and Gatekeeper are webhooks, and why failurePolicy matters: Fail turns webhook downtime into cluster-wide write outage, Ignore silently disables policy. Permissions say who may ask; admission says which asks are acceptable.
