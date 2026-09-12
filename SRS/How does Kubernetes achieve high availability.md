<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How does Kubernetes achieve high availability

> [!abstract] Short answer
> At both layers, the same recipe: redundancy plus failure detection plus redistribution. The **control plane** is HA by running multiple kube-apiserver replicas behind one endpoint with a 3-or-5-member etcd quorum underneath — losing a control-plane node costs capacity, not availability, as long as etcd keeps majority. **Workloads** are HA through multiple replicas spread across nodes and zones (anti-affinity, topology spread), probes that route traffic only to healthy pods, Deployments that recreate what dies, **PodDisruptionBudgets** to keep voluntary operations (drains, upgrades) from stacking outages, and multi-zone clusters so a datacenter event is a blip, not an outage.

## Control plane: quorum is the anchor

The API server is stateless — run 2-3 of it behind a load balancer and clients keep working through member failures; that part is easy. The state is etcd, and etcd availability *is* control-plane availability: a 3-member etcd survives one member loss, 5 survive two — below quorum the API server refuses writes (the cluster freezes rather than forks, [[What is etcd in Kubernetes]]), which is why stacked topologies (etcd on control-plane nodes) use odd member counts and why losing "just one master" of two is the worst configuration. The scheduler and controller-manager also run active-passive through leader election (Lease objects in kube-node-lease) — replicas everywhere, one acting.

## Workloads: from replicas to disruption budgets

Pod-level HA composes four controls. Replicas: the Deployment keeps the count alive through node deaths ([[What is the difference between a Deployment and a ReplicaSet in Kubernetes]]). Spread: pod anti-affinity and topology spread constraints place replicas across nodes and zones, so one failure domain holds one replica, not all. Health: readiness gates traffic to functioning pods only ([[What is the difference between liveness readiness and startup probes in Kubernetes]]); liveness restarts the wedged. Protection from *your own operations*: **PodDisruptionBudget** — `minAvailable` or `maxUnavailable` — makes voluntary disruptions (drain, upgrade, autoscaler consolidation) wait: an eviction that would breach the budget is rejected until capacity allows. PDBs cover voluntary disruption only — a node catching fire is involuntary and bypasses them entirely; that distinction is the interview's favorite precision test. Zonal architecture completes it: multi-zone clusters with per-zone capacity make zone loss survivable without reserve headroom elsewhere ([[How do you perform a rolling update and rollback in Kubernetes]] — upgrades are the routine HA stress test).

```d2
direction: right
lb: "one API endpoint\nload balancer" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
a1: "apiserver-1" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
a2: "apiserver-2" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
a3: "apiserver-3" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
etcd: "etcd quorum 2 of 3\nsurvives 1 member loss" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
z: "zones a + b + c\nreplicas spread, PDB guards drains" {
  width: 380
  height: 90
  style.fill: "#e8f5e9"
}
lb -> a1
lb -> a2
lb -> a3
a1 -> etcd
a2 -> etcd
a3 -> etcd
etcd -> z: "scheduling\ncontinues"
```

**Fig. 1.** Control-plane HA is one load balancer over stateless apiservers over an etcd quorum; workload HA is spread plus probes plus PDB-guarded churn.

> [!warning] HA is not copies — and PDBs do not stop fires
> The traps: two etcd members (or two "masters") — any single failure loses quorum or splits decisions; HA starts at three. Replicas scheduled onto the same node or zone by luck — affinity and topology spread are declarations, not defaults ([[How does Kubernetes scheduling work]]). Missing PDBs — every drain becomes an outage; PDBs set to `minAvailable: 100%` — drains become impossible, which is the opposite failure. And assuming etcd replication is a backup — snapshots are separate ([[What is etcd in Kubernetes]]); quorum survives member loss, not data corruption.

> [!tip] Interview answer
> Control plane: stateless kube-apiservers behind one endpoint, three or five etcd members for a Raft quorum that tolerates one or two failures, leader-elected scheduler and controller-manager — losing quorum freezes writes by design instead of forking. Workloads: multiple replicas spread by anti-affinity and topology spread across nodes and zones, readiness and liveness probes deciding traffic and restarts, and PodDisruptionBudgets so drains and upgrades cannot stack voluntary outages — knowing PDBs cover voluntary disruption only, and that etcd quorum is the anchor, is the whole senior answer.
