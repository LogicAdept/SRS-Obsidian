<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the distributed tracing pattern in microservices

> [!abstract] Short answer
> The distributed tracing pattern records the path and timing of one request as it travels through multiple services: each external request gets a unique trace id, propagated through every hop; each service records spans — its operations' start, end and outcome — into a centralized tracing backend that reassembles them per trace id. Richardson's observability pattern; it answers "where did this request spend its time and where did it fail", which per-service logs cannot.

## The mechanics: context propagation plus span recording

Two halves. Propagation: the trace context — trace id, current span id, sampling flags — travels with the request across every protocol boundary (HTTP headers, message headers, RPC metadata); each service continues the trace and creates child spans for its outbound calls. Standardized now by W3C Trace Context and OpenTelemetry's semantic conventions ([[What are tracing spans and OpenTracing]] covers the data model and its standardization history). Recording: spans arrive at a collector and are stored indexed by trace id and attributes. The reassembled trace is a tree: gateway span containing order-service span containing db spans — with timings that localize latency (the 23ms order step inside a 2s request is not your problem; the 1.8s inventory step is) and errors that localize failures at the exact hop.

```d2
direction: down
gw: "api-gateway span
4ms" {style.fill: "#e3f2fd"}
o: "orders.createOrder span
23ms" {style.fill: "#e8f5e9"}
db: "orders.db.query
11ms" {style.fill: "#f3e5f5"}
i: "inventory.reserveStock span
9ms" {style.fill: "#e8f5e9"}
tr: "Trace tr-42 reassembled in the backend" {style.fill: "#fff3e0"}
gw -> o: child
o -> db: child
o -> i: child
o -> tr
```

**Fig. 1.** One trace id, a tree of spans: parent-child timings localize latency and failure to the exact hop.

## Instrumentation strategy and the sampling decision

Where spans come from: automatic instrumentation in the chassis or agent covers the transport edges — HTTP servers/clients, DB drivers, queue clients — without touching business code ([[What is the microservice chassis pattern]] ships it once for the fleet; a mesh records hop-level spans with zero application instrumentation, [[How would you explain the service mesh pattern]]); manual spans wrap genuinely custom operations worth seeing individually. Sampling is the design decision with teeth: recording 100% of traces is the only way to guarantee the failing request is captured — head sampling (decide at entry) at 1% means the problem request was almost certainly not recorded; tail sampling (record all errors and slow outliers, sample the healthy rest) needs the buffering infrastructure to wait and decide. Propagation discipline is non-negotiable: a service that drops the trace context starts a new root and breaks the chain — the most common instrumentation defect in polyglot fleets, and the reason context propagation belongs in shared plumbing, not per-service code ([[What is the log aggregation pattern in microservices]] complements traces — the trace id in every log line is the join key between narrative and timing).

> [!warning] A trace is only as complete as its weakest hop
> One service that neither propagates context nor records spans leaves a hole in every trace through it — the trace silently shows a 400ms gap with no explanation. And message-based hops need explicit care: the context rides in message headers, and a consumer that starts a "new" trace per message splits one business operation into unrelatable fragments. Trace completeness is a fleet property; test it the way you test authentication.

> [!tip] Interview answer
> Distributed tracing gives one request a trace id that propagates through every service and message hop; each service records spans for its operations into a central backend, which reassembles them into a parent-child tree with timings. That localizes latency and failure to the exact hop across a call graph — something per-service logs can't do. The real decisions are instrumentation coverage (agents plus mesh versus manual spans) and sampling: tail-sample to keep all errors and slow requests, and never let a service break the context chain.
