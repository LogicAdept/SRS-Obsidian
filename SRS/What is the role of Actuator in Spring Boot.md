<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #SRS

# What is the role of Actuator in Spring Boot?

> [!abstract] Short answer
> Actuator is Boot’s **production-ready ops layer**: **monitor and manage** a running app over **HTTP** (`/actuator/{id}`) or **JMX**. Built-in endpoints cover **health**, **metrics** (Micrometer), **info**, **loggers**, **mappings**, dumps, and more. Add **`spring-boot-starter-actuator`**. An endpoint is **available** only when **access is permitted and it is exposed**. Default HTTP **and JMX** include is **`health` only**.

## Ops endpoints, not your public API

Official: extra features for when you **push to production** — HTTP or JMX; auditing, health, and metrics can apply automatically. The manufacturing metaphor: a small control that moves a large machine. Role in an interview: **liveness/readiness**, scrape **Prometheus**, inspect **beans/conditions**, change **log levels**, not “a REST framework for metrics” ([[How do you monitor an application with Spring Boot Actuator]], [[What is Micrometer observability in Spring Boot]]).

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

**Listing 1.** Starter pulls `spring-boot-actuator` auto-config. Default map: **`health` → `/actuator/health`**. `info`, `metrics`, `mappings`, `heapdump` exist but are **not** HTTP-exposed until `management.endpoints.web.exposure.include` ([[Which Actuator endpoints are exposed over HTTP by default]]).

```properties
management.endpoints.web.exposure.include=health,metrics,prometheus
```

**Listing 2.** Boot **4** **access** (`none` / `read-only` / `unrestricted`) replaced deprecated `enabled`. `shutdown` and `heapdump` are **not** unrestricted by default. JMX default include is also **`health` only**. Sanitize `env` / `configprops`. This is **in-process**; Spring Boot Admin is a **separate UI** that **calls** these endpoints ([[What is the difference between enabling and exposing an Actuator endpoint]], [[What is the difference between Spring Boot Actuator and Spring Boot Admin]]).

```d2
direction: down
starter: "spring-boot-starter-actuator" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
eps: "Endpoints: health, metrics,\nloggers, mappings, …" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
http: "HTTP /actuator\ndefault: health only" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
jmx: "JMX\nsame default include" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

starter -> eps
eps -> http
eps -> jmx
```

**Fig. 1.** K8s probes use **health groups**, not a random business URL ([[How do you implement Kubernetes probes with Spring Boot]]). Lock down anything beyond health ([[How do you expose Spring Boot Actuator endpoints safely]]).

> [!warning] Not “RESTful metrics you can just call”
> Dump wording treats Actuator as an open REST catalog. **`beans` / `env` / `heapdump` / `loggers` POST** are sensitive. Exposure is **opt-in** except `health`. Adding the starter does **not** publish `info` on HTTP anymore.

> [!warning] Available = access **and** exposure
> Inaccessible endpoints are **removed from the context**. Changing `include` does not grant `shutdown`. `logfile` needs `logging.file.name` / `logging.file.path`. `prometheus` needs `micrometer-registry-prometheus`.

> [!tip] Interview answer
> Actuator is how I operate a Boot app in production: health, metrics, and management endpoints over HTTP or JMX. I add spring-boot-starter-actuator. By default only health is exposed. I treat the rest as sensitive and I do not confuse Actuator with Spring Boot Admin.
