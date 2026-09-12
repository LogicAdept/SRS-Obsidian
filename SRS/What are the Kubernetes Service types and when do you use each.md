<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What are the Kubernetes Service types and when do you use each

> [!abstract] Short answer
> A Service gives a **stable virtual IP and DNS name** for a set of pods selected by labels, and its `type` controls *how far* that address reaches: **ClusterIP** (default) — an internal-only virtual IP inside the cluster; **NodePort** — also opens a static high port (30000–32767) on every node; **LoadBalancer** — additionally asks the cloud for an external load balancer pointing at the nodes; **ExternalName** — no proxying at all, just a DNS CNAME alias. A **headless** Service (`clusterIP: None`) skips the virtual IP and returns pod IPs straight from DNS.

## The onion from inside out

Each type is a strict superset of the previous one, which is why the "when do you use each" answer is a reach decision. ClusterIP is the default and the workhorse: one `clusterIP` that never changes, load-balanced by kube-proxy rules to current pod endpoints — pod IPs churn, the Service does not ([[How does networking work in Kubernetes]] carries the rule-installation story). NodePort extends it outward: every node listens on the same port and forwards to the Service, useful for on-prem demos, webhooks, and environments where you control your own external balancer — but it exposes a fixed port per service and knows nothing about HTTP routing. LoadBalancer is the cloud-integrated extension: the provider creates a real balancer (often with its own static IP) that forwards to node ports; it is per-Service, so twenty services mean twenty balancers and twenty bills — that is where Ingress enters ([[What is an Ingress in Kubernetes and how does it work]]). ExternalName is a DNS trick — the Service's name resolves as a CNAME to `external.database.example` — handy for renaming external dependencies without touching app config. Headless Services opt out of proxying entirely: `clusterIP: None` makes DNS return the individual pod addresses, which is what StatefulSets and client-side balancing need ([[What is a StatefulSet in Kubernetes and when do you need one]]).

```bash
./kubectl create service clusterip svc-demo --tcp=80:8080 --dry-run=client -o yaml
```

**Listing 1.** kubectl v1.37.0 generating a Service: `type: ClusterIP` is the default, and the split between `port: 80` (what clients dial) and `targetPort: 8080` (what pods listen on) is the versioning seam.

```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: svc-demo
  name: svc-demo
spec:
  ports:
  - name: 80-8080
    port: 80
    protocol: TCP
    targetPort: 8080
  selector:
    app: svc-demo
  type: ClusterIP
status:
  loadBalancer: {}
```

```d2
direction: right
client: "external client" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
lb: "LoadBalancer\ncloud balancer, static IP" {
  width: 290
  height: 90
  style.fill: "#ffebee"
}
np: "NodePort\n30000-32767 on every node" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
cip: "ClusterIP\nvirtual IP, stable DNS" {
  width: 270
  height: 90
  style.fill: "#e8f5e9"
}
pods: "pod endpoints\nvia label selector" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
client -> lb -> np -> cip -> pods
```

**Fig. 1.** Types as layers: each outer type still has the inner ones underneath — a LoadBalancer Service is also a NodePort and a ClusterIP.

> [!warning] NodePort is not a production ingress and selector-less Services are not mistakes
> The traps: serving user traffic on NodePorts "because it works" — no TLS, no host routing, one more open port per service, and the port range is dictated to you. Publishing a Service does nothing if the platform has no LoadBalancer implementation — `status.loadBalancer` stays empty forever (the empty `status` block is already visible in the generated manifest above). A Service whose selector points at nothing (or at pods whose labels changed) resolves and then connects nowhere — endpoints, not the Service, are the truth to check when debugging ([[How do you debug a Pod that fails to start]] starts one layer below this).

> [!tip] Interview answer
> A Service is a stable virtual IP plus DNS in front of label-selected pods; the type decides reach. ClusterIP, the default, is internal-only. NodePort opens the same 30000-to-32767 port on every node. LoadBalancer adds a cloud balancer in front — one per Service, which is why Ingress exists for HTTP at scale. ExternalName is a pure DNS CNAME for external dependencies, and a headless Service with clusterIP None skips proxying so DNS returns pod IPs directly — StatefulSets need that. Behind the scenes it is kube-proxy rules moving traffic to current endpoints, so pod churn is invisible to clients.
