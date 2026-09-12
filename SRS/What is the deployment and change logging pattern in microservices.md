<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/Observability #SRS

# What is the deployment and change logging pattern in microservices

> [!abstract] Short answer
> The deployment and change logging pattern records every change to the running system — deploys, configuration changes, infrastructure moves, feature-flag flips — into a central, machine-readable log, so the operational history answers "what changed, when, by whom" in one queryable place. An observability pattern; its core use is correlation: a metric anomaly or error spike is almost always explained by a change visible in this log.

## The mechanics: every change is an event

The pattern turns change management into event sourcing for operations. Each change emits a record: what changed (service, version/artifact digest, configuration diff or version, feature flags, infrastructure), when (trusted timestamp), who/what (pipeline run, operator, automation), and where (environment, cluster, zone). Sources are wired at the actuator level — CI/CD pipelines emit on deploy, the config service emits on applied changes ([[What is the externalized configuration pattern for microservices]]), the platform emits on scaling and rescheduling — not gathered later by hand. The store is append-only and queryable by service and time. The payoff is in the joins: dashboards overlay deploy markers on latency graphs; alert runbooks start with "what changed in the last hour"; incident timelines assemble from the change log rather than memory ([[What is the application metrics pattern in microservices]] supplies the curves; this log supplies the annotations that explain them).

```d2
direction: down
ci: "CI/CD
deploy v2.4.0" {style.fill: "#e8f5e9"}
cfg: "Config service
applied diff #331" {style.fill: "#e3f2fd"}
ops: "Platform
scaled orders 3->5" {style.fill: "#e3f2fd"}
cl: "Change log
who / what / when / where" {shape: cylinder; style.fill: "#fff3e0"}
dash: "Dashboards + incident review
deploy markers over metrics" {style.fill: "#f3e5f5"}
ci -> cl
cfg -> cl
ops -> cl
cl -> dash
```

**Fig. 1.** Every actor that changes the system emits to one log; dashboards and incident reviews join it against operational metrics.

## Why it must be machine-readable and complete

The value is automated correlation, so the log's consumers are programs: dashboards query it, alert pipelines attach recent changes to notifications, rollback tooling reads it to find the last known-good artifact. Two disciplines keep it authoritative. Completeness at the source: anything that can alter behavior without appearing in the log — manual hotfixes, direct database changes, flag toggles — turns the history into fiction; the plumbing must cover the human paths too (change ticket IDs, audited admin actions, [[What is the audit logging pattern in microservices]] for user-level changes). Honest versioning: record artifact digests, not just tag names — reproducibility and provenance in incident forensics come from digests, and the same registry that serves the artifact should back the claim ([[What is the service per container pattern]] makes digests natural — immutable images have them).

> [!warning] "We'll reconstruct it from git" fails in the incident
> Source control says what was intended; the change log says what is actually running where — and they diverge exactly when things break: failed deploys, manual interventions, rolled-forward rollbacks, config applied out of band. If assembling the operational history requires human memory at 3 a.m., the pattern is missing, and mean-time-to-recovery pays for it.

> [!tip] Interview answer
> Deployment and change logging makes every operational change an event — deploys with artifact digests, config versions, flag flips, scaling actions — written centrally by the actors themselves: pipelines, config service, platform. It's machine-readable so dashboards overlay deploys on metrics, alerts carry recent changes, and incident timelines assemble from facts. Completeness is the hard part: manual hotfixes and out-of-band changes must be captured too, or the history lies exactly when you need it.
