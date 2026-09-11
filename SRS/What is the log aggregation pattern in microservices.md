<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the log aggregation pattern in microservices

> [!abstract] Short answer
> The log aggregation pattern collects the logs of every service instance into one central store with a unified format and queryable index: instead of SSH-ing into N hosts to grep N files, operators and developers query one system across the whole fleet, filtered by service, time, level and correlation id. Richardson's observability pattern; ELK-class stacks are the canonical implementation.

## The mechanics: emit, collect, index, query

Four stages. Emit: services write structured, one-event-per-line logs to stdout/stderr (the container-platform convention) with consistent fields — timestamp, level, service, instance, correlation id ([[What is the distributed tracing pattern in microservices]] makes that id the join key to traces; the emitting convention governs what the lines contain). Collect: a per-host agent (Filebeat/Fluentd-class) or the platform's collector tails and ships the streams — crucially without the application knowing about storage. Index and store: the pipeline parses, normalizes and indexes into a searchable store with retention tiers (hot search, cold archive). Query and visualize: full-text and field-scoped queries across services; dashboards for error rates and latency narratives; saved queries for known failure modes. The aggregation layer is also where the fleet gets uniformity for free: one parsing config, one PII scrubbing rule, one retention policy — instead of per-service discipline ([[What is the microservice chassis pattern]] standardizes the emitting side).

```d2
direction: down
s1: "orders
stdout: JSON lines" {style.fill: "#e8f5e9"}
s2: "inventory
stdout: JSON lines" {style.fill: "#e8f5e9"}
s3: "gateway
stdout: JSON lines" {style.fill: "#e8f5e9"}
ag: "Agent / collector
per host" {style.fill: "#e3f2fd"}
idx: "Central store
indexed, retention tiers" {shape: cylinder; style.fill: "#fff3e0"}
q: "Query: trace=tr-42 across all services" {style.fill: "#f3e5f5"}
s1 -> ag
s2 -> ag
s3 -> ag
ag -> idx
idx -> q
```

**Fig. 1.** Every instance's stdout flows through collectors into one indexed store; queries span the fleet by correlation id.

## The disciplines that make aggregated logs usable

Structured over human-readable: free-text lines defeat field queries and cross-service correlation; JSON lines with a stable schema are the working default, with the message staying greppable. Correlation as schema: every line carries the trace/request id so one query reconstructs a request's journey across services — this is the single highest-leverage convention in the whole pattern. Volume economics: debug logging at scale is a cost problem — level discipline per environment, sampling for chatty paths, and retention tiers (hot days, warm weeks, cold archive) keep the system affordable; the aggregation layer must never be the thing that falls over under an error storm (backpressure, drop policies). Security and hygiene: logs leak — tokens, headers, PII end up in messages; scrub at emission, restrict read access, and remember that aggregated logs concentrate what was previously scattered, raising both their usefulness and their sensitivity ([[What is the audit logging pattern in microservices]] is the deliberately separate trail for user-driven changes; [[What is the centralized exception tracking pattern in microservices]] is the issue-oriented view over the same events).

> [!warning] Aggregation turns log loss from a per-host annoyance into a fleet-wide blind spot
> When the collector queue saturates or the pipeline falls behind, the system keeps serving while its memory does not — and the outage investigation happens against the very pipeline that was saturated. Design the collection path for backpressure and explicit drop accounting, alert on pipeline lag as a first-class signal, and never let a log shipper be on the synchronous critical path of a request.

> [!tip] Interview answer
> Log aggregation ships every instance's structured stdout through collectors into one indexed, queryable store with retention tiers — one place to ask across the fleet instead of grepping N hosts. The conventions that make it work: JSON lines with a stable schema, a correlation id on every line as the join key to traces, level and volume discipline so an error storm doesn't bankrupt the pipeline, and PII scrubbing at emission. I also watch the pipeline itself — collection lag is a first-class alert.
