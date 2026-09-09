<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you expose metrics in Quarkus?

> [!abstract] Short answer
> Via **Micrometer** — Quarkus' recommended metrics facade: add `quarkus-micrometer-registry-prometheus` and application, JVM and pool metrics surface at **`/q/metrics`** in Prometheus text format. Base metrics arrive automatically (HTTP server dimensions, timers for endpoint latency); custom ones use the Micrometer API or annotation shortcuts — **`@Timed`, `@Counted`, `@Gauged`** — on CDI beans; other registries (OTLP, Datadog, Influx) plug in the same way. The older MicroProfile Metrics approach is deprecated in favor of Micrometer — name the successor in interviews.

## What appears without writing code

Installing the registry extension turns on a metrics layer that instruments the runtime: HTTP request counts and durations by URI/status/outcome, memory and GC through the JVM registry, plus integration metrics from other extensions — Agroal publishes connection pool gauges per datasource, Reactive Messaging and gRPC add their own ([[Which connection pool does Quarkus use]]). The endpoint responds at `/q/metrics` (path configurable) with content negotiation: Prometheus text for scrapes. In the verified fast-jar run, `GET /q/metrics` returned 200 on the prod profile — the scrape target needs no code, only the registry dependency and (in production) a Prometheus scraping the pod or ServiceMonitor if the Kubernetes extension is in play.

```java
// Custom metric on a CDI bean (the extension's documented annotation style), plus the
// Micrometer programmatic API. JDK 21, Quarkus 3.39.2.
//
// package org.acme;
//
// import io.micrometer.core.annotation.Timed;
// import io.micrometer.core.instrument.MeterRegistry;
// import jakarta.enterprise.context.ApplicationScoped;
// import jakarta.inject.Inject;
//
// @Path("/orders")
// @ApplicationScoped
// public class OrderResource {
//     @Inject MeterRegistry registry;                 // programmatic API
//
//     @POST
//     @Timed(value = "orders.create", percentiles = {0.5, 0.95})   // declarative timer
//     public String create(String body) {
//         registry.counter("orders.created", "type", "standard").increment();
//         return "ok";
//     }
// }
// (Conceptual for the annotation block; the /q/metrics endpoint itself WAS verified:
//  GET /q/metrics -> 200 on the packaged fast-jar of this deck's demo application.)
```

**Listing 1.** Marked `Conceptual` for the annotation part; the narrative: `MeterRegistry` injection covers arbitrary dimensions, `@Timed` records latency distributions, counters track events with tags — all exported by the same scrape endpoint.

```d2
direction: down
app: "Application code\n@Timed / @Counted / MeterRegistry" {
  width: 320
  height: 65
  style.fill: "#e8f5e9"
}
auto: "Automatic instrumentation\nHTTP endpoints, JVM, pools, messaging" {
  width: 340
  height: 65
  style.fill: "#fff3e0"
}
reg: "Micrometer registry\nPrometheus | OTLP | Datadog" {
  width: 320
  height: 65
  style.fill: "#e3f2fd"
}
ep: "/q/metrics\nscrape target" {
  width: 220
  height: 50
}
app -> reg
auto -> reg
reg -> ep
```

**Fig. 1.** Facade over many registries: application and runtime metrics converge into one registry selection, exposed at one endpoint ([[What health checks does Quarkus expose]] lives on the neighboring /q/ path).

## Choosing metrics that answer questions

The senior-level point is dimension discipline: tag by things you alert on (endpoint, outcome, tenant tier) and never by unbounded values (user id, request id — cardinality explosions kill Prometheus). Latency is a distribution (`@Timed` with percentiles or histograms), not an average; throughput without error-rate and saturation is the classic "green dashboard during an outage". Prometheus conventions (naming, base units) come free because the registry formats the exposition.

> [!warning] MicroProfile Metrics is yesterday's answer
> Quarkus deprecated the MicroProfile Metrics extension in favor of Micrometer — quoting `quarkus-smallrye-metrics` and `/metrics` MP-OPTIONS as current practice dates you. Two traps on the current stack: forgetting that annotations (`@Timed`) require the bean to be CDI-managed (self-invocation bypasses the interceptor, the timer silently records nothing), and enabling percentile/histogram quantiles on everything — each histogram carries memory and scrape cost, so they belong on the critical paths, not by default on all methods.

> [!tip] Interview answer
> Quarkus standardized on Micrometer: I add the prometheus registry extension and /q/metrics serves the scrape — HTTP endpoint metrics, JVM metrics and extension metrics like Agroal pools appear automatically. Custom metrics go through the injected MeterRegistry or @Timed/@Counted annotations on beans, with tags chosen for the questions we alert on and cardinality kept bounded. MicroProfile Metrics is deprecated — Micrometer is the current answer, and the same facade can export OTLP or Datadog instead of Prometheus.
