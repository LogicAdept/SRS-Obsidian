<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# Which Actuator endpoints are exposed over HTTP by default?

> [!abstract] Short answer
> **Only `health`.** With `spring-boot-starter-actuator` on the classpath, **`management.endpoints.web.exposure.include`** defaults to **`health`**, so HTTP maps **`/actuator/health`** (base path `/actuator`). **JMX’s include is also `health` on current Boot.** Other IDs (`info`, `metrics`, `env`, …) may have **unrestricted access** and still **404** until you add them to `include`. Dumps that list **`/info` as a default** describe **older Boot** (2.x), not current.

## One ID on the wire

Exposure is **per technology**. Defaults:

| Property | Default |
|---|---|
| `management.endpoints.web.exposure.include` | `health` |
| `management.endpoints.web.exposure.exclude` | (empty) |
| `management.endpoints.jmx.exposure.include` | `health` |
| `management.endpoints.jmx.exposure.exclude` | (empty) |

`exclude` **wins** over `include`. An endpoint is **available** only if access is permitted **and** it is exposed ([[What is the difference between enabling and exposing an Actuator endpoint]]).

```properties
management.endpoints.web.exposure.include=health,info,metrics
```

**Listing 1.** Opt-in extra HTTP IDs. `info` is **not** implied by the starter.

```properties
management.endpoints.web.exposure.include=*
management.endpoints.web.exposure.exclude=env,beans
```

**Listing 2.** Official “everything except …” pattern. Quote `"*"` in YAML (`*` is an alias). This is the **open management** setup ([[How do you expose Spring Boot Actuator endpoints safely]]).

Liveness/readiness **probes** are **health groups** (`/actuator/health/liveness`, `/actuator/health/readiness`), not extra rows in `include`. The ID is still **`health`** ([[How does the Actuator health endpoint aggregate status]]).

```d2
direction: down
starter: "spring-boot-starter-actuator" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
http: "HTTP include = health\nGET /actuator/health" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
rest: "info, metrics, env, …\n404 until include" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}

starter -> http
starter -> rest
```

**Fig. 1.** The starter **auto-configures** endpoints. **HTTP publication** is a second switch.

Custom strategy: an **`EndpointFilter`** bean. If Spring Security is on the classpath and you did not define a `SecurityFilterChain`, actuators **other than** `/health` are secured — after you actually expose them.

> [!warning] `/info` is not a current HTTP default
> Interview lists from Boot **2** often pair **health + info**. Current docs: **health only**, on **web and JMX**. Access being unrestricted is **not** the same as a 200 from `/actuator/info`.

> [!warning] `include=*` is not “production ready”
> Official: if the app is public, **secure** actuators (firewall and/or Spring Security) before widening `include`. `env`, `heapdump`, `loggers`, `shutdown` are the usual leaks. YAML `include: *` without quotes is invalid.

> [!tip] Interview answer
> By default Boot exposes only the health Actuator endpoint over HTTP — /actuator/health — even though the starter is on the classpath. I add others with management.endpoints.web.exposure.include. Info used to be a default on older Boot; it is not now. Star include plus no security is the open-management anti-pattern.
