<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/MethodSecurity #SRS

# At what levels can Spring Security enforce access control?

> [!abstract] Short answer
> Two primary levels in a typical app: **web / request** (`SecurityFilterChain` + `authorizeHttpRequests` / `AuthorizationFilter`) and **method** (Spring AOP + `@PreAuthorize`, `@PostAuthorize`, `@Secured`, … via `@EnableMethodSecurity`). Both use **`AuthorizationManager`**; they differ in **what** is secured — an HTTP request vs a bean method invocation.

## Request level (filter chain)

Guards **incoming HTTP** before MVC:

- Matchers on URL / HTTP method
- Runs inside the ordered security filters — [[How does the Spring Security filter chain work]]
- Only applies when the call arrives over that web entry point

## Method level (AOP)

Guards **Spring bean method invocations**:

- `@PreAuthorize` / `@PostAuthorize` / filters — can use **parameters and return values**
- Applies whether the caller is a controller, scheduler, messaging listener, or another bean — [[Why does method security still matter if URL rules exist]]
- Boot’s security starter does **not** enable this by default — add `@EnableMethodSecurity`

Spring’s authorization architecture describes interceptors for **web requests** and **method invocations** (and messaging) that delegate to `AuthorizationManager`.

```d2
direction: down
http: "HTTP request" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
url: "URL / filter-chain\nauthorization" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
mvc: "Controller" {
  width: 120
  height: 40
  style.fill: "#f3e5f5"
}
meth: "Method security\n(@PreAuthorize …)" {
  width: 180
  height: 55
  style.fill: "#e8f5e9"
}
svc: "Service method" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}
other: "Job / listener\n(no HTTP)" {
  width: 140
  height: 50
  style.fill: "#ffebee"
}

http -> url -> mvc -> meth -> svc
other -> meth
```

**Fig. 1.** URL rules cover the HTTP edge; method security covers every proxied call into the service.

> [!warning] Proxy limits still apply
> Method security skips **self-invocation** and **private** methods under default proxy AOP — [[Can Spring AOP advise private methods]], [[Why does a self-invocation skip Spring AOP advice]]. Defense in depth still needs **both** layers for HTTP-exposed services.

> [!tip] Interview answer
> Web level: SecurityFilterChain authorizeHttpRequests. Method level: @EnableMethodSecurity and @PreAuthorize on services. Use both — URL rules alone miss non-HTTP callers and fine-grained argument checks.
