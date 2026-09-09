<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What health checks does Quarkus expose?

> [!abstract] Short answer
> The `quarkus-smallrye-health` extension implements MicroProfile Health over three endpoints: **`/q/health/live`** (is the process up — liveness), **`/q/health/ready`** (can it serve — readiness) and **`/q/health/started`** (has it started), with `/q/health` accumulating everything. Extensions register built-in checks automatically — database connections (Agroal), Reactive Messaging connectivity — and you add custom checks by implementing `HealthCheck` annotated `@Liveness` or `@Readiness`. When `quarkus-kubernetes` is present, generated manifests wire these endpoints into the pod's liveness/readiness/startup probes.

## Endpoints, semantics, built-in checks

The three URL groups exist because Kubernetes treats failure differently: liveness failure triggers a container **restart**, readiness failure only removes the pod from Service load balancing, startup failure during boot delays the readiness gate. Built-in checks arrive from whatever extensions are installed: the datasource extension publishes "Database connections health check" per datasource (pool borrow test), Reactive Messaging publishes liveness/readiness for each channel's connector state — the verified app's `/q/health` output contained both, plus a custom one. Custom checks implement `HealthCheck` and return a named `HealthCheckResponse` (up/down with data); custom groups (`@HealthGroup("release")`) add separate URLs for deployment-specific gating.

```java
// src/main/java/org/acme/check/infra/CustomReadiness.java (JDK 21, Quarkus 3.39.2).
package org.acme.check.infra;

import jakarta.enterprise.context.ApplicationScoped;
import org.eclipse.microprofile.health.HealthCheck;
import org.eclipse.microprofile.health.HealthCheckResponse;
import org.eclipse.microprofile.health.Readiness;

@Readiness
@ApplicationScoped
public class CustomReadiness implements HealthCheck {
    @Override
    public HealthCheckResponse call() {
        return HealthCheckResponse.named("warmup").up().withData("phase", "done").build();
    }
}
// Boot of the fast-jar, GET /q/health (verbatim fragment):
// {
//     "status": "UP",
//     "checks": [ {
//         "name": "SmallRye Reactive Messaging - liveness check",   "status": "UP"
//     }, {
//         "name": "Database connections health check",              "status": "UP",
//         "data": { "<default>": "UP" }
//     }, {
//         "name": "warmup",                                         "status": "UP",
//         "data": { "phase": "done" }
//     }, ... ]
// }
// GET /q/health/ready -> 200 {"status":"UP", ...}   (asserted in the test run, 6/6 green)
```

**Listing 1.** One custom readiness check named "warmup" appears beside the automatic datasource and messaging checks — extension-provided and user-provided checks aggregate into one document ([[Which connection pool does Quarkus use]], [[How does reactive messaging work in Quarkus]]).

```d2
direction: down
k8s: "Kubernetes probes\nliveness | readiness | startup" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
urls: "/q/health/live | /q/health/ready | /q/health/started\n/q/health = all" {
  width: 400
  height: 65
  style.fill: "#e3f2fd"
}
auto: "Built-in checks\nAgroal datasource, messaging connectors" {
  width: 320
  height: 65
  style.fill: "#fff3e0"
}
custom: "Custom HealthCheck\n@Liveness / @Readiness / @HealthGroup" {
  width: 330
  height: 65
  style.fill: "#e8f5e9"
}
k8s -> urls
auto -> urls
custom -> urls
```

**Fig. 1.** Three probe semantics on top of one aggregation point; automatic and custom checks merge into the same document the probes poll ([[How does Quarkus deploy to Kubernetes]]).

## Choosing liveness vs readiness — the interview favorite

A dependency outage (database unreachable, broker disconnected) is a **readiness** matter: the pod cannot serve usefully right now, but restarting it would not help — flip it out of rotation instead. A process-level fault (deadlocked heap, corrupted state) is **liveness** territory: restart is the remedy. Putting database connectivity into liveness is the classic anti-pattern that turns a short database blip into a fleet-wide restart storm. The `started` probe covers slow-starting applications where the readiness endpoint only becomes meaningful after initialization.

> [!warning] A DOWN liveness check is a self-inflicted restart loop
> Anything flaky you register as `@Liveness` — external service pings, rate-limited downstreams — makes Kubernetes kill the container exactly when the system is already stressed, and every replica restarts in lockstep. The mirrored trap: forgetting `quarkus-smallrye-health` is what *creates* the endpoints — without the extension `/q/health` returns 404, and generated Kubernetes manifests keep polling a path that does not exist. Health checks must stay cheap and local: an expensive check on every probe interval is its own denial-of-service.

> [!tip] Interview answer
> Quarkus implements MicroProfile Health: /q/health/live for liveness, /q/health/ready for readiness, /q/health/started for the startup gate, all aggregated at /q/health. Extensions register built-ins automatically — I saw the database pool check and Reactive Messaging connector checks in a live run — and custom checks are HealthCheck beans annotated @Liveness or @Readiness. The design rule I state: dependencies belong in readiness, not liveness, because liveness failure restarts the pod; and quarkus-kubernetes wires these URLs straight into the generated probes.
