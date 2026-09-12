<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Nginx #SRS

# What is the difference between HAProxy, Nginx and Envoy

> [!abstract] Short answer
> All three are proxies with load balancing, but their centers of gravity differ: **HAProxy** is a dedicated TCP/HTTP load balancer — a traffic regulator, normalizer, and SSL terminator that deliberately does nothing else; **Nginx** is a web server first — static content, HTTP reverse proxying, caching — with load balancing as a strong second role; **Envoy** is an L7 proxy and communication bus designed for service-to-service meshes, with dynamic configuration (xDS APIs) and first-class HTTP/2 and gRPC.

HAProxy describes itself as a TCP proxy and HTTP reverse proxy: it load balances TCP connections (decision per connection) and HTTP requests (decision per request), normalizes traffic, terminates or initiates TLS with runtime-updatable certificates (SNI-aware), applies rate limiting, and protects against abuse. Its limits are deliberate and documented: it is **not** a static web server — it chroots at startup and never touches the filesystem — and it is **not** a packet-based balancer: no NAT, no DSR; that is IPVS territory. Nginx uses a master-process plus worker-processes event-driven model, serves static content fast, proxies and caches HTTP, and balances over upstreams (round-robin, `least_conn`, `ip_hash`); a stream module extends it to raw TCP/UDP sessions. Envoy runs out-of-process next to every application server, forming a transparent mesh over localhost: pluggable L3/L4 and L7 filters, HTTP/1.1↔HTTP/2↔HTTP/3 translation, gRPC as a first-class routing substrate, service discovery and configuration through layered dynamic APIs, active and passive (outlier-detection) health checking, retries, circuit breaking, and built-in stats and tracing.

```d2
direction: right
edge: "HAProxy\nTCP/HTTP LB at the edge" {
  width: 300
  height: 100
  style.fill: "#e3f2fd"
}
web: "Nginx\nweb server + reverse proxy" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
mesh: "Envoy\nsidecar mesh, xDS, gRPC" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
edge -> web
web -> mesh
```

**Fig. 1.** Typical coexistence rather than competition: HAProxy at the edge, Nginx in front of applications, Envoy between services inside a mesh.

## Choosing in an interview answer

A load-balancing-only tier with brutal connection throughput — HAProxy. Serving static assets, terminating TLS for a web app, reverse-proxying into application servers — Nginx. A polyglot microservice fleet that needs uniform retries, timeouts, mTLS, and observability without touching each service — Envoy as the sidecar (this is exactly the niche Istio fills), or as an edge proxy reusing the same configuration model; the sidecar pattern also changes how [[How does service discovery work in Kubernetes]] gets answered, because the mesh, not the application, watches endpoints. The roles genuinely overlap — all three can terminate TLS and balance HTTP/2 — so the honest answer names the workload first and the tool second.

```text
# Conceptual HAProxy edge load balancer
frontend fe
    bind :443 ssl crt /etc/haproxy/certs
    default_backend apps
backend apps
    balance roundrobin
    server app1 app1:8080 check
    server app2 app2:8080 check
```

**Listing 1.** HAProxy in its edge role: TLS termination on the frontend, connection-level balancing with health checks on the backend.

> [!warning] Three factual traps
> "Nginx cannot proxy raw TCP" is outdated — the stream module handles TCP and UDP sessions. "HAProxy can also serve static files" is flat wrong per its own documentation — it is not a web server by design. "Envoy is only a sidecar" undercounts its edge-proxy role. The deepest trap is arguing about products when the question is about layers: connection-level versus request-level balancing decisions (HAProxy TCP vs HTTP mode) is the distinction interviewers usually probe, and it maps onto [[How do you achieve server-side load balancing with Spring Cloud]] at the client-side end of the same spectrum.

> [!tip] Interview answer
> **HAProxy is a pure TCP/HTTP load balancer — per-connection in TCP mode, per-request in HTTP mode — with normalization, SSL termination, and rate limiting, and nothing else: no static files, no packet NAT. Nginx is a web server first: static content, caching, reverse proxy, plus HTTP load balancing and a stream module for TCP/UDP. Envoy is the service-mesh proxy: out-of-process, dynamically configured via xDS, HTTP/2- and gRPC-first, with outlier detection, retries, and tracing built in. Choose by role: edge LB, web front, or mesh sidecar.**
