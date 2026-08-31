<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS

# How do you enable Spring Security debug logging for the filter chain?

> [!abstract] Short answer
> Turn the **`org.springframework.security` logger to `DEBUG` or `TRACE`**. Startup **`DEBUG`** on `DefaultSecurityFilterChain` prints each chain’s filter list. **`TRACE`** on `FilterChainProxy` prints `Invoking SomeFilter (n/m)` **per request**. `@EnableWebSecurity(debug = true)` is a **different** switch: `DebugFilter` dumps multi-line request details (headers, parameters) — **dev only**.

## Logger levels vs `debug = true`

401/403 responses stay opaque on purpose. The explanation is in the logs.

```properties
logging.level.org.springframework.security=TRACE
```

**Listing 1.** Boot property (or a Logback logger named `org.springframework.security` at `trace`). `DEBUG` is enough to see `FilterChainProxy` `Securing METHOD /path` and the **startup** line `Will secure any request with [ … filters … ]`. `TRACE` is what walks **every** filter in [[What is FilterChainProxy and DelegatingFilterProxy]].

```java
@Configuration
@EnableWebSecurity(debug = true)
public class SecurityConfig {
    // SecurityFilterChain beans…
}
```

**Listing 2.** `debug` on [[What is the purpose of EnableWebSecurity]] wraps the chain in `DebugFilter` (XML `<debug />`). That is **not** the same as Listing 1. It prints a human-readable, multi-line view of each request **into** the security filters.

```d2
direction: down
trace: "logging TRACE\nFilterChainProxy Invoking … (n/m)" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
boot: "logging DEBUG\nDefaultSecurityFilterChain list at startup" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
dbg: "@EnableWebSecurity(debug = true)\nDebugFilter request dump" {
  width: 280
  height: 55
  style.fill: "#fce4ec"
}

boot -> trace: "add TRACE for per-filter"
dbg -> trace: "orthogonal to loggers"
```

**Fig. 1.** Three knobs: startup filter list, per-request `Invoking` lines, and the sensitive `DebugFilter` dump.

A breakpoint in `FilterChainProxy` is the documented place to start when the logs are not enough.

> [!warning] `debug = true` is not for production
> The debug infrastructure may log **request parameters and headers** (including `Authorization`). `WebSecurity` wraps the proxy only when debug is on and warns that this **may include sensitive information** — do not ship it. Prefer Listing 1 in shared environments.

> [!tip] Interview answer
> Set org.springframework.security to DEBUG to print each SecurityFilterChain’s filters at startup, and TRACE to see FilterChainProxy invoke them per request. That is how you debug 401/403. EnableWebSecurity(debug = true) is a separate DebugFilter that can leak headers and tokens — never in production.
