<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the centralized exception tracking pattern in microservices

> [!abstract] Short answer
> The centralized exception tracking pattern collects every exception from every service into one system that deduplicates, groups and counts them — so each distinct problem becomes one tracked item with a stack trace, metadata and a trend, rather than a needle in a thousand log lines. Richardson's observability pattern; the canonical category is Sentry-class tools (Raven/DSN clients), distinct from log aggregation in purpose and data model.

## Why grep is not exception tracking

Application logs hold exceptions, but log-oriented storage answers poorly: exceptions repeat (one bug can produce a million identical lines), interpolate differently per occurrence (ids in messages break naive grouping), and lack the cross-service view. A tracker changes the data model: an exception arrives with its type, message, stack frames, service, release version, environment, request metadata and correlation id; the tracker fingerprints it (type plus normalized stack) into one issue and increments its counter. The result: a ranked list of distinct problems with first/last seen, affected releases and trend — the questions triage actually asks. Correlation ids carried from the request ([[What is the distributed tracing pattern in microservices]]) turn a tracked exception into a jump point into the full trace; release tagging turns "it started failing" into a deploy-linked fact ([[What is the deployment and change logging pattern in microservices]]).

```d2
direction: down
s1: "Service A
exception + metadata" {style.fill: "#e8f5e9"}
s2: "Service B
exception + metadata" {style.fill: "#e8f5e9"}
s3: "Service C
exception + metadata" {style.fill: "#e8f5e9"}
tr: "Tracker
fingerprint -> issue" {style.fill: "#fff3e0"}
iss: "Issue NPE at OrderMapper.map
count 14,203 · since v2.4.0" {style.fill: "#ef9a9a"}
s1 -> tr
s2 -> tr
s3 -> tr
tr -> iss: deduplicate + count
```

**Fig. 1.** Many services, many occurrences, one issue: fingerprinting collapses noise into a ranked, trended list.

## The mechanics that decide its usefulness

Capture with context: the hook must run at the outermost boundary per service (an exception-handler filter or the chassis' error path, [[What is the microservice chassis pattern]]), capture the stack with symbol names intact, and attach the request's identity: correlation id, user role (not PII), release version. Volume control: sampling or rate limiting per fingerprint — an outage storm must not become a tracker outage; and the pipeline is best-effort by design — losing a tracker event must never break the business request (unlike the audit log, [[What is the audit logging pattern in microservices]]). Grouping hygiene: fingerprints normalize volatile parts (ids, paths, line-level shifts between releases), because both failure modes hurt — one bug split into twenty issues hides its size, and two distinct bugs merged into one issue hide one of them. The end state Richardson implies: exception tracking is the triage surface — what is new, what is spiking, what shipped broken — while aggregated error metrics ([[What is the application metrics pattern in microservices]]) watch the rates and logs keep the narrative context.

> [!warning] An exception tracker with access to sensitive payloads is a data leak with a UI
> Exceptions routinely swallow request bodies, tokens and PII into their messages and local variables. A tracker that captures everything creates a searchable store of secrets — with weaker access control than the database the data came from. Scrub at capture (deny-list known-sensitive fields), scope read access, and treat tracker URLs as secret-bearing: their shareable links have leaked tokens more than once.

> [!tip] Interview answer
> Centralized exception tracking pulls every exception from every service into one system that fingerprints and groups them: each distinct problem becomes one issue with stack, metadata, release and trend — instead of scattered log lines. The hooks live at each service's outermost error boundary and carry correlation ids and release tags, so an issue links to its trace and to the deploy that introduced it. It's best-effort by design — sampled and rate-limited — and it must scrub sensitive payload data at capture.
