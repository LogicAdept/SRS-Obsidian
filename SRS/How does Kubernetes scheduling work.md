<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How does Kubernetes scheduling work

> [!abstract] Short answer
> The kube-scheduler watches for pods with no assigned node and, for each, runs a two-phase decision: **filtering** — discard nodes that cannot fit the pod (requests, ports, volumes, node selectors, taints, affinity) — then **scoring** — rank the survivors (spread, image locality, affinity weights) and pick the best. The scheduler only *binds* the pod to a node in the API; the kubelet on that node does the actual starting. Control hooks come in the same vocabulary everywhere: `nodeSelector`, node/pod affinity and anti-affinity, taints and tolerations, topology spread.

## Filter, score, bind

Filtering is feasibility: does the node have enough allocatable CPU and memory for the pod's requests ([[How do resource requests and limits work in Kubernetes]] — requests are the admission currency), are the requested ports free, do the volumes match topology, does the pod tolerate the node's taints. Scoring ranks what survived: spreading replicas across zones and nodes, preferring nodes that already have the image (less pulling), affinity weights, and so on; the highest score wins and ties are randomized. The output of all this is one API write — the pod's `spec.nodeName` — and from that moment the kubelet owns the pod's fate; a "scheduled" pod can still fail to start, which is why scheduler-side and runtime-side symptoms look different ([[How do you debug a Pod that fails to start]] — Pending is the scheduler saying no, CrashLoopBackOff is the kubelet trying).

Placement constraints, in rising sophistication: `nodeSelector` matches labels — the simple, recommended case; node affinity adds operators and soft/hard variants (`preferred` vs `required`); pod (anti-)affinity co-locates or separates pods *relative to other pods*; taints work in reverse — nodes repel pods that do not explicitly tolerate them, which is how control-plane nodes stay empty and how draining marks nodes; topology spread constraints distribute across failure domains. When nothing fits, the pod stays `Pending` — either genuinely unschedulable (ask for less, add capacity) or waiting for a cluster-autoscaler node ([[How does autoscaling work in Kubernetes]]).

```d2
direction: right
queue: "pods without nodeName" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
filter: "filtering\nrequests, taints, affinity, ports, volumes" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
score: "scoring\nspread, image locality, weights" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
bind: "bind spec.nodeName\none API write" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
pending: "no node passes\npod stays Pending" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
queue -> filter
filter -> score: "feasible nodes"
filter -> pending: "none"
score -> bind: "best node"
```

**Fig. 1.** The decision is pure API arithmetic: no node is contacted during scheduling — the kubelet discovers its new pod by watching the API server like everyone else.

> [!warning] The scheduler trusts requests, and affinity is not a guarantee
> The traps: "it fits" is measured in *requests*, not reality — a node full of under-requesting pods becomes CPU-oversubscribed the moment everyone bursts; skew comes back as eviction and throttling. Required affinity that cannot be satisfied is not a preference — it is a Pending pod forever. Taints vs tolerations is directional and often stated backwards: the node taints itself, the pod tolerates, not the other way around. And `nodeName` set manually bypasses the scheduler entirely — admission webhooks and defaults do not run ([[What do admission controllers do in Kubernetes]]).

> [!tip] Interview answer
> Scheduling is a two-phase bin-packing loop: the kube-scheduler filters nodes by hard feasibility — requests against allocatable, taints, selectors, volumes, ports — then scores survivors for soft preferences like zone and replica spread and image locality, and finally writes the chosen node into spec.nodeName. It never starts containers; the kubelet does. Placement control is a layered vocabulary: nodeSelector for simple cases, affinity with required and preferred variants, pod anti-affinity for spreading, taints and tolerations for repelling, topology spread for domains; unsatisfiable means Pending, not error.
