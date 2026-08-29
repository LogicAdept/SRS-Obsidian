<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Actuator #Java/Spring/Security/FilterChain #SRS

# How do you expose Spring Boot Actuator endpoints safely?

> [!abstract] Short answer
> Keep the default HTTP include (**`health` only**). Widen **`management.endpoints.web.exposure.include`** only after the extra IDs are **behind a firewall**, **Spring Security**, or both. A custom **`SecurityFilterChain`** **replaces** Boot’s actuator rules — you must write them. Isolate ops traffic with **`management.server.port`** and optionally **`management.server.address`**. Leave **`management.endpoint.health.show-details`** at **`never`** unless the caller is trusted.

## Three gates, then a bind address

An endpoint is on the wire only when **access** permits it **and** the transport **exposes** it ([[What is the difference between enabling and exposing an Actuator endpoint]]). Safety is a **third** gate: who may call the URL.

```properties
management.endpoints.web.exposure.include=health,info,prometheus
management.server.port=8081
management.server.address=127.0.0.1
management.endpoint.health.show-details=never
```

**Listing 1.** Opt-in IDs, separate management port, loopback bind. `address` **requires** a port that **differs** from the app server. `show-details` default is already **`never`** (`when-authorized` / `always` leak indicator bodies). `info` and `prometheus` are **not** HTTP defaults ([[Which Actuator endpoints are exposed over HTTP by default]]).

Official checklist **before** any `include` change: the payload is not sensitive, **or** it sits behind a **firewall**, **or** **Spring Security** (or equivalent) authenticates callers.

If `spring-boot-starter-security` is on the classpath and you **did not** declare a `SecurityFilterChain`, Boot auto-config **secures every actuator other than `/health`**. Declare **any** `SecurityFilterChain` and that auto-config **backs off completely**.

```java
@Configuration(proxyBeanMethods = false)
public class MySecurityConfiguration {

	@Bean
	SecurityFilterChain actuatorChain(HttpSecurity http) {
		http.securityMatcher(EndpointRequest.toAnyEndpoint());
		http.authorizeHttpRequests((requests) -> requests.anyRequest().hasRole("ENDPOINT_ADMIN"));
		http.httpBasic(withDefaults());
		return http.build();
	}
}
```

**Listing 2.** Boot 4 matcher: `org.springframework.boot.security.autoconfigure.actuate.web.servlet.EndpointRequest`. This chain **only** covers actuators. You still need **another** `SecurityFilterChain` for the application. `EndpointRequest.to("health")` matches the ID **and** subpaths (`/actuator/health/**`).

Behind a **private** network you may `include=*` **and** `permitAll()` on `EndpointRequest.toAnyEndpoint()` — that is the **firewall** pattern, not a public-internet pattern. Quote `"*"` in YAML.

```d2
direction: down
access: "access\nnone / read-only / unrestricted" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
expose: "web.exposure.include\ndefault health" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
sec: "firewall and/or\nEndpointRequest + roles" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
bind: "optional management.port\n+ management.address" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

access -> expose -> sec -> bind
```

**Fig. 1.** Exposure is not authorization. `env` / `configprops` / `quartz` values are **`******`** unless you raise `show-values`. **`heapdump`** and **`shutdown`** are not unrestricted by default; still do not `include` them on a public port.

Kubernetes liveness/readiness are **health groups** (`/actuator/health/liveness`, `/actuator/health/readiness`), still the **`health`** ID. If Actuator sits on a **separate** management context, a probe can pass while the **main** server cannot accept connections — set **`management.endpoint.health.probes.add-additional-paths=true`** so `/livez` and `/readyz` hit the **application** port ([[How does the Actuator health endpoint aggregate status]]).

> [!warning] Your `SecurityFilterChain` owns Actuator
> One application chain that `permitAll()` on `/**` also opens **`/actuator/**`**. Boot will not keep the “everything except health is authenticated” default. Match actuators with **`EndpointRequest`**, not a guessed `/actuator/**` string if you change `management.endpoints.web.base-path`.

> [!warning] CSRF and mutating endpoints
> Default Spring Security **CSRF** is on. **`POST` / `PUT` / `DELETE`** actuators (`shutdown`, `loggers`, …) return **403** until the client sends a token **or** you disable CSRF for **non-browser** services only. Sanitization does **not** make `env` safe to expose.

> [!tip] Interview answer
> I leave HTTP exposure at health unless ops needs more, then I list IDs on management.endpoints.web.exposure.include and put that surface behind a firewall, Spring Security, or a loopback management.server.address on a second port. A custom SecurityFilterChain replaces Boot’s actuator rules, so I use EndpointRequest and a role. Health details stay never; I never include env or heapdump on a public URL.
