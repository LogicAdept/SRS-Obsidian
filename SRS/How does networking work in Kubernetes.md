<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How does networking work in Kubernetes

> [!abstract] Short answer
> Kubernetes imposes one flat contract on the network: **every pod gets its own routable IP**, any pod can reach any other pod on that IP **without NAT**, and a node can reach every pod — so pods behave like little hosts on one big virtual network. The platform does not implement this itself: the **container runtime delegates to a CNI plugin** (Calico, Cilium, Flannel...) that wires IPs and routes per node. Everything above the flat net — stable names, load balancing — is Services and DNS layered on top.

## The four problems the docs name

The official framing is worth repeating in interviews because it explains why the pieces exist: container-to-container inside a pod (solved by the shared network namespace — localhost), pod-to-pod (the CNI's flat network), pod-to-Service (kube-proxy's virtual IP routing), external-to-Service (the Service types and Ingress). The flat model's cost is IP discipline: pod CIDR, service CIDR, and node addresses must not overlap, and every node must be able to route to every pod CIDR — this is exactly what dual-stack clusters re-solve per IP family, and what makes pod IPs burn space. NAT is not banned at the edges — traffic leaving the cluster SNATs through the node, and inbound paths terminate somewhere — but *inside* the cluster, pod-to-pod is IP-to-IP, which is what makes NetworkPolicies meaningful ([[How do you secure a Kubernetes cluster]] — a policy that says "deny pod X from pod Y" only works because identities are real IPs, not port-mapped host ports).

Who does the work: kube-proxy on each node programs Service rules (iptables or IPVS) — the pod-to-Service leg; the CNI plugin assigns pod IPs, builds routes/overlays or BGP fabrics — the pod-to-pod leg; CoreDNS answers names ([[How does service discovery work in Kubernetes]]). The Docker-world contrast: Docker builds per-bridge NAT by default; Kubernetes demands a routable per-pod IP and pushes complexity into the CNI ([[How do containers find each other by name on a Docker network]] is the container-runtime counterpart).

```d2
direction: right
p1: "pod A\n10.42.0.11" {
  width: 180
  height: 80
  style.fill: "#e8f5e9"
}
p2: "pod B (other node)\n10.42.1.12" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
flat: "flat pod network\nno NAT pod-to-pod" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
svc: "Service ClusterIP\nvirtual, kube-proxy rules" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
ext: "external traffic\nSNAT out / LB in" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}
p1 -> flat
p2 -> flat
flat -> svc: "name resolves\nthen routed"
flat -> ext: "egress"
```

**Fig. 1.** Three zones of the model: the flat no-NAT core between pods, the virtual Service layer above it, and NAT confined to the cluster edge.

> [!warning] Flat does not mean open — and pod IPs are still not addresses
> Two traps: "flat network" is frequently misread as "no network policy needed" — the model says nothing about *access control*, only reachability; default posture is all-allow, and the rules that restrict it live in NetworkPolicy objects, which need a CNI that implements them. The second trap: hardcoding pod IPs or expecting them to survive rescheduling — the flat model guarantees routability, not stability; only Services and DNS are stable. And a CNI that fails silently after an upgrade is a classic outage: pods run, but the flat net is gone.

> [!tip] Interview answer
> The Kubernetes network model says: every pod gets a routable, cluster-unique IP, pod-to-pod traffic needs no NAT, and nodes reach pods directly — pods are first-class network citizens, not port-mapped tenants. The runtime delegates to a CNI plugin that assigns pod IPs and builds the routing, kube-proxy programs Service virtual IPs with iptables or IPVS, and CoreDNS names the Services. Non-overlapping CIDRs are the operator's obligation, NAT only appears at the cluster edge, and access control is a separate layer — NetworkPolicies — which only works because pod identities are real IPs.
