<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #DevOps/Tools/Kubernetes #SRS

# How do you implement Kubernetes probes with Spring Boot?

> [!abstract] Short answer
> Put `spring-boot-starter-actuator` on the classpath. Boot already exposes **`health`**, and the **`liveness`** / **`readiness` health groups** are on by default at **`/actuator/health/liveness`** and **`/actuator/health/readiness`**. Point kubelet **`livenessProbe`** and **`readinessProbe`** at those paths (different probes). Do **not** hang **liveness** on a database. On a **separate** management port, also set **`management.endpoint.health.probes.add-additional-paths=true`** so probes hit the **app** server (`/livez`, `/readyz`).

## Availability state, then two HTTP groups

Boot keeps in-memory **`ApplicationAvailability`**: **`LivenessState`** (`CORRECT` / `BROKEN`) and **`ReadinessState`** (`ACCEPTING_TRAFFIC` / `REFUSING_TRAFFIC`). Actuator maps those to **`LivenessStateHealthIndicator`** / **`ReadinessStateHealthIndicator`** and to health groups. They are **not** extra `include` IDs — they ride on **`health`** ([[Which Actuator endpoints are exposed over HTTP by default]]).

Current Boot: **`management.endpoint.health.probes.enabled`** defaults to **`true`**. Set it **`false`** to turn the groups off. Older docs said groups auto-enabled **only in Kubernetes**; interview dumps that tell you to “turn probes on” are describing that older default.

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
```

**Listing 1.** kubelet wiring from the Actuator guide. Use the **management** port if you set `management.server.port`. **`startupProbe`** is optional: readiness already refuses traffic until runners finish; use a startup probe on the **liveness** path if the process is so slow that kubelet would **kill** it for failing liveness during boot ([[What is the difference between liveness readiness and startup probes in Kubernetes]]).

By default **neither group includes `db` or other indicators**. Add checks only to **readiness**, and only for dependencies that should take the instance **out of the Service**:

```properties
management.endpoint.health.group.readiness.include=readinessState,customCheck
management.endpoint.health.probes.add-additional-paths=true
```

**Listing 2.** Extra readiness members ([[How do you write a custom HealthIndicator in Spring Boot]]). `add-additional-paths=true` publishes **`/livez`** and **`/readyz`** on the **main** server so a split management context cannot report UP while Tomcat cannot accept connections ([[How do you expose Spring Boot Actuator endpoints safely]]). Override paths with `management.endpoint.health.group.<name>.additional-path=server:/healthz` (prefix **`server:`** or **`management:`**, one path segment).

```java
AvailabilityChangeEvent.publish(applicationContext, LivenessState.BROKEN);
```

**Listing 3.** Irrecoverable internal failure. Components inject **`ApplicationAvailability`** or listen for **`AvailabilityChangeEvent`**. Do **not** publish `BROKEN` because Redis blipped.

| Startup phase | Liveness | Readiness | HTTP |
|---|---|---|---|
| Starting | `BROKEN` | `REFUSING_TRAFFIC` | not started |
| Started (context up, runners still going) | `CORRECT` | `REFUSING_TRAFFIC` | refuses |
| Ready | `CORRECT` | `ACCEPTING_TRAFFIC` | accepts |

Lifecycle from the reference. On graceful shutdown, readiness goes **`REFUSING_TRAFFIC`** while in-flight work drains; HTTP probes then stop being a reliable external signal.

```d2
direction: down
avail: "ApplicationAvailability\nCORRECT / ACCEPTING_TRAFFIC" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
live: "/actuator/health/liveness\nkubelet restarts if down" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
ready: "/actuator/health/readiness\nService stops routing" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

avail -> live
avail -> ready
```

**Fig. 1.** Same process, two kubelet questions ([[How does the Actuator health endpoint aggregate status]]). If **every** pod is unready, a `ClusterIP`/`NodePort` Service accepts **no connection** (not a 503 from the app).

> [!warning] Liveness must not check shared externals
> A failed liveness makes Kubernetes **restart** the container. If every replica probes the same down database, you get a **restart storm**. Boot therefore **does not** put other indicators on these groups. Readiness may include an instance-local dependency; a shared, circuit-broken dependency often stays **out** of the probe.

> [!warning] Do not point both probes at `/actuator/health`
> Combined health includes **everything** you enabled (`db`, disk, …). That couples “restart me” with “stop sending traffic.” Use the **group** paths. A custom management port without **`add-additional-paths`** can look live while the **application** port is dead.

> [!tip] Interview answer
> Actuator health groups: /actuator/health/liveness and /actuator/health/readiness, on by default in current Boot. Kubelet livenessProbe restarts, readinessProbe removes from the Service. I never put the database on liveness. If management uses another port I enable add-additional-paths so /livez and /readyz hit the app server. Long startup is a startupProbe on the liveness path, not a fat combined /health check.
