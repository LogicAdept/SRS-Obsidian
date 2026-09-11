<!--
reps: 0
priority: 0
-->
#Observability #Patterns/Architecture/Microservices/Observability #SRS

# What are tracing spans and OpenTracing

> [!abstract] Short answer
> A tracing span is one timed operation inside a distributed trace: a named, attributed record with a span id, its parent span id, the shared trace id, start/end timestamps and outcome — the atomic unit of distributed tracing. OpenTracing was the vendor-neutral API for spans that merged with OpenCensus in 2019 into OpenTelemetry, which is now the standard instrumentation framework — OpenTracing itself is archived and should no longer be adopted.

## The span data model

A span is the tree node that traces are built from. Its fixed fields: trace id (shared by every span of one request's journey), span id (unique per operation), parent span id (which makes the trace a tree — the root span is the request's entry), operation name, start timestamp and duration, and attributes/tags (service name, HTTP route, status, error flags — standardized names in OpenTelemetry's semantic conventions). Spans may carry logs/events (timestamped points inside the span — "cache miss", "retry issued") and, historically, baggage: a small key-value map propagated with the trace context. The consumer view reassembles spans into a waterfall: where the request went, how long each hop took, which hop errored ([[What is the distributed tracing pattern in microservices]] is the system-level pattern; the span is its data structure).

```d2
direction: down
root: "span: gateway.handle
trace tr-42, parent -" {style.fill: "#e3f2fd"}
o: "span: orders.create
parent = gateway" {style.fill: "#e8f5e9"}
q: "span: orders.db.query
parent = orders" {style.fill: "#f3e5f5"}
i: "span: inventory.reserve
parent = orders" {style.fill: "#e8f5e9"}
root -> o
o -> q
o -> i
```

**Fig. 1.** Spans form a tree via parent ids: one trace id, per-span ids, parent links — the waterfall is derived, not stored as such.

## OpenTracing to OpenTelemetry — the history that interviews ask about

OpenTracing (CNCF, 2016) defined the vendor-neutral span/trace API — start a span, inject/extract context into carriers, finish the span — with implementations plugging into Zipkin, Jaeger and others. The friction: two CNCF projects did overlapping work (OpenTracing's API vs OpenCensus' agent-plus-libraries), every language had two ecosystems, and vendors had to support both. In May 2019 the projects merged into OpenTelemetry: one project combining the API, SDKs per language, the OTLP wire protocol, collector and semantic conventions — covering traces first, then metrics and logs as the "three pillars" under one data model. OpenTracing is archived; its API survives as a compatibility shim. The migration consequence for codebases: span-producing code written against OpenTracing keeps working through bridges, but new instrumentation targets the OpenTelemetry API, and propagation follows W3C Trace Context headers rather than the old B3 default ([[What is the microservice chassis pattern]] is where the OTel SDK usually gets wired).

> [!warning] A span without context propagation is a stranger in the backend
> The data model is trivial; the hard part is the same as the pattern level: every hop must carry the trace context, or the backend stores well-formed spans that never assemble into a trace. The second classic defect is cardinality in attributes — user ids, raw URLs — turning span storage into the metrics-system cost problem at a larger scale ([[What is the application metrics pattern in microservices]] has the same rule, and the same blast radius).

> [!tip] Interview answer
> A span is the atomic unit of a distributed trace: operation name, trace id shared across the journey, its own span id, parent span id, timings and attributes — spans form a tree that the backend renders as a waterfall. OpenTracing was the vendor-neutral API for that model; it merged with OpenCensus into OpenTelemetry in 2019, which is now the standard — API, SDKs, OTLP, collector and semantic conventions across traces, metrics and logs. New code targets OTel; OpenTracing is archived history, but the span model it defined is the same.
