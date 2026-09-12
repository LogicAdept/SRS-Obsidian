<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/Containerisation #DevOps/Tools/Kubernetes #DevOps/Orchestration #SRS

# How does Docker differ from Kubernetes

> [!abstract] Short answer
> Docker is a **build-and-run tool**: a client plus daemon that builds images and starts containers on a single host. Kubernetes is a **container orchestrator**: a control plane plus node agents that run the same (OCI) containers across many hosts, adding scheduling, replication, self-healing, service discovery, and rolling updates. They compose — Docker builds the image, Kubernetes runs fleets of it.

## One host versus a reconciled cluster

With Docker alone you manage containers one host at a time: `docker run` starts a container, and if the host dies, the container dies with it. Kubernetes shifts the model to **declarative desired state**: you declare "3 replicas of this image", and controller-manager processes watch etcd's recorded state versus reality and reconcile continuously — restarting, rescheduling, scaling.

```d2
direction: right
dock: "Docker Engine (per host)\nCLI -> dockerd -> containerd/runc\nyou run containers by hand" {
  width: 380
  height: 110
  style.fill: "#e3f2fd"
}
cp: "Kubernetes control plane\nkube-apiserver + etcd\nscheduler + controllers" {
  width: 360
  height: 110
  style.fill: "#fff3e0"
}
n1: "node 1\nkubelet -> Pods" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
n2: "node 2\nkubelet -> Pods" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
dock -> cp: "images pushed to a registry"
cp -> n1: "schedule"
cp -> n2: "schedule"
```

**Fig. 1.** Docker is the per-host build/run engine; Kubernetes is the control plane (API server front end, etcd backing store, scheduler, controllers) telling kubelets on every node which Pods to run.

Unit of deployment changes too: Kubernetes schedules **Pods** — one or more containers sharing network and storage — not bare containers, and gives each Service a stable virtual IP and DNS name while pod IPs churn. A port you publish with `-p` in Docker becomes a Service/ingress concern; the container-to-container DNS idea survives in cluster DNS ([[What does the EXPOSE instruction in a Dockerfile actually do]] covers the publish half). The application-shape consequence: service-per-container is the unit both are built around ([[What is the service per container pattern]]), but only an orchestrator automates its placement and recovery.

> [!warning] "Kubernetes replaces Docker" — no: it replaces the manual part
> Kubernetes never ran Docker Engine as its core: node runtimes are containerd or CRI-O, both OCI implementations, so a Docker-built image runs unchanged ([[What is the OCI and how does Docker relate to containerd and runc]]). What Kubernetes removes is the human `docker run` + `docker restart` + hand-configured networks loop — and brings its own operational price: a whole control plane to run, or a managed one to pay for. Docker-vs-Kubernetes is also not Swarm: Docker's own Swarm mode exists but is a different, lighter orchestrator, not the platform the interview means.

> [!tip] Interview answer
> **Docker builds and runs containers on one host — client, daemon, images, ports. Kubernetes orchestrates them across a cluster: a control plane (API server, etcd, scheduler, controllers) reconciles declared state, kubelets run Pods on nodes, Services give stable names and IPs. It uses the same OCI images — Docker builds, Kubernetes runs fleets, and it adds self-healing, scaling, and rolling updates on top.**

