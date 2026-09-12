<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How does autoscaling work in Kubernetes

> [!abstract] Short answer
> Three independent axes, three controllers. **HPA** (HorizontalPodAutoscaler) changes the *replica count* of a workload — Deployment, StatefulSet — based on metrics: resource metrics (CPU/memory vs requests) from metrics-server, or custom/external metrics from the metrics APIs. **VPA** adjusts *pod resource requests* to observed usage. **Cluster Autoscaler** (or Karpenter) adds and removes *nodes* when pods are unschedulable or idle. They compose but do not coordinate: HPA scales pods, CA scales the pool they live on.

## HPA: the one interviewers mean

The HPA loop runs through the API server: it computes the ratio of observed metric to target (say, 80% average CPU utilization — utilization measured **against each pod's CPU request**, which makes correct requests a precondition, not a detail) and scales `spec.replicas` proportionally, with stabilization windows and rate limits to prevent flapping. Metrics plumbing matters: resource metrics need **metrics-server** running — without it, `kubectl top` is empty and an HPA on CPU shows `unknown`; custom metrics (queue length, RPS) go through the custom-metrics API served by an adapter (Prometheus adapter is the classic). Scaling up is immediate on breach; scaling *down* is deliberately delayed (default stabilization window of 5 minutes) because load curves lie. HPA does not touch pods that a controller does not manage ([[What is the difference between a Deployment and a ReplicaSet in Kubernetes]] — the HPA rewrites the Deployment's replicas, and the ReplicaSet chain does the rest), and it must not fight a fixed `replicas:` in a reapplied manifest ([[What is the difference between kubectl apply and kubectl create]] — the classic GitOps/HPA conflict).

## The other two axes

VPA watches actual usage and rewrites requests — in recommendation mode first, since its auto mode evicts pods to resize them, which surprises people. Cluster Autoscaler watches the *scheduler's* failures: pods stuck Pending for lack of allocatable capacity trigger node additions, and long-underutilized nodes trigger consolidation — it scales the pool that makes HPA's scaling physically possible. The standard interview composition: HPA on CPU or custom metric + Cluster Autoscaler behind it; VPA mostly for right-sizing analysis.

```d2
direction: right
load: "load rises\nCPU > 80% of request" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
hpa: "HPA computes ratio\nscale replicas up" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
dep: "Deployment -> ReplicaSet\nnew pods scheduled" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
full: "node capacity exhausted\npods Pending" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
ca: "Cluster Autoscaler\nadds nodes" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
load -> hpa -> dep
dep -> full: "if no room"
full -> ca
```

**Fig. 1.** The two-level answer: HPA fixes load at pod granularity; when the pod layer runs out of physics, the Cluster Autoscaler buys more physics.

> [!warning] Autoscaling amplifies bad requests
> The traps: an HPA targeting CPU with *missing or wrong requests* — the percentage is of requests, so no request means no meaningful target and scaling thrashes. HPA plus a fixed `replicas` field in the applied manifest — every apply stomps the HPA's decision. HPA plus VPA both on CPU — they fight over the same signal. Scaling down aggressively during a deploys-and-restarts storm evicts busy pods; the stabilization window exists because of that, not for fun. And an HPA cannot rescue a single-replica, non-graceful app: scaling out amplifies whatever the startup story is ([[How do you perform a rolling update and rollback in Kubernetes]]).

> [!tip] Interview answer
> Kubernetes scales on three axes: HPA rewrites replica counts from metrics — CPU or memory versus requests via metrics-server, custom metrics via the metrics API and adapters — with a stabilization window on scale-down; VPA right-sizes requests; Cluster Autoscaler adds or drains nodes for Pending pods and idle capacity. The interview-grade detail: HPA's CPU target is a percentage of the pod's request, so requests are part of the scaling contract, and a fixed replicas in your manifest will fight the HPA every apply.
