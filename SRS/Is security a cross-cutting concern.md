<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Framework/AOP #SRS

# Is security a cross-cutting concern?

> [!abstract] Short answer
> **Yes.** Authorization and authentication cut across many types and layers — they are not owned by one business module. Spring treats that as classic cross-cutting work: a **Servlet filter chain** at the web edge, and **Spring AOP method security** (`@PreAuthorize`, …) at the service layer.

## Why “cross-cutting”

Spring AOP literature defines **cross-cutting concerns** as behavior that spans multiple types and objects — **transaction management** is the textbook example. **Security** fits the same definition: every controller and many services need consistent authz/authn without copying checks into each method body — [[What is a cross-cutting concern]].

You configure security **once** (filter chain + optional method annotations) instead of scattering `if (!hasRole(...))` through domain code — [[Which parts of a system would you move into aspects]].

## How Spring Security implements it

| Layer | Mechanism | What it protects |
|---|---|---|
| **HTTP / Servlet** | `SecurityFilterChain` via `FilterChainProxy` | URLs, sessions, CSRF, headers, authentication entry |
| **Method / service** | Spring AOP advisors (`@EnableMethodSecurity`) | Method args/return values, service-layer rules |

Method security docs state it is **built using Spring AOP** — the same interceptor model as `@Transactional`. URL rules alone are not enough when the same service is called from multiple entry points — [[Why does method security still matter if URL rules exist]].

```java
@EnableMethodSecurity
@Configuration
class SecurityConfig { }

@Service
class OrderService {
    @PreAuthorize("hasRole('ADMIN')")
    public void cancel(long orderId) { /* domain work only */ }
}
```

**Listing 1.** Authorization is declared once on the join point; business logic stays free of role checks.

```d2
direction: right
http: "HTTP request" {
  width: 120
  height: 45
  style.fill: "#e3f2fd"
}
filters: "Security\nfilter chain" {
  width: 140
  height: 55
  style.fill: "#fff3e0"
}
mvc: "Controller" {
  width: 110
  height: 45
  style.fill: "#f3e5f5"
}
aop: "Method-security\nAOP proxy" {
  width: 150
  height: 55
  style.fill: "#fff3e0"
}
svc: "Service\n(domain)" {
  width: 120
  height: 45
  style.fill: "#e8f5e9"
}

http -> filters -> mvc -> aop -> svc
```

**Fig. 1.** Security wraps the call path at the web edge and again at advised service methods — both are cross-cutting, not domain-local.

> [!warning] Not “just a filter”
> Calling security **only** a filter misses **method security**. Filters cover the HTTP boundary; AOP covers bean method invocations (including non-web callers). Boot’s security starter does **not** enable method security by default — you need `@EnableMethodSecurity`.

> [!tip] Interview answer
> Yes — security spans the whole app like logging and transactions. Spring Security uses the filter chain for web requests and Spring AOP for @PreAuthorize-style method rules, so you configure it centrally instead of duplicating checks in every controller.
