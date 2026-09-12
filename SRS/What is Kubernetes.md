<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #DevOps/Orchestration #SRS

# What is Kubernetes

> [!abstract] Short answer
> Kubernetes (K8s) is an open-source **container orchestration platform**: instead of telling a cluster what to do step by step, you declare the **desired state** of your workloads in API objects — Deployments, Services, ConfigMaps — and its controllers continuously reconcile the live cluster toward that declaration: they schedule containers across nodes, restart what dies, expose stable network endpoints, and scale on demand. Kubernetes grew out of Google's Borg and is now the CNCF-graduated standard for running containers in production.

## The problem it solves

Running one container is `docker run`. Running hundreds of containers across dozens of hosts is a different problem class entirely: which host gets which container, who restarts a crashed one, how do containers find each other when IPs change on every restart, how do you ship a new version without downtime, and how do configuration and credentials reach the right containers only. Kubernetes answers all of these with one mechanism: a shared API backed by a controller per resource type. You hand the API a desired state — three replicas of this image behind a Service — and controllers do the placement, healing, and exposure work forever after ([[What are the main components of the Kubernetes architecture]]).

## Reconciliation is the core idea

Everything in Kubernetes is declarative: an object's `spec` is what you want, its `status` is what the cluster observed, and controllers run reconcile loops that keep working on the difference. Kill a pod managed by a Deployment and nothing "runs" a restart command — the ReplicaSet controller simply notices `spec.replicas` is now `3` while the live count is `2` and creates a replacement. This is why "self-healing" is not a feature bolted on top but a consequence of the model, and why tools that mutate live state without touching the declared spec fight the platform ([[How do you perform a rolling update and rollback in Kubernetes]] works the same way — a new desired state, applied gradually).

```bash
./kubectl create deployment web --image=nginx:1.27 --replicas=3 --dry-run=client -o yaml
```

**Listing 1.** A client-side dry run (kubectl v1.37.0, no cluster) prints the declarative object the command generates: `apiVersion: apps/v1`, `kind: Deployment`, `spec.replicas: 3`, a pod `template` — this YAML is the whole contract you submit, and the cluster does the rest.

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

## What ships in the box

The standard "what are its features" answer maps directly to objects: automated rollouts and rollbacks (Deployment), service discovery and load balancing (Service, DNS), storage orchestration (PersistentVolumes), config and secret management (ConfigMap, Secret), horizontal autoscaling from CPU or custom metrics, batch runs (Job, CronJob), and self-healing driven by probes. Kubernetes itself does not build images, does not pull source code, and is not a PaaS — it assumes container images exist and orchestrates where and how they run ([[How does Docker differ from Kubernetes]] covers the split: Docker packages and runs one container, Kubernetes coordinates fleets of them).

```d2
direction: right
desired: "You submit desired state\nDeployment: 3 replicas" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
api: "API server persists it\ncontrollers observe" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
diff: "ReplicaSet controller\ndiff: want 3, live 2" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
act: "create 1 pod\nscheduler places it" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
observe: "status updated\nloop continues forever" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
desired -> api
api -> diff
diff -> act
act -> observe
observe -> api
```

**Fig. 1.** The reconcile loop never finishes by design: state drifts (a node dies, someone scales the Deployment), controllers keep closing the gap between `spec` and reality.

> [!warning] Kubernetes is not a Docker replacement
> A recurring interview trap: Kubernetes does not replace Docker's job of building images or even of running one container — every node still needs a container runtime (containerd or CRI-O), and Kubernetes talks to it over the CRI. Also, "Kubernetes restarts everything" is overstated: controllers recreate objects they own; a bare pod deleted by hand stays deleted because nothing declares it.

> [!tip] Interview answer
> Kubernetes is a container orchestration platform built around a declarative API: you describe the desired state — replicas, networking, config — in objects, and controllers continuously reconcile the live cluster toward it. That one mechanism gives you self-healing, rolling updates, service discovery with DNS, scaling, and secret management. It runs containers via a CRI runtime like containerd, and it deliberately stops at orchestration: no image builds, no source deploys.
