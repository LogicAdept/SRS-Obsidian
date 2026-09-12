<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# How does service discovery work in Kubernetes

> [!abstract] Short answer
> Two cooperating mechanisms. First, **DNS**: CoreDNS, the cluster add-on, resolves Service names — `<service>.<namespace>.svc.cluster.local` — to the Service's stable ClusterIP (or, for headless Services, to the individual pod IPs), so clients find each other by name, not by IP. Second, **the Service + endpoints machinery**: every pod's `/etc/resolv.conf` points at the cluster DNS via the kubelet's `clusterDNS` setting, and kubelet also injects environment variables for Services existing before the pod starts. The registry is the API server itself: a Service created or deleted is immediately DNS-visible — no separate discovery store.

## Names and their scope

A full name is `my-svc.my-namespace.svc.cluster.local`: the `svc.cluster.local` zone is cluster-internal, namespace resolution lets a pod in `default` call plain `orders` for a sibling `orders.default` Service, and cross-namespace calls spell the namespace out. The lookup lands on a virtual IP held by the Service, and kube-proxy routes to current endpoints — callers cache the *name*, never the pod IP ([[How does networking work in Kubernetes]] — pod IPs are routable but mortal). A headless Service (`clusterIP: None`) flips the deal: DNS A records return each ready pod's address directly — `db-0.db-headless...`, `db-1.db-headless...` — which is how StatefulSet members enumerate peers and how client-side load balancers get real endpoints ([[What is a StatefulSet in Kubernetes and when do you need one]]). Endpoint slices feed both DNS and kube-proxy, so readiness is what joins or evicts a pod from every lookup at once ([[What is the difference between liveness readiness and startup probes in Kubernetes]] — the readiness gate is the discovery gate).

The Java-relevant corollary: traditional client-side discovery libraries (Eureka, Consul registries) register and heartbeat explicitly; Kubernetes replaces the *registration* half automatically — pods are registered by being ready and labeled — leaving your app only to consume a name. That is why Spring Cloud Kubernetes can swap Eureka for plain Service DNS ([[How would you explain client side service discovery]] and its server-side counterpart frame the pattern vocabulary).

```d2
direction: right
app: "app pod\nenv: DB_HOST=orders" {
  width: 230
  height: 90
  style.fill: "#e3f2fd"
}
dns: "CoreDNS\norders.default.svc.cluster.local" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
cip: "Service ClusterIP\n10.96.14.20" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
eps: "endpoint slices\nready pods only" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
pods: "orders pods\n10.42.0.5, 10.42.1.7" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
app -> dns -> cip -> eps -> pods
```

**Fig. 1.** The chain from a name to a live pod: CoreDNS answers the name with the virtual IP, kube-proxy rules choose a current endpoint — readiness decides membership.

> [!warning] Discovery is readiness-shaped, not existence-shaped
> The traps: a pod is discoverable the moment it is *Ready*, not when the process starts — long warmups without a readiness probe join DNS empty-handed or, worse, get traffic before being able to serve it. Headless Services return only ready pods too, so a quorum app can see its own peers disappear mid-flap. And the namespace trap: bare `orders` resolves *inside your own namespace only* — code that works in dev because everything shares `default` breaks in prod the moment namespaces split.

> [!tip] Interview answer
> Kubernetes ships DNS-based discovery: CoreDNS serves a svc.cluster.local zone, Service names resolve to the stable ClusterIP — or, for headless Services, to individual ready pod IPs — and the API server's endpoint slices are the source of truth that DNS and kube-proxy both consume. Registration is automatic: being labeled and Ready *is* the registration, so there is no separate registry to heartbeat against; namespace scoping gives short names inside a namespace and FQDNs across. Pod IPs stay routable but mortal, so clients cache names, never IPs.
