<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What are the main components of the Kubernetes architecture

> [!abstract] Short answer
> A cluster splits into the **control plane** — kube-apiserver (the single front door exposing the Kubernetes HTTP API), etcd (the consistent key-value store holding all cluster state), kube-scheduler (assigns new pods to nodes), and kube-controller-manager (runs the reconcile loops) — plus **node components** on every worker: kubelet (talks to the API, keeps the node's pods running), kube-proxy (network rules for Services), and a container runtime such as containerd. Everything else, including kubectl and CoreDNS, is a client or an add-on around these.

## Control plane: the brain

kube-apiserver is the only component that matters for correctness conversations: every read and write of cluster state goes through it — kubectl, the scheduler, controllers, and the kubelet all are its clients, and nothing talks to etcd except the API server itself. The scheduler watches for pods with no assigned node and picks one by filtering and scoring candidates; it never starts anything itself. The controller-manager bundles the controllers that implement Deployment, ReplicaSet, Node, and Job behavior — each a loop of "observe, diff, act". etcd stores the result: the entire desired and observed state of the cluster as key-value records. The cloud-controller-manager (optional) wires node load balancers and routes to a specific cloud ([[What is etcd in Kubernetes]] covers the storage, [[How does Kubernetes achieve high availability]] covers why you run three or five of them).

## Node components: the muscle

Every worker runs a kubelet — the node agent that watches the API server for pods scheduled to its node and drives the container runtime to match their specs, including probes and mounts. kube-proxy installs the network rules (iptables or IPVS) that give Service cluster IPs their load-balancing behavior on that node ([[How does networking work in Kubernetes]]). The container runtime — containerd, or CRI-O — actually creates containers over the CRI; Docker is no longer a supported Kubernetes runtime, which is a favorite trap question. Add-ons like CoreDNS (cluster DNS) and monitoring agents run as ordinary pods, usually as DaemonSets.

```bash
./kubectl version --client
```

**Listing 1.** Every component above ships as an independent versioned binary; the client here is kubectl v1.37.0 with Kustomize v5.8.1 bundled — the cluster components can run the same version or neighbors, because the API contract, not the binary set, is the compatibility surface.

```
Client Version: v1.37.0
Kustomize Version: v5.8.1
```

```d2
direction: right
you: "kubectl / CI" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
apiserver: "kube-apiserver\nonly door to state" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
etcd: "etcd\nall cluster state" {
  width: 190
  height: 90
  style.fill: "#ffebee"
}
sched: "kube-scheduler\nassign pods to nodes" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
cm: "kube-controller-manager\nreconcile loops" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
node1: "node: kubelet + kube-proxy\n+ containerd -> pods" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
you -> apiserver
apiserver -> etcd
sched -> apiserver: "watch, bind"
cm -> apiserver: "watch, patch"
node1 -> apiserver: "kubelet watches\nits pods"
apiserver -> node1: "scheduled pods"
```

**Fig. 1.** Hub-and-spoke: components do not talk to each other — they all watch and write through kube-apiserver, which is the sole owner of etcd.

> [!warning] Nothing bypasses the API server
> The classic architecture trap: "which component writes pod state to etcd?" — none directly; only kube-apiserver touches etcd, so it is both the performance bottleneck and the consistency anchor. Two more traps: the scheduler only *assigns* pods (kubelet does the starting), and kube-proxy is marked optional in the docs because some CNIs implement Service traffic their own way.

> [!tip] Interview answer
> The control plane is kube-apiserver — the only entry point that persists everything to etcd — kube-scheduler, which assigns unscheduled pods to nodes by filtering and scoring, and kube-controller-manager running the reconcile loops. On every node you have kubelet driving the container runtime, kube-proxy installing Service routing rules, and containerd or CRI-O running containers. All components communicate only through the API server; etcd is never touched directly.
