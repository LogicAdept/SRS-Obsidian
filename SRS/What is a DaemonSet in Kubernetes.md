<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is a DaemonSet in Kubernetes

> [!abstract] Short answer
> A DaemonSet ensures **every node — or a selected subset of nodes — runs exactly one copy of a pod**, and keeps that invariant as nodes join and leave the cluster. It exists for node-local infrastructure: log collectors, node-level metrics agents, CNI plugins, storage and device drivers, and other facilities that must sit on every machine by definition. You scale it implicitly: the unit of scaling is the node, not a replica count.

## The one-pod-per-node contract

Unlike a Deployment, a DaemonSet has no `replicas` field — the desired count is derived from eligible nodes. When a new node appears, the DaemonSet controller puts a pod on it; when the node drains or is removed, the pod goes with it. Node selection uses the same vocabulary as everything else — `nodeSelector`, affinity, and taints/tolerations — so you can run an agent on GPU nodes only, or on Linux nodes only, and modern DaemonSets get a default toleration for `node.kubernetes.io/not-ready` and `unreachable` so agents still land on nodes that are not yet healthy ([[How does Kubernetes scheduling work]]). When a DaemonSet is deleted, its pods go with it, per node. For updates it supports RollingUpdate (the default, one node at a time) and OnDelete — the pattern where the agent only changes when the node or pod is manually recycled.

The standard interview examples map one-to-one to real clusters: Fluentd/Vector-style log shippers reading node container logs, node-exporter for Prometheus, kube-proxy and CNI agents themselves, and CSI node plugins — all DaemonSets ([[How does logging work in Kubernetes]] and [[How do you monitor a Kubernetes cluster]] show the consumers). A side observation that lands well: DaemonSets are how you can often tell what a cluster considers "part of the operating system" — everything that must be everywhere is a DaemonSet.

```bash
./kubectl create deployment agent --image=busybox:1.36 --dry-run=client -o yaml | grep -c replicas
```

**Listing 1.** The conceptual contrast, run on kubectl v1.37.0: a Deployment manifest carries a `replicas` field; a DaemonSet manifest cannot — its pod count is the number of matching nodes, decided by the controller, not by you.

```
0
```

```d2
direction: right
ds: "DaemonSet\nno replicas field" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
n1: "node-1\nagent pod" {
  width: 180
  height: 90
  style.fill: "#e8f5e9"
}
n2: "node-2\nagent pod" {
  width: 180
  height: 90
  style.fill: "#e8f5e9"
}
n3: "node-3 (GPU, nodeSelector)\nagent pod" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
join: "node-4 joins\npod scheduled automatically" {
  width: 310
  height: 90
  style.fill: "#fff3e0"
}
ds -> n1
ds -> n2
ds -> n3
n1 -> join: "reacts to\ntopology"
```

**Fig. 1.** Scaling is the cluster's job: add a node, the DaemonSet notices and places a pod — remove it, the pod is cleaned up.

> [!warning] DaemonSets are not for your applications
> Putting an application into a DaemonSet "so every node has it" couples its lifecycle to node topology instead of demand — no autoscaling, no surge. The other trap is forgetting taints: an agent without the right tolerations silently skips tainted nodes (and the reverse — a DaemonSet with too-broad tolerations lands on control-plane nodes). Also, `nodeSelector` on a DaemonSet is not a scaling mechanism: nodes that stop matching get their pods removed.

> [!tip] Interview answer
> A DaemonSet guarantees one copy of a pod on every matching node, adding and removing them as nodes come and go — no replicas field, the node set is the replica count. It is the controller for node-local infrastructure: CNI and kube-proxy agents, log collectors, node-exporter, device plugins. Node targeting works through nodeSelector, affinity, and taints and tolerations, and updates roll one node at a time or wait for OnDelete. If the workload serves user traffic, it is a Deployment; if it must exist wherever a node exists, it is a DaemonSet.
