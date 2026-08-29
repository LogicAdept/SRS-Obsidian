<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# How do you monitor an application with Spring Boot Actuator?

> [!abstract] Short answer
> Add **`spring-boot-starter-actuator`**. Actuator publishes **endpoints** so you can **monitor and interact** with the process over **HTTP** (`/actuator/{id}`) or **JMX**. Default HTTP **and** JMX include is **`health` only**. For production: keep **health** (and k8s **liveness/readiness groups**), add **`metrics` / `prometheus`** behind a scrape network, **do not** expose **`env` / `heapdump`**, use a **management port** and **Spring Security**, and write a **`HealthIndicator`** for dependencies you actually care about.

## Starter, then endpoints, then a scrape

The `spring-boot-actuator` module is production-ready features: health, metrics (via **Micrometer**), loggers, dumps, conditions, … You turn the module on with the starter. Built-in endpoints are auto-configured only when they are **available**: **access** permitted **and** **exposed** on a transport ([[What is the difference between enabling and exposing an Actuator endpoint]]).

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**Listing 1.** Official enablement. HTTP base path is **`/actuator`**. `GET /actuator` is the **links** document for **exposed** IDs — not a catalog of every endpoint on the classpath.

```properties
management.endpoints.web.exposure.include=health,info,metrics,prometheus,loggers
management.server.port=8081
```

**Listing 2.** Opt-in HTTP IDs plus a separate management port ([[How do you expose Spring Boot Actuator endpoints safely]]). Quote `"*"` in YAML. Dumps that still set `management.endpoint.*.enabled` / `management.endpoints.enabled-by-default` are the **deprecated** spellings of **`access`**.

| ID | What it is for monitoring |
|---|---|
| `health` | Aggregate status; k8s groups **`/actuator/health/liveness`**, **`/actuator/health/readiness`** |
| `metrics` | Micrometer meters (JVM, CPU, HTTP, …) as JSON |
| `prometheus` | Same meters, scrape format — needs **`micrometer-registry-prometheus`** |
| `loggers` | **Logger levels** at runtime — not the log file |
| `logfile` | File contents, only if `logging.file.name` / `logging.file.path` is set |
| `httpexchanges` | Last ~100 HTTP exchanges; needs an **`HttpExchangeRepository`** bean |
| `threaddump` / `heapdump` | JVM diagnostics; **heapdump** is restricted and must not be public |

**Listing 3 (table).** `httptrace` is the **old** ID. `info` is **not** an HTTP default ([[Which Actuator endpoints are exposed over HTTP by default]]). `loggers` **shows and modifies** configuration ([[How do you change log levels at runtime with Actuator]]).

```d2
direction: down
starter: "spring-boot-starter-actuator" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
health: "/actuator/health\nkubelet / load balancer" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
metrics: "Micrometer\n/metrics or /prometheus" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
ops: "loggers, conditions, …\nbehind firewall / Security" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

starter -> health
starter -> metrics
starter -> ops
```

**Fig. 1.** Health is the **probe**. Metrics are the **time series** (Prometheus, Datadog, OTLP, … — a `micrometer-registry-*` on the classpath is enough for Boot to wire a `MeterRegistry`). Ops endpoints are **interactive**, not scrape targets ([[How do you implement Kubernetes probes with Spring Boot]]).

Custom dependency checks: a **`HealthIndicator`** bean ([[How do you write a custom HealthIndicator in Spring Boot]]). Details stay hidden while **`management.endpoint.health.show-details`** is **`never`**.

A **dashboard** is optional: **Spring Boot Admin** polls these URLs; it does not replace Actuator ([[What is the difference between Spring Boot Actuator and Spring Boot Admin]]). JMX is the other transport — current default include is still **`health` only**.

> [!warning] The links document is not “everything is on”
> Interview JSON that lists **`health` + `info`** as the only `_links` is **Boot 2**. Current default `_links` is **`health`** (and `self`). `include=*` without a firewall leaks **`env`**, **`heapdump`**, **`mappings`**, **`beans`**. Sanitization (`******`) is not a reason to expose `env`.

> [!warning] `loggers` is not `logfile`, and `enabled` is not exposure
> `GET /actuator/loggers` does **not** stream log lines. HTTP **403** on `POST` loggers is often **CSRF**. Inaccessible endpoints are **removed from the context**; changing **include** does not raise **`read-only`** to **`unrestricted`**.

> [!tip] Interview answer
> I add spring-boot-starter-actuator. Health is on by default at /actuator/health; I point probes at the liveness and readiness groups. For metrics I add a Micrometer registry — prometheus if we scrape — and include those IDs on HTTP behind a management port and Spring Security. I never expose env or heapdump. Custom HealthIndicator beans cover our dependencies. Dumps that mention httptrace and enabled-by-default are a version behind.
