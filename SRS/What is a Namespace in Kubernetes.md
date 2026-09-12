<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is a Namespace in Kubernetes

> [!abstract] Short answer
> A Namespace is a **virtual cluster inside the cluster**: a scope for object names (a Deployment named `api` can exist in every namespace) and the unit for policy, quotas, and RBAC delegation. Four ship with the system — `default`, `kube-system`, `kube-public`, `kube-node-lease`. Namespaces do **not** provide network isolation by themselves: every pod can still reach every other unless NetworkPolicies say otherwise.

## What a namespace scopes — and what it does not

Inside a namespace, names must be unique per kind; across namespaces, the full identity is the name plus its namespace ([[How does service discovery work in Kubernetes]] — the same rule gives DNS its `svc.cluster.local` shape). Resource-wise, a namespace is where isolation is *declared*: a **ResourceQuota** caps the sum of CPU, memory, and object counts its occupants may consume; a **LimitRange** injects default requests and limits into pods that arrive without them, keeping quota accounting sane; RBAC Roles are namespace-scoped while ClusterRoles are not, which makes namespaces the delegation boundary for teams. System components live in `kube-system`, node heartbeats in `kube-node-lease` (Lease objects keep node liveness cheap), `kube-public` holds publicly readable data. Object deletion is namespace-wide: deleting the namespace deletes everything in it — the blunt instrument behind the classic "we lost staging" story.

The honest limits: namespaces are soft multi-tenancy — fine for team and environment separation, not a security boundary against a hostile tenant; the network stays flat cluster-wide by default ([[How does networking work in Kubernetes]]), and node-level resources (ports, kernels) are shared. For hard tenancy you add NetworkPolicies, Pod Security admission, separate node pools — namespaces are the *organizing unit*, not the wall.

```d2
direction: right
cluster: "cluster\none API server, one etcd" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
ns1: "namespace: team-a\nquota 8 CPU / 16 Gi\nown RBAC Role" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
ns2: "namespace: team-b\nquota 4 CPU / 8 Gi\nown RBAC Role" {
  width: 270
  height: 100
  style.fill: "#e8f5e9"
}
flat: "network still flat\npods reach pods across ns" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
cluster -> ns1
cluster -> ns2
ns1 -> flat
ns2 -> flat
```

**Fig. 1.** Namespaces partition names, quotas, and RBAC — the dotted line is administrative; the network line only appears when NetworkPolicies draw it.

> [!warning] Namespaces are not environments-in-a-box and not firewalls
> The traps: "prod and staging in one cluster, separated by namespaces" — shared nodes, shared control plane, one bad ResourceQuota or one leaked ClusterRole touches both; the isolation story needs admission policy and capacity hygiene. The second trap: relying on namespaces for network security — without a CNI implementing NetworkPolicies and policies actually written, cross-namespace traffic is default-allow. The third: `kube-system` as a playground — putting workloads there inherits system upgrade and eviction semantics you do not want ([[How do you secure a Kubernetes cluster]] treats namespace scoping as the first RBAC layer).

> [!tip] Interview answer
> A namespace scopes object names — same names can repeat per namespace, cross-references spell the namespace — and is the unit for ResourceQuota, LimitRange, and namespace-scoped RBAC, which makes it the delegation boundary for teams and environments. The system namespaces are default, kube-system for control-plane workloads, kube-node-lease for node heartbeats, kube-public. Crucially, namespaces give no network isolation by default — pods talk across namespaces unless NetworkPolicies forbid it — so they are organizational soft tenancy, not a security wall.
