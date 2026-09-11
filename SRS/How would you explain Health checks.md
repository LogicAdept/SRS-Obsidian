<!--
reps: 0
priority: 0
-->
#SystemDesign #SRS

# How would you explain Health checks

> [!abstract] Short answer
> A health check is the load balancer's (or orchestrator's) probe deciding whether an instance should receive traffic: active checks poll an endpoint on a schedule (HTTP GET /health, TCP connect) with configured intervals and thresholds; passive checks judge by observed results of real traffic (error rates, connection failures). HealthyThreshold/UnhealthyThreshold counts prevent flap — an instance must pass or fail N consecutive probes before its status changes.

## Active probes and their thresholds

An active check is configured with a path or port, an interval, a timeout, success/failure codes, and consecutive counts. AWS ALB's model names them exactly: HealthCheckIntervalSeconds (default 30 seconds for instance/ip targets), HealthCheckTimeoutSeconds (default 5), HealthCheckPath (default /), and the router marks a target healthy after HealthyThresholdCount consecutive successes or unhealthy after UnhealthyThresholdCount consecutive failures — the counts are the anti-flap mechanism, so one lost packet or one GC pause does not eject an instance from rotation. The semantics of the endpoint decide whether the check is meaningful: a liveness check (process up, TCP accepts) says the instance exists; a readiness check (dependencies reachable, pool warm, migrations done) says it can actually serve — AWS supports status-code matching precisely so apps can expose 200-when-ready, 503-when-draining. The deeper design rule: check what would actually fail, cheaply. A check that queries the whole dependency graph on every probe turns monitoring into load; a check that never exercises the database reports healthy until a user does. [[How do you monitor database health and load]] and Spring's Actuator health aggregation ([[How does the Actuator health endpoint aggregate status]], [[How do you write a custom HealthIndicator in Spring Boot]]) show how an application composes its own readiness signal.

```text
active:   GET /health every 30s, timeout 5s
          2 consecutive failures -> unhealthy (out of rotation)
          5 consecutive successes -> healthy  (back in rotation)
passive:  real requests' errors counted (outlier ejection)
endpoint: 200 = serving; 503 = draining/not ready (readiness)
```

**Listing 1.** Probe parameters and the anti-flap thresholds.

## Passive checks and the closing loop

Passive detection complements polling: instead of (or besides) probing, the balancer counts outcomes of real requests — a target returning errors or timing out accumulates strikes and is ejected — which catches failures an endpoint may not report about itself (a check that lies, a dependency failing per-request). In microservice meshes the same logic runs per-hop (outlier detection), and application-level adaptive throttling (Google SRE's handling-overload chapter) is the server-side continuation: the server itself sheds when it knows it is unhealthy. Health checks also drive lifecycle: an instance that starts failing goes out of rotation ([[How do you protect a slower downstream service from overload]] uses the same signal for protection), and a leaving instance must finish in-flight work first — [[How would you explain Connection draining]] is the companion mechanism. Sticky-session deployments tie the two together: [[How would you explain Sticky sessions]] plus health checks decide both where a user goes and whether they must move.

> [!warning] A health check that cannot fail is decoration
> A /health endpoint returning hardcoded 200 keeps a broken instance in rotation — the LB reports green while users see errors. The check must exercise the real serving path (dependencies, pools) at acceptable probe cost, or it monitors nothing.

> [!tip] Interview answer
> Health checks are the probes routing traffic only to capable instances: active polling of a health endpoint with interval, timeout and consecutive success/failure thresholds to prevent flapping, plus passive counting of real-traffic errors. I separate liveness from readiness — a 503 readiness signal during startup or draining keeps the balancer honest.
