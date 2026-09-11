<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the health check API pattern

> [!abstract] Short answer
> The health check API pattern: every service exposes an endpoint (HTTP `/health` being the default shape) that reports whether the instance is actually able to handle requests — checking its critical dependencies (database connections, brokers, disk) rather than just process liveness. Monitoring, load balancers, registries and orchestrators poll it; a failed check stops routing and triggers alerts or restarts.

## Liveness versus readiness — the distinction that makes the pattern work

The endpoint's meaning must be precise or the platform's decisions go wrong. Liveness: is the process alive and able to run — a failing liveness check should restart the instance (a deadlock, a corrupted heap). Readiness: can this instance handle a request right now — dependencies reachable, connection pool warm, not still booting; a failing readiness check should remove the instance from load balancing without restarting it (the restart would not help a down database, and would add a stampede when everything comes back). Conflating them produces the classic failure: an instance whose dependency is down gets killed and restarted forever instead of being pulled from rotation. The checks themselves: connection pings with tight timeouts, host resources (disk space), and application-specific invariants — but a check must answer quickly and cheaply, because monitoring polls it continuously and every dependency check is itself a load ([[What is the application metrics pattern in microservices]] records check outcomes as series; the platform acts on the instant answer).

```d2
direction: down
hc: "Health endpoint
/health" {style.fill: "#e3f2fd"}
db: "DB connection check" {style.fill: "#e8f5e9"}
br: "Broker check" {style.fill: "#e8f5e9"}
lb: "LB / registry: route?" {style.fill: "#fff3e0"}
orch: "Orchestrator: restart?" {style.fill: "#f3e5f5"}
hc -> db
hc -> br
hc -> lb: readiness verdict
hc -> orch: liveness verdict
```

**Fig. 1.** One endpoint, two verdicts: the load balancer acts on readiness, the orchestrator on liveness.

```java
boolean allUp = db.status() == Status.UP && broker.status() == Status.UP;
String body = "{"status":"" + (allUp ? "UP" : "DOWN")
        + "","checks":[{"name":"inventory-db","status":"" + db.status() + ""},...]}";
send(ex, allUp ? 200 : 503, body);
```

**Listing 1.** Verified on JDK 21 (G13_HealthCheckHttp in empirics): with both dependencies up the endpoint answers `200 {"status":"UP",...}`; after the db flag flips, `503 {"status":"DOWN",...}` with the failing check named — the payload tells the platform not just if but why (out/G13_HealthCheckHttp.txt).

## Fleet wiring and the traps

Consumers: the monitoring system alerts on failures and trends; load balancers and registries gate routing on readiness ([[How would you explain the service registry pattern]] — heartbeats and health checks compose); orchestrators restart on liveness failures. The trap set is well known: cascading restarts (every instance restarts on a shared dependency's failure — add jitter and dependency-scoped semantics); health checks that pass while the app is unusable (process alive, connection pool exhausted — check depth, not just reachability); and checks heavier than production traffic (deep probes at 1-second intervals are a DDoS from your own monitoring). Spring Boot Actuator's `/health` is Richardson's canonical example of the pattern shipped as part of the chassis ([[What is the microservice chassis pattern]]), and on orchestrators the probe configuration (liveness/readiness/startup paths, timings) is where the pattern's semantics get encoded.

> [!warning] A health endpoint that lies is worse than no health endpoint
> The endpoint's answer drives automated action: routing away, restarts, traffic shifts. A check that always returns UP hides outages from the platform; a check that flaps causes restart storms and routing flapping. Verify the semantics per dependency (can this instance still serve if the check fails?), keep checks cheap and deterministic, and alert on check flapping itself — it is its own failure signal.

> [!tip] Interview answer
> Each service exposes a health endpoint whose checks cover its critical dependencies — connection pools, brokers, disk — and the platform's consumers act on it with different semantics: readiness failures pull the instance from routing, liveness failures trigger restart, and they must not be conflated or a dead dependency causes restart storms. Checks are cheap, deterministic, jittered, and return the failing component so the payload says why. Actuator's /health or the orchestrator's probes are this pattern, packaged.
