<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is a Pod in Kubernetes

> [!abstract] Short answer
> A Pod is the **smallest deployable unit** in Kubernetes: one or more containers that share the same network namespace (one IP, one port space), the same IPC, and often the same volumes, and that are scheduled **as a unit onto a single node**. Containers inside a pod talk to each other over localhost and must coordinate ports. You almost never create bare pods — controllers (Deployment, StatefulSet, DaemonSet, Job) own and manage them, which is what gives you self-healing and scaling.

## Why pods group containers

A pod models one logical host: containers in it see each other at `localhost:port`, share `/etc/hosts` and IPC, and can share files through volumes mounted into several containers. The classic healthy split is one application container plus small helpers — a log shipper reading a shared volume, a proxy terminating TLS in front of the app — rather than "everything in one image". The scheduling consequence matters for sizing: pods are atomic, so a pod fits a node only if its containers' requests sum within the node's allocatable resources; two fat containers in one pod mean two fat pods' worth of resources always travel together ([[How do resource requests and limits work in Kubernetes]]). If two containers do not need to share a lifecycle and network, they belong in different pods — that is the interview litmus test ([[What is the Sidecar pattern]] formalizes the helper-container arrangement).

## Lifecycle in one breath

A pod passes through phases: `Pending` (accepted, containers not all running yet — waiting for scheduling, image pull, or an init container), `Running` (bound to a node, at least one container up), `Succeeded` or `Failed` (all containers terminated with exit 0 / any failure), and `Unknown` (node lost contact). Inside `Running`, each container has its own state — waiting, running, terminated — driven by restart policy and probes. The phase is coarse on purpose; `kubectl describe` is how you see the container-level truth ([[How do you debug a Pod that fails to start]] uses exactly that gap). Pods are mortal by design: their identity is not stable across rescheduling — stable identity is what StatefulSets add ([[What is a StatefulSet in Kubernetes and when do you need one]]).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: probe-demo
  labels:
    app: probe-demo
spec:
  containers:
    - name: app
      image: busybox:1.36
      command: ["sh", "-c", "touch /tmp/ready; httpd -f -p 8080"]
      ports:
        - containerPort: 8080
      startupProbe:
        httpGet: { path: /, port: 8080 }
        failureThreshold: 30
        periodSeconds: 2
      resources:
        requests: { cpu: 100m, memory: 64Mi }
        limits: { memory: 128Mi }
```

**Listing 1.** A single-container pod from the empirics manifests (`scripts/empirics/kubernetes/probe-pod.yaml`): one IP for the pod, the app listens on 8080, probes and resources attach per container — the container, not the pod, is the unit for both.

```d2
direction: right
pod: "Pod (one IP per pod)\nshared net + IPC + volumes" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
app: "app container\nlocalhost:8080" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
helper: "helper container\nships logs from volume" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
sched: "scheduled as a unit\nonto one node" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
controller: "owned by a controller\nDeployment, DaemonSet, Job" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
pod -> app
pod -> helper
pod -> sched
pod -> controller
```

**Fig. 1.** Pod anatomy: the shared network namespace is the headline — one IP means inter-container traffic is plain localhost and ports must be unique within the pod.

> [!warning] Pods are not pets and localhost is not a RPC bus
> Two traps: packing an app and a database into one pod "because they talk to each other" — they then always scale, fail, and restart together, which no one wants; and treating pod IP as an address to remember — pod IPs change on every reschedule, only Services and DNS give stable names ([[How does service discovery work in Kubernetes]]). A bare pod deleted by hand is gone forever — no controller, no recreation.

> [!tip] Interview answer
> A pod is the atomic scheduling unit of Kubernetes: one or more containers sharing a network namespace — a single IP, so they talk over localhost and must not clash on ports — plus optional shared volumes and IPC. Kubernetes schedules the pod as a whole onto one node, and real workloads let controllers own pods for self-healing and scaling. Lifecycle phases are Pending, Running, Succeeded or Failed; the IP is ephemeral, so exposure goes through Services. Use multiple containers per pod only when they genuinely share a lifecycle — app plus sidecar helper.
