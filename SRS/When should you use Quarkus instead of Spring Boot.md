<!--
reps: 0
priority: 0
-->
#Java/Quarkus #Java/Spring/Boot #SRS

# When should you use Quarkus instead of Spring Boot?

> [!abstract] Short answer
> Decide from the **constraint, not the fashion**. Quarkus wins when **startup latency, memory density or native executables** are first-class requirements: serverless and scale-to-zero, CLI/batch tools, tightly packed Kubernetes nodes, edge workloads. Spring Boot stays the lower-friction choice when the deciding factor is **ecosystem depth and team gravity** — deep Spring Security/Batch/custom-starters usage, a large hiring pool — because on a long-running, throughput-oriented JVM service the startup difference matters little and the ecosystem difference matters a lot.

## A decision map that survives follow-ups

```d2
direction: down
q1: "Cold start or RSS\na hard requirement?" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
q: "Quarkus\nserverless, scale-to-zero,\nCLI tools, dense pods, native" {
  width: 300
  height: 85
  style.fill: "#e8f5e9"
}
q2: "Deep Spring investment?\nSecurity internals, Batch,\ncustom starters, team skills" {
  width: 300
  height: 85
  style.fill: "#fff3e0"
}
s: "Spring Boot\nlong-running JVM services,\necosystem and hiring" {
  width: 290
  height: 85
  style.fill: "#e3f2fd"
}
q1: yes -> q
q1: no -> q2
q2: yes -> s
q2: no -> q: "measure both,\nprefer standards"
```

**Fig. 1.** Neither answer is global: the same organization can run Quarkus for its cold-start-sensitive services and Boot where its Spring investment lives. The honest baseline for "no hard constraint" is to prototype one endpoint in both and measure.

## What tips each way

Toward Quarkus: sub-second JVM boot and tens-of-milliseconds native boot ([[Why does Quarkus start faster than a typical Spring Boot application]]); lower RSS lets a node host more replicas; the dev loop (live reload plus auto-provisioned dependencies) is genuinely fast ([[What are Dev Services in Quarkus]]); standards-first stack (Jakarta REST, CDI, JPA) keeps portability.

Toward Boot: the Spring catalog's specific modules are richer than their Quarkus counterparts ([[What is Spring Boot]]); a team fluent in Spring semantics ships faster than one translating to CDI Lite and ArC's subset ([[What is ArC in Quarkus]]); third-party integrations assume Spring Boot first. Quarkus' compatibility extensions (`spring-di`, `spring-web`, `spring-data-jpa`) ease migration but are explicitly partial.

```java
// The workload check that decides more than any checklist:
long running JVM service, constant traffic, no cold starts
  -> startup speed is paid once; throughput and ecosystem dominate.
Serverless function / CLI / autoscaled pod that idles and restarts
  -> startup and RSS are paid on every cold start; they dominate.
```

**Listing 1.** Conceptual rubric: the cost structure of the workload, not the framework benchmark, determines which difference is material.

> [!warning] Two wrong extremes
> "Quarkus is only for microservices/native" — false: the docs never gate it that way, and a JVM-mode monolith on Quarkus is a supported, ordinary use. "Quarkus replaces Spring Boot everywhere" — also false: partial compatibility extensions do not equal Spring's surface, and migration of deep Spring code is a real project, not a dependency swap ([[What is the difference between Quarkus and Spring Boot]]).

> [!tip] Interview answer
> I frame it as constraints: if the workload pays for cold starts — serverless, scale-to-zero, dense Kubernetes packing, CLI tools — Quarkus' build-time architecture and native support make it the right tool. If the service is long-running and the team lives in Spring, Boot's ecosystem and familiarity outweigh startup numbers. Both run fine in JVM mode for years-long services, so I decide from cost structure and team reality, and I prototype and measure when the answer is not obvious.
