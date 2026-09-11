<!--
reps: 0
priority: 0
-->
#SystemDesign #SRS

# How would you explain Connection draining

> [!abstract] Short answer
> Connection draining (deregistration delay, graceful removal) is the practice of stopping NEW requests to a backend that is leaving rotation while letting its existing, in-flight requests finish — instead of killing connections mid-transaction. The balancer (or orchestrator) waits a configured delay (AWS ALB's deregistration timeout defaults to 300 seconds) or until active request count reaches zero, then removes the target fully. It is the difference between a deploy that is invisible and one that serves 502s.

## The lifecycle of a leaving backend

Removing an instance without draining breaks whatever it was doing: in-flight HTTP requests truncated mid-response, WebSocket connections dropped, transactions half-way through. The draining sequence is: deregister the target (or send SIGTERM to the process) → the balancer/proxy stops sending new requests to it → existing requests continue until they complete or the deregistration delay expires → the target is removed. AWS documents this as the deregistration delay: ALB waits for in-flight requests to complete before deregistering, default 300 seconds, configurable per target group (a value of zero kills immediately). The application side must cooperate — the process traps SIGTERM, stops accepting new work, finishes or safely aborts current work, and closes listeners last; k8s terminationGracePeriod and preStop hooks are the orchestrator-level expression of the same idea. Long-lived connections need explicit handling: WebSockets and gRPC streams do not "finish" like a request, so they must be actively closed or migrated at drain start, and keep-alive connection pools on the client side should detect closure and reconnect to live instances.

```text
t0    instance deregistered / SIGTERM
t0+   LB: no NEW requests routed here
      app: stops accepting; finishes in-flight requests
t0+   long-lived conns (WS/gRPC): closed or migrated now
t0+X  in-flight == 0 OR delay (default 300s) expires -> removed
before: kill -> truncated responses, 502s, broken transactions
```

**Listing 1.** The drain sequence and what it prevents.

## Draining as part of the traffic toolkit

Draining connects the other load-balancing mechanisms: health checks ([[How would you explain Health checks]]) decide when an instance must leave (failed probes or an explicit deregistration), affinity ([[How would you explain Sticky sessions]]) makes draining user-visible when sessions are instance-local — users pinned to a draining backend must re-establish session state elsewhere, which is one more argument for externalized sessions. On the service side, draining is graceful degradation under planned load shift; the unplanned counterpart is the breaker and shedding behavior of [[How do you protect a slower downstream service from overload]]. Deployment cadence is where the value shows: rolling deploys with correct draining plus readiness gates are invisible to users; without it, every deploy is a mini-outage. The timeout choice is a workload property: interactive APIs need the p99 request duration; batch or streaming endpoints need explicit migration logic because no fixed delay covers them.

> [!warning] A drain timeout cannot cover a stream that never ends
> Long-lived WebSocket or streaming connections will outlive any fixed deregistration delay. Applications must actively signal and close or migrate them at drain start — waiting out the timer just turns "graceful" into "abrupt, later".

> [!tip] Interview answer
> Connection draining means removing a backend from rotation while its in-flight work finishes: stop new requests (deregistration delay — 300s default on ALB), let current ones complete, close long-lived connections explicitly. It is what makes rolling deploys invisible; without it every deploy truncates requests and drops connections.
