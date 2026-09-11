<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the application metrics pattern in microservices

> [!abstract] Short answer
> The application metrics pattern instruments every service to publish counters, gauges and timers about what it is doing — request rates, error rates, latencies (ideally as percentiles), resource usage, business counts — and exposes them in a scrapeable or pushable format for a central metrics system. Richardson lists it among the observability patterns; it answers "how is the system behaving right now and over time", which logs alone cannot.

## The mechanics: instrument, aggregate, expose

Three layers. Instrumentation: the service records measurements at meaningful boundaries — every inbound and outbound call gets at least a count and a duration; business events (orders placed, payments retried) get counters; queues get gauges. The standard dimension model is name plus label set (e.g. `requests_total{service="orders",route="/orders/:id"}`) — labels carry low-cardinality structure; putting ids or timestamps into labels is the classic mistake that explodes the series count. Exposure: a metrics endpoint in a standard text or binary format (Prometheus exposition being the lingua franca) that a collector scrapes, or a push agent in environments without pull. Storage and alerting: the backend stores time series, computes rates and percentiles, and drives dashboards and alerts (the records behind [[What is the log aggregation pattern in microservices]] explain individual events; metrics show the shape of events over time).

```d2
direction: right
s1: "Service A
counters, timers" {style.fill: "#e8f5e9"}
s2: "Service B
counters, timers" {style.fill: "#e8f5e9"}
sc: "Metrics endpoint
/metrics" {style.fill: "#e3f2fd"}
col: "Collector
scrape every Ns" {style.fill: "#fff3e0"}
ts: "Time-series DB
+ dashboards + alerts" {shape: cylinder; style.fill: "#f3e5f5"}
s1 -> sc
s2 -> sc
sc -> col
col -> ts
```

**Fig. 1.** Every service exposes its own numbers; the collector scrapes them into one time-series store.

```java
void inc(String name) { counters.merge(name, 1L, Long::sum); }
void time(String name, long ms) { timers.computeIfAbsent(name, k -> new ArrayList<>()).add(ms); }
// endpoint prints Prometheus-style text:
// # TYPE requests_total{service="orders"} counter
// requests_total{service="orders"} 1
// latency_ms{service="orders"}{quantile=0.5} 23
```

**Listing 1.** Verified on JDK 21 (G12_ObservabilityCorrelation in empirics): three instrumented stages emit per-service counters and latency summaries in Prometheus text format — one series per service with a median and count (out/G12_ObservabilityCorrelation.txt).

## The metrics that actually pay: the RED method

For every service, three series are the floor: Rate (requests per second), Errors (failed requests per second), Duration (latency distribution — p50, p95, p99, not the mean; means hide the tail where users live). Derived signals — saturation (queue depths, thread pools, connection pools), resource gauges (heap, GC time, file descriptors) — explain what RED reveals. Two disciplines make fleet metrics trustworthy: uniform naming and labels across services (a chassis or mesh provides this once for everyone, [[What is the microservice chassis pattern]]; a mesh exports traffic metrics without any instrumentation, [[How would you explain the service mesh pattern]]), and cardinality budgeting — every extra label multiplies stored series by its value count. Metrics are aggregates: they say "p99 is two seconds", and tracing picks the individual offenders ([[What is the distributed tracing pattern in microservices]]).

> [!warning] Averages and unbounded labels lie
> An average latency of 120ms is compatible with 5% of users waiting four seconds — decisions made on means are decisions made without the tail; always look at percentiles. And one high-cardinality label (user id, full URL) turns a flat series count into millions of singleton series, which is how teams discover their metrics system's cost curve — usually during an outage of the metrics system itself.

> [!tip] Interview answer
> The metrics pattern instruments each service with counters, gauges and timers — RED per service: request rate, error rate, duration as percentiles — and exposes them in a scrapeable format for a central time-series backend that drives dashboards and alerts. The discipline that makes it work fleet-wide: uniform naming via chassis or mesh, low-cardinality labels, and p99 instead of means. Logs explain single events; metrics give the behavioral shape over time.
