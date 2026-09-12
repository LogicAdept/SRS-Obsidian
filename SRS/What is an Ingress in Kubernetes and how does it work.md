<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Kubernetes #SRS

# What is an Ingress in Kubernetes and how does it work

> [!abstract] Short answer
> An Ingress is an API object that describes **L7 (HTTP) routing rules** — which host and which path go to which Service — but it does nothing by itself: an **Ingress controller** (NGINX, Traefik, HAProxy, a cloud one) must watch Ingress objects and actually configure a reverse proxy or balancer. It is the standard answer to "one public entry point, many Services": TLS termination, host-based and path-based routing, and name-based virtual hosts, without paying for a cloud LoadBalancer per Service.

## Resource and controller: the two halves

The Ingress resource is declarative data: rules matching `host` + `path` to a `service:port` backend, an optional default backend for unmatched requests, and a `tls` section referencing a TLS Secret whose cert the controller terminates on the same entry point. The controller is the missing engine — no controller, no behavior, which is why "I applied an Ingress and nothing listens" is a rite of passage. Controllers implement the same rules differently: path matching semantics (prefix vs exact) are defined by the API, but header handling, rewrites, and annotations are controller-specific — a portability trap hidden in plain sight ([[What are the Kubernetes Service types and when do you use each]] — the Ingress controller's pods are reached by a Service of type LoadBalancer or NodePort; Ingress rides *on top of* a Service type, it does not replace it). For the interview: LoadBalancer is per-Service and L4; Ingress is per-cluster (or per-namespace group) and L7 — one balancer fans out to dozens of Services by host and path.

The spec is also deliberately frozen: the Gateway API is the designated successor — typed resources (Gateway, HTTPRoute) splitting infrastructure from routing — and interviewers increasingly expect a one-liner on it: Ingress is stable and everywhere, Gateway API is the modern, more expressive replacement being adopted incrementally.

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: shop
spec:
  tls:
    - hosts: [shop.example.com]
      secretName: shop-tls
  rules:
    - host: shop.example.com
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: api-svc
                port: { number: 80 }
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-svc
                port: { number: 80 }
```

**Listing 1.** The canonical shape: one host, TLS from a Secret, two path rules — the controller turns this into proxy config; the cluster turns the Secret into the certificate presented at the edge ([[What is the difference between a ConfigMap and a Secret in Kubernetes]]).

```d2
direction: right
net: "internet" {
  width: 150
  height: 80
  style.fill: "#e3f2fd"
}
lb: "Service: LoadBalancer\none public IP" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
ctrl: "Ingress controller pods\nNGINX / Traefik" {
  width: 270
  height: 90
  style.fill: "#fff3e0"
}
r1: "shop.example.com/api\n-> api-svc:80" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
r2: "shop.example.com/\n-> web-svc:80" {
  width: 250
  height: 90
  style.fill: "#e8f5e9"
}
net -> lb -> ctrl
ctrl -> r1
ctrl -> r2
```

**Fig. 1.** Public cost stops at one LoadBalancer; host and path decisions happen inside controller pods, then normal Services carry traffic to pods.

> [!warning] An Ingress with no controller is a YAML ornament
> The traps: installing an Ingress in a cluster without a controller — it routes nothing, silently. Assuming annotation portability — `nginx.ingress.kubernetes.io/*` rewrites do nothing on Traefik. Mismatched `pathType` expectations — `Prefix` matches segment boundaries, not raw string prefixes, so `/api` does not catch `/apiv2` under Prefix but does under ImplementationSpecific behaviors that differ per controller. And forgetting that TLS only covers the hosts you listed in the `tls` block — everything else terminates plain HTTP.

> [!tip] Interview answer
> Ingress is an L7 routing API: rules of host and path mapping to Service backends, plus TLS termination from a referenced Secret — but it needs an Ingress controller watching it and reconfiguring a real proxy. It sits on top of a LoadBalancer or NodePort Service, so the cluster keeps exactly one public entry point for many Services — that is the cost argument against per-Service LoadBalancers. Rules semantics are standardized, but annotations are controller-specific, which is the portability tax; the Gateway API is the successor design that separates gateway infrastructure from route objects.
