<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What are init containers and sidecars in Kubernetes

> [!abstract] Short answer
> **Init containers** are special containers in a pod that run to completion **before** the application containers start — sequentially, each one required to succeed; the app does not begin until all of them are done. A **sidecar** is the sibling pattern: a helper container that runs **alongside** the app for the pod's whole life (proxy, log shipper, config reloader). Kubernetes now models sidecars natively as init containers with `restartPolicy: Always`, which start first but never "complete".

## Init: strict prerequisites

Init containers answer "the app must not start until X is true": wait for the database endpoint to resolve, register with a leader-election system, generate or fetch secrets, chown a mounted volume, run schema migration. The rules make them safe for that role: they run one at a time in order, each must exit 0 before the next runs, and if one fails, the pod restarts it (per the pod's `restartPolicy`) instead of ever starting the app — a pod with init containers is not Ready until every init container has succeeded, and init containers deliberately do not support probes or lifecycle hooks: they are either running or done. Resource requests are charged at the *maximum* of any single init container versus the sum of app containers, not their sum — init containers run sequentially, and scheduling reflects that ([[How do resource requests and limits work in Kubernetes]]). Their logs come from the same `kubectl logs` with the `-c` container selector.

## Sidecars: the modern native form

Classically, a sidecar is just a second container in `spec.containers` — a proxy that carries all traffic, a log tailer reading a shared `emptyDir`, a git-sync refreshing files. The lifecycle wrinkle: the classic sidecar cannot be *guaranteed* to start before the app or stop after it. Kubernetes 1.28+ fixes this natively: an init container with `restartPolicy: Always` starts before app containers (order preserved) and keeps running for the pod's lifetime, with its image restarted if it dies — and during pod termination, native sidecars are stopped last, after app containers. Jobs with proxies finally work correctly this way: the sidecar survives until the Job's work ends. This is also the mechanism under service meshes ([[What is the Sidecar pattern]] — the mesh proxy per workload is exactly this shape), and the pattern boundary is the same as for pods themselves: if the helper shares the pod's lifecycle and needs localhost access to the app, it is a sidecar; if it is a prerequisite, it is an init container ([[What is a Pod in Kubernetes]]).

```yaml
spec:
  initContainers:
    - name: wait-for-db
      image: busybox:1.36
      command: ["sh", "-c", "until nc -z db 5432; do sleep 2; done"]
  containers:
    - name: proxy
      image: envoy:1.31
      restartPolicy: Always
    - name: app
      image: myapp:1.42
```

**Listing 1.** Both roles in one pod: `wait-for-db` gates the start, `proxy` declares `restartPolicy: Always` inside `initContainers` — native sidecar, first to start, last to stop.

```d2
direction: right
start: "pod created" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
init1: "init: wait-for-db\nmust exit 0" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
sidecar: "native sidecar starts\nrestartPolicy: Always" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
app: "app container runs\ntalks via localhost" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
term: "termination\napp stops first, sidecar last" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
start -> init1 -> sidecar -> app -> term
```

**Fig. 1.** Ordering is the whole value: init gates the start, the native sidecar brackets the app's lifetime on both ends.

> [!warning] Init is not startup logic and a sidecar is not a microservice
> Migrations and data seeding in init containers rerun on *every* pod restart of a Deployment — make them idempotent or move them to a Job. A failing init container loops the whole pod in `Init:CrashLoopBackOff` — there is no probe to blame. On the sidecar side, each helper shares the pod's resource bill, CPU throttling, and failure domain: a runaway sidecar starves the app container on the same node bill — init and app containers are one scheduling unit ([[What is a Pod in Kubernetes]]), not two services.

> [!tip] Interview answer
> Init containers run sequentially before app containers and must each succeed — the app never starts otherwise — so they gate startup: wait for dependencies, prepare volumes, fetch config; they have no probes and their resources count at the max of one, since they run one at a time. Sidecars are helpers sharing the pod's lifetime, and modern Kubernetes declares them as init containers with restartPolicy Always — started before the app, restarted on failure, stopped after it on termination, which finally makes proxies-in-Jobs correct. Prerequisite means init; lifelong companion means sidecar.
