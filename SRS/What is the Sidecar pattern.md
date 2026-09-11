<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Sidecar #Patterns/DistributedSystems #SRS

# What is the Sidecar pattern

> [!abstract] Short answer
> The sidecar pattern deploys a helper process alongside each service instance — same host or pod, same lifecycle — to implement cross-cutting concerns without touching the service's code: TLS and token handling, retries and logging, configuration sync, telemetry. The service talks to its sidecar over localhost; the sidecar talks to the world. Kubernetes' native sidecar concept and service-mesh proxies (Envoy) are the mainstream instances.

## Mechanics: same lifecycle, localhost contract

The sidecar is collocated on purpose: same pod means shared localhost, shared volumes and — crucially — one lifecycle (deployed, scaled and health-checked together). The division of labor: the sidecar owns everything that should be uniform across the fleet and independent of the service's language; the service owns its business logic. Traffic may flow through it (proxy mode: all in/out traffic passes the sidecar — the mesh's data plane, [[How would you explain the service mesh pattern]]) or alongside it (ambassador/adapter mode: the app consciously calls the sidecar for specific duties — a config-sync agent, a credential refresher, a log shipper). Because the contract is localhost networking and files, the sidecar can be a different language, upgraded on its own schedule and reused across the fleet ([[What is the microservice chassis pattern]] is the library-based alternative — chassis inside the process, sidecar outside it).

```d2
direction: right
pod: "Pod / host" {style.fill: "#eceff1"}
app: "Service
business logic only" {style.fill: "#e8f5e9"}
sc: "Sidecar
retry, mTLS, trace, ship logs" {style.fill: "#e3f2fd"}
world: "Network" {shape: cloud; style.fill: "#fffde7"}
app -> sc: localhost
sc -> world: policy enforced
world -> sc
sc -> app
```

**Fig. 1.** One instance, two processes: the service sees only localhost; the sidecar carries policy to and from the network.

```java
// sidecar proxy: same runtime host as the app (localhost), adds retry + tracing
String traceId = "trace-" + ++traceCounter;
for (int attempt = 1; attempt <= 2; attempt++) {
    resp = client.send(HttpRequest.newBuilder(
            URI.create("http://127.0.0.1:18105" + ex.getRequestURI().getPath())).build(),
            HttpResponse.BodyHandlers.ofByteArray());
    if (resp.statusCode() < 500) break;
    System.out.println("sidecar: " + traceId + " attempt " + attempt + " got " + resp.statusCode() + ", retrying");
}
ex.getResponseHeaders().set("X-Trace-Id", traceId);
```

**Listing 1.** Verified on JDK 21 (G11_SidecarHttp in empirics): the app calls only `localhost:18104`; the sidecar's first upstream attempt gets `500`, it retries once, returns the final `200` and injects `X-Trace-Id` — retry and trace policy live entirely outside the app (out/G11_SidecarHttp.txt).

## Costs and boundaries of the pattern

Resources: every instance pays the sidecar's CPU and memory — at fleet scale that is real money, which is why proxy sidecars are tuned relentlessly. Latency: proxy mode adds two loopback hops and proxy processing to every call. Complexity budget: another deployable per instance to version and upgrade (and historically, to start before the app — the init/ordering problem Kubernetes solved with native sidecar containers). The boundary rule keeps it sane: a sidecar must be reusable across languages and teams — the moment it encodes one service's business rules it is not a sidecar anymore, it is a second service and should be owned and deployed like one. Sidecar versus library versus mesh is a spectrum of the same concerns: library (chassis) is cheapest at runtime but per-language; sidecar is uniform and language-agnostic at per-instance cost; mesh is sidecars plus a control plane for fleet-wide policy.

> [!warning] Sidecar and app must not share fate blindly
> Collocation is a lifecycle contract, not a safety property: a sidecar crash can take the pod's traffic down with it, and a sidecar upgrade can break an app that quietly depended on its old behavior. Both processes need their own health checks, resource limits and startup ordering — and the app needs an explicit degradation path for "sidecar is down", not an implicit hang.

> [!tip] Interview answer
> A sidecar is a helper process deployed with every service instance — same pod, same lifecycle, reachable over localhost — that owns cross-cutting duties out of band: TLS, retries, tracing, log shipping, config sync. The service stays business-logic-only, and the concern becomes uniform across languages. I pay per-instance resources and latency for that, and I keep the contract strict: generic and reusable, or it's not a sidecar — it's a second service.
