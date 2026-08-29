<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Spring/Boot/Actuator #SRS

# How can you debug which auto-configuration classes applied?

> [!abstract] Short answer
> Turn on Boot’s **`debug` property** (`--debug`, `-Ddebug`, or `debug=true`) so a **conditions report** is logged: which auto-configuration (and other `@Configuration`) classes matched, which did not, and the **condition message** for each. In a running app with **Actuator**, `GET /actuator/conditions` returns the same `ConditionEvaluationReport` as JSON — but that endpoint is **not** HTTP-exposed by default.

## Console report at startup

`ConditionEvaluationReport` is recorded on the `ApplicationContext` as `@Conditional*` annotations are evaluated. `ConditionEvaluationReportLoggingListener` writes that report to the log at **DEBUG**. On a **crash**, the listener logs an **INFO** hint to run again with debug enabled rather than dumping the full report.

`--debug` does two things at once: it enables **debug logs for a selection of core loggers** (embedded container, Hibernate, Spring Boot) **and** it logs the conditions report. It does **not** set every logger to DEBUG.

```properties
debug=true
```

**Listing 1.** Same `debug` property as the `--debug` CLI switch or the `-Ddebug` system property. Default is `false`.

```bash
java -jar myapp.jar --debug
```

**Listing 2.** Command-line form of the same `debug` property.

A narrower alternative when you only want the report: set **DEBUG** on `org.springframework.boot.autoconfigure.logging.ConditionEvaluationReportLoggingListener` instead of turning on debug mode.

```d2
direction: right
debug: "debug=true\n--debug / -Ddebug" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
listener: "ConditionEvaluationReportLoggingListener\n(DEBUG)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
report: "ConditionEvaluationReport\nmatched / not matched" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
actuator: "GET /actuator/conditions\n(JSON, runtime)" {
  width: 220
  height: 70
  style.fill: "#f3e5f5"
}

debug -> listener -> report
report -> actuator
```

**Fig. 1.** One report object; two views — startup log versus Actuator JSON.

## Runtime JSON from Actuator

With `spring-boot-starter-actuator` on the classpath, the `conditions` endpoint serializes the report. Default mapping is **`GET /actuator/conditions`** (or the JMX equivalent). The JSON is keyed by **application context id** and includes:

| Field | Meaning |
|---|---|
| **`positiveMatches`** | Classes and methods with conditions that **matched**, each with `condition` + `message` |
| **`negativeMatches`** | Classes and methods with conditions that **did not** match: `notMatched` (why it failed) and `matched` (conditions that still passed) |
| **`unconditionalClasses`** | Auto-configuration classes that were evaluated but were **not** conditional |
| **`parentId`** | Parent context, when you have a hierarchy |

```properties
management.endpoints.web.exposure.include=health,conditions
```

**Listing 3.** Required for HTTP: by default only **`health`** is exposed over HTTP. `exclude` takes precedence over `include`.

Read a **negative** match by the failed `@ConditionalOnClass` / `OnBean` / `OnProperty` / `OnWebApplication` message — that is why a starter’s auto-config stayed off. If a class you do not want is a **positive** match, exclude it ([[How do you disable a specific auto-configuration class]]) rather than guessing from the classpath.

> [!warning] Conditions is Actuator, and exposure is not enablement
> Adding the Actuator starter does **not** publish `/actuator/conditions`. Endpoints are auto-configured only when Actuator is present; HTTP exposure still defaults to **`health`**. You must **include** `conditions` ([[Which Actuator endpoints are exposed over HTTP by default]], [[What is the difference between enabling and exposing an Actuator endpoint]]). If Spring Security is on the classpath and you have not defined your own `SecurityFilterChain`, every actuator **other than** `/health` is secured. The report also lists **your** `@Configuration` classes, not only `*AutoConfiguration`.

> [!warning] `--debug` is not “log everything”
> Debug mode raises a **fixed set of core loggers**. It will not flip `logging.level.root` to DEBUG, and a custom logging setup that never lets that listener reach DEBUG will hide the report. Prefer `debug=true` for the report; use logger-specific levels when you need a quiet, targeted dump.

> [!tip] Interview answer
> I enable Boot’s debug property — `--debug`, `-Ddebug`, or `debug=true` — which logs the ConditionEvaluationReport: positive matches, negative matches with the failing condition, and unconditional classes. For a live process I use Actuator’s conditions endpoint, after the starter is on the classpath and `conditions` is actually HTTP-exposed. `--debug` also turns on extra core loggers; it is not the same as root DEBUG, and `/actuator/conditions` is not open by default.
