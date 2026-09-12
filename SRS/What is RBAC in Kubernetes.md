<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is RBAC in Kubernetes

> [!abstract] Short answer
> RBAC (Role-Based Access Control) answers "who can do what to which objects". **Roles** (namespace-scoped) and **ClusterRoles** (cluster-wide) hold *rules*: verbs (`get`, `list`, `watch`, `create`, `update`, `delete`) over resource kinds. **RoleBindings** and **ClusterRoleBindings** attach those rules to *subjects*: users, groups, or — in practice, most often — **ServiceAccounts**. Authorization is purely additive: there are no deny rules; the API server grants only what some binding explicitly allows.

## The four objects and how they compose

The split of labor: Role vs ClusterRole decides *scope* (a Role in `team-a` says nothing about `team-b`; a ClusterRole covers the whole API, including non-namespaced objects like nodes); Binding vs ClusterBinding decides *who gets it where*. The composition trick everyone uses: a ClusterRole describes a capability ("view", "edit", "admin" ship with the cluster), and RoleBindings reference it to grant that capability *only inside their namespace* — cluster-level definition, namespace-level delivery. Subjects deserve the interview emphasis: human access comes through OIDC/cert identities and groups, but **workload access is a ServiceAccount** — a pod runs `as` a ServiceAccount, its token is auto-mounted (or projected via the TokenRequest API), and every API call the app makes rides that identity. Default posture matters: with RBAC enabled, no permission exists until granted — `system:anonymous` is nothing, and listing pods in another namespace fails by default.

The Java-shop corollary: your app's in-cluster API calls (checking endpoints, leader election, custom controllers) fail with `Forbidden` until someone binds a Role to the pod's ServiceAccount — the classic fix is a Role + RoleBinding pair per concern, not ClusterRoleadmin ([[How do you secure a Kubernetes cluster]] — least-privilege ServiceAccounts are the first control on the checklist).

```yaml
kind: Role
metadata:
  name: pod-reader
  namespace: team-a
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
---
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: team-a
subjects:
  - kind: ServiceAccount
    name: ci-bot
    namespace: team-a
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**Listing 1.** The minimal real pair: `ci-bot` may read pods and their logs in `team-a` and nowhere else — note `pods/log`, a subresource, which is where RBAC's granularity shows.

```d2
direction: right
who: "ServiceAccount ci-bot" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
bind: "RoleBinding (ns team-a)\nattaches subject to role" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
role: "Role pod-reader\nverbs get list watch" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
res: "pods, pods/log\nonly in team-a" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
who -> bind -> role -> res
```

**Fig. 1.** Authorization always flows through a binding: the Role never names subjects, the binding never names verbs — and the namespace of the binding caps the reach.

> [!warning] No deny rules, and wildcards are a foot-gun
> The traps: RBAC has no deny — an admin cannot "forbid" a verb; they must audit that no binding grants it. `verbs: ["*"]` and `resources: ["*"]` in hand-written roles silently include escalation-capable operations (`pods/exec`, `secrets` read — which is reading every credential in the namespace). Secrets are resources like any other: whoever can `get` secrets in a namespace owns its credentials ([[What is the difference between a ConfigMap and a Secret in Kubernetes]]). And changing a pod's ServiceAccount to `default` "to make it work" quietly hands the app whatever the default identity has.

> [!tip] Interview answer
> RBAC is additive authorization: Roles or ClusterRoles define verb-over-resource rules — with subresources like pods/log as first-class entries — and RoleBindings or ClusterRoleBindings attach them to users, groups, or ServiceAccounts. Scope comes from the binding: a ClusterRole bound inside a namespace delivers a reusable capability there. Workloads authenticate as ServiceAccounts with projected tokens, so least privilege means per-app identities and narrow verbs. No deny rules exist, wildcards leak escalation paths, and secret read equals credential ownership — that is the security review lens.
