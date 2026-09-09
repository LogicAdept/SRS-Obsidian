<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft decision cues: serverless/CLI/batch where cold start and RSS dominate; Kubernetes deployments where memory density matters (more pods per node, scale-to-zero with Knative); long-lived JVM services are also fine thanks to live reload.
Team/ecosystem gravity: if the team is deep in Spring (Security, Batch, custom starters, contract ecosystem) and has no startup/memory pressure, Boot remains the lower-friction choice.
Standards angle: Quarkus leans on Jakarta specs + MicroProfile; Spring-specific modules (e.g. Spring Security's filter chain richness) have Quarkus counterparts but differ in shape.
Migration reality: Quarkus offers a Spring API compatibility layer (spring-di, spring-web, spring-data-jpa) but it is partial; plan real porting effort for deep Spring usage.
Honest answer shape: name the constraint (startup, memory, native, K8s density) and pick the framework that matches; do not claim Quarkus "replaces" Boot everywhere.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
