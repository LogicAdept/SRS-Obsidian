<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is the difference between a Deployment and a ReplicaSet in Kubernetes

> [!abstract] Short answer
> A **ReplicaSet** is the low-level controller that keeps a fixed number of identical pods running — it does scaling and self-healing and nothing else. A **Deployment** sits above it and owns ReplicaSets: it adds declarative rollouts — a new pod template produces a *new* ReplicaSet that the Deployment scales up while scaling the old one down — plus rollback, pause, and revision history. You never manage ReplicaSets directly; you manage Deployments and let the chain Deployment → ReplicaSet → Pod do its job.

## What each layer contributes

The ReplicaSet's entire contract is the set: it watches pods matching its `selector`, and creates or deletes until the live count equals `spec.replicas`. It has no notion of versions — change its pod template and it does nothing to existing pods. The Deployment is the versioning layer: on a template change it creates a fresh ReplicaSet (a "revision") and performs the rollout by shifting replica counts between the old and new ReplicaSets according to `maxSurge`/`maxUnavailable`. Old ReplicaSets are kept (bounded by `revisionHistoryLimit`) precisely so `rollout undo` can flip back — this is why "delete the ReplicaSet" answers are wrong: the Deployment simply recreates it ([[How do you perform a rolling update and rollback in Kubernetes]] is the operational payoff). Both layers select pods by **label selectors**, not names — the selector is immutable after creation, a favorite trap ([[What is a Pod in Kubernetes]] — labels are the join key of the whole API).

## Why the split matters in interviews

Interviewers use this pair to test whether you understand controllers as composition, not as a zoo of YAML kinds. The same pattern repeats: Job wraps pods, CronJob wraps Jobs, StatefulSet plays the ReplicaSet role for identity-bearing pods. The practical corollary: `kubectl get rs` shows one ReplicaSet per pod template ever applied — several coexisting during a rollout is normal, and replicas spread across them is the rollout in progress.

```bash
./kubectl create deployment web --image=nginx:1.27 --replicas=3 --dry-run=client -o yaml
```

**Listing 1.** The generated object (kubectl v1.37.0) contains only a pod `template`, `replicas: 3` and a `selector` — the Deployment spec; the ReplicaSet it will create is implied, not written by you.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: web
  name: web
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web
  strategy: {}
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - image: nginx:1.27
        name: nginx
        resources: {}
status: {}
```

```d2
direction: right
dep: "Deployment\nversioning + rollout strategy" {
  width: 270
  height: 90
  style.fill: "#e3f2fd"
}
rs1: "ReplicaSet v2\n3 pods (new template)" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
rs0: "ReplicaSet v1\n0 pods, kept for undo" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
pods: "pods\nself-healing + scaling" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
dep -> rs1: "scale up"
dep -> rs0: "scale down\nrevision kept"
rs1 -> pods
rs0 -> pods: "own pods by\nlabel selector"
```

**Fig. 1.** A rollout is replica-count arithmetic between two ReplicaSets; each ReplicaSet itself only ever keeps its count alive.

> [!warning] Selector traps and direct-RS edits
> Changing a Deployment's `spec.selector` is rejected — it would orphan pods owned by the old selector; labels in `template.metadata.labels` must match the selector or the API server rejects the Deployment outright. Editing a ReplicaSet's replicas by hand "works" until the Deployment reconciles it back. And `replicas: N` set by a scaling tool is later overridden by the next `apply` with an old file — the apply-vs-imperative drift in miniature ([[What is the difference between kubectl apply and kubectl create]]).

> [!tip] Interview answer
> ReplicaSet is the primitive that keeps N identical pods alive via label selectors — self-healing and scaling only. Deployment manages ReplicaSets: each pod template revision becomes a new ReplicaSet, rollouts shift counts between them under maxSurge and maxUnavailable, history is retained for rollback, and bad rollouts can be paused. You operate Deployments; touching ReplicaSets directly just gets reconciled away. The composition pattern repeats with Job and CronJob and with StatefulSet for stable-identity pods.
