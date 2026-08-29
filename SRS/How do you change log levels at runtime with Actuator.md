<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #Java/Logging #SRS

# How do you change log levels at runtime with Actuator?

> [!abstract] Short answer
> Expose Actuator’s **`loggers`** endpoint and **`POST`** JSON `{"configuredLevel":"DEBUG"}` to **`/actuator/loggers/{name}`** (a logger such as `com.example`, `ROOT`, or a **logger group**). **`GET /actuator/loggers`** lists `configuredLevel` vs `effectiveLevel`. The change is in-process — **no restart**. Reset with `configuredLevel: null` or `POST {}`. This is **not** `/logfile`, which only **reads** a file when `logging.file.name` / `logging.file.path` is set.

## View, then POST a level

With `spring-boot-starter-actuator` on the classpath, the `loggers` endpoint **shows and modifies** logger configuration. HTTP mapping is `/actuator/loggers` and `/actuator/loggers/{logger.name}` (same path for a **group** name).

Allowed levels: **`TRACE`**, **`DEBUG`**, **`INFO`**, **`WARN`**, **`ERROR`**, **`FATAL`**, **`OFF`**, and **`null`** (no explicit configuration). `configuredLevel` is what you set; `effectiveLevel` is what the logging framework actually uses after inheritance.

```json
{
  "configuredLevel": "DEBUG"
}
```

**Listing 1.** Body of `POST /actuator/loggers/com.example`. The REST API’s curl sample uses `"debug"`; it sets `DEBUG`.

```bash
curl -X POST '/actuator/loggers/com.example' \
  -H 'Content-Type: application/json' \
  -d '{"configuredLevel":"DEBUG"}'
```

**Listing 2.** Runtime change for one logger. `POST` the same JSON to a **group** name (built-in examples in the API sample: `web`, `sql`) to move every member.

`GET /actuator/loggers` returns `levels`, `loggers` (name → configured/effective), and `groups` (configured level + `members`). `GET /actuator/loggers/ROOT` is a single logger. Clearing: `POST` `{"configuredLevel": null}` or an empty `{}` so the logger falls back to the default configuration.

```properties
management.endpoints.web.exposure.include=health,loggers
```

**Listing 3.** Required for HTTP: default web exposure is **`health` only** ([[Which Actuator endpoints are exposed over HTTP by default]]).

```d2
direction: right
get: "GET /actuator/loggers\nconfigured vs effective" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
post: "POST /actuator/loggers/{name}\nconfiguredLevel" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
runtime: "Logging framework\nno restart" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

get -> post -> runtime
```

**Fig. 1.** Read the map, then POST a level. `/logfile` is a different endpoint (file contents), not a level switch.

> [!warning] Exposed is not enough to POST
> `/loggers` is **not** HTTP-exposed by default. Even after `include=loggers`, **read-only** access (`management.endpoint.loggers.access=read-only`) allows GET but not the change. With Spring Security’s default CSRF, **POST** to `loggers` (and `shutdown`) returns **403**. If Security is on the classpath and you did not write a `SecurityFilterChain`, actuators other than `/health` are secured. Do not confuse **enabled** vs **exposed** ([[What is the difference between enabling and exposing an Actuator endpoint]]).

> [!warning] Runtime level is not `logging.file.*`
> `/logfile` **streams the log file**; it does not set levels, and it exists only when a file name or path is configured. A POST here is **process-local**: it does not rewrite `application.properties`, and the next restart restores file-based `logging.level.*`.

> [!tip] Interview answer
> I expose Actuator loggers and POST configuredLevel to /actuator/loggers/{name} — a package, ROOT, or a logger group — so DEBUG sticks until I reset it with null or {}. GET shows configured versus effective levels. It must be HTTP-exposed, writable, and CSRF-aware; /logfile is only for reading a log file, not for changing levels.
