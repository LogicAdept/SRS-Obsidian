<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How do you perform a rolling update and rollback in Kubernetes

> [!abstract] Short answer
> You change the pod template of the Deployment (`kubectl set image`, `kubectl apply` with a new manifest) — the controller does the rest: it creates a new ReplicaSet for the new template and shifts replica counts from old to new under the `RollingUpdate` strategy's `maxSurge` and `maxUnavailable` bounds (both 25% by default). New pods must pass readiness before the next wave, a stuck rollout halts itself after `progressDeadlineSeconds`, and `kubectl rollout undo` flips back to the previous ReplicaSet revision.

## The mechanics of the rollout

A rollout is replica-count arithmetic between ReplicaSets ([[What is the difference between a Deployment and a ReplicaSet in Kubernetes]]): with `replicas: 10`, `maxUnavailable: 25%` rounds down to 2 — at most 2 pods fewer than 10 at any moment; `maxSurge: 25%` rounds up to 3 — at most 13 pods total. Readiness probes are the gate: a wave advances only when the new pods report Ready, which ties update speed directly to how honest your probes are ([[What is the difference between liveness readiness and startup probes in Kubernetes]]). If the new version crashes on boot or never becomes ready, the Deployment's controller **stops scaling up the new ReplicaSet automatically** and, after `progressDeadlineSeconds` (600s default), marks the rollout as stuck — old pods keep serving because they were never scaled away. `kubectl rollout status` watches this; `kubectl rollout pause` holds a half-applied template for canary-style inspection; `history` and `undo --to-revision=N` work because old ReplicaSets are retained by `revisionHistoryLimit` (default 10).

```bash
./kubectl set image deploy/web nginx=nginx:1.27-alpine
./kubectl rollout status deploy/web
./kubectl rollout history deploy/web
./kubectl rollout undo deploy/web
```

**Listing 1.** The whole operational surface in four lines: change the template, watch the controller shift ReplicaSet counts, list revisions, and revert — the undo is another template change, just pointed at the old ReplicaSet.

```d2
direction: right
old: "RS v1\n10 pods, all Ready" {
  width: 210
  height: 90
  style.fill: "#fff3e0"
}
new: "RS v2 created\ntemplate changed" {
  width: 220
  height: 90
  style.fill: "#e3f2fd"
}
wave: "+3 surge, -2 unavailable\nnew pods must pass readiness" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
ok: "RS v2: 10 pods\nRS v1: 0, kept for undo" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
stuck: "new pods not Ready\nrollout halts, old serve on" {
  width: 320
  height: 100
  style.fill: "#ffebee"
}
old -> new -> wave
wave -> ok: "progress"
wave -> stuck: "no progress"
stuck -> ok: "rollout undo"
```

**Fig. 1.** The safety story: capacity dips are bounded by maxUnavailable, spikes by maxSurge, and failure freezes the state where old pods still hold the traffic.

> [!warning] A ready pod is not a working service
> The sharpest trap: readiness only proves the process answers, not that the release is good — a bad endpoint returning 200 rolls out smoothly. Zero-downtime also needs the shutdown side: preStop plus `terminationGracePeriodSeconds` so in-flight requests finish while endpoints are removed ([[What is the service per container pattern]]-style front ends observe endpoint removal only after the pod starts terminating). And `maxUnavailable: 0` with a slow-starting app silently turns every deploy into a blocked one — surge without readiness honesty is the classic foot-gun.

> [!tip] Interview answer
> Updating a Deployment's pod template makes the controller create a new ReplicaSet and shift replicas under maxSurge and maxUnavailable — by default 25 percent — with readiness probes gating each wave. Stuck rollouts self-halt after progressDeadlineSeconds and keep old pods serving; history is just retained ReplicaSets, so rollout undo re-points the template at the previous revision. Real zero-downtime adds the exit side: preStop hooks, graceful termination, and honest readiness — otherwise you roll out 200-OK garbage at full speed.
