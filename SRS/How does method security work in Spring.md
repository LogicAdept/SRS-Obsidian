<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# How does method security work in Spring?

> [!abstract] Short answer
> **Method security is Spring AOP on service (and other bean) methods.** `@EnableMethodSecurity` publishes **advisors** that intercept annotated invocations. A **before** interceptor evaluates `@PreAuthorize` / `@Secured` / JSR-250 **before** the target runs; an **after** interceptor evaluates `@PostAuthorize` **after** a normal return. Denial throws `AccessDeniedException`. This is **not** the servlet `SecurityFilterChain`.

## Enablement, then advisors on the proxy

`spring-boot-starter-security` **does not** turn this on. Add `@EnableMethodSecurity` on a `@Configuration` class (or `<sec:method-security/>`). That annotation **supersedes** deprecated `@EnableGlobalMethodSecurity`.

Defaults on `@EnableMethodSecurity` (since Spring Security **5.6**; Security **6** / Boot **3** is the usual migration point):

| Attribute | Default | What it registers |
|---|---|---|
| `prePostEnabled` | `true` | `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, `@PostFilter` |
| `securedEnabled` | `false` | `@Secured` |
| `jsr250Enabled` | `false` | JSR-250 (`@RolesAllowed`, …) |
| `mode` | `AdviceMode.PROXY` | Spring AOP proxies, not AspectJ weaving |

The old `@EnableGlobalMethodSecurity` defaulted **`prePostEnabled` to `false`**. `@EnableMethodSecurity` with no attributes is the functional replacement for `@EnableGlobalMethodSecurity(prePostEnabled = true)`.

Each annotation has **its own pointcut** (method, class, interface, and meta-annotations) and **its own interceptor**. Multiple **different** annotations on one invocation are evaluated **in series** (all must pass). Repeating the **same** annotation on one method is **not** supported — combine with SpEL instead.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
}

@Service
public class CustomerService {

    @PreAuthorize("hasAuthority('permission:read')")
    @PostAuthorize("returnObject.owner == authentication.name")
    public Customer readCustomer(String id) {
        return load(id);
    }
}
```

**Listing 1.** Conceptual enablement — pre/post annotations are on by default; `@Secured` still needs `securedEnabled = true`.

## What runs on one call

For `readCustomer` with both pre- and post-authorize:

1. The caller hits the **Spring AOP proxy**, not the raw target.
2. `AuthorizationManagerBeforeMethodInterceptor.preAuthorize()` matches `@PreAuthorize`. It builds a SpEL `EvaluationContext` via `MethodSecurityExpressionHandler` / `MethodSecurityExpressionRoot` and runs `PreAuthorizeAuthorizationManager`.
3. If the expression fails, the interceptor publishes `AuthorizationDeniedEvent` and throws `AccessDeniedException` — the **target method never runs**.
4. If it passes, the target method executes.
5. `AuthorizationManagerAfterMethodInterceptor.postAuthorize()` runs `PostAuthorizeAuthorizationManager` against the **return value**. Failure is the same deny path after the method has already run.

`@PreFilter` / `@PostFilter` use `PreFilterAuthorizationMethodInterceptor` and `PostFilterAuthorizationMethodInterceptor` (they filter collections; they are not the same class as the authorize interceptors). `@Secured` and JSR-250 use **before** interceptors (`AuthorizationManagerBeforeMethodInterceptor.secured()` / `.jsr250()`) once those flags are on.

```d2
direction: down
client: "Other bean / controller\ncalls the proxy" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
before: "AuthorizationManagerBeforeMethodInterceptor\n@PreAuthorize SpEL" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
target: "Target method body" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
after: "AuthorizationManagerAfterMethodInterceptor\n@PostAuthorize SpEL" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

client -> before -> target -> after
```

**Fig. 1.** Proxy advisors wrap the join point; HTTP filters are a different stack.

`MethodSecurityInterceptor` is the **legacy** AOP Alliance interceptor (`AbstractSecurityInterceptor` + `MethodSecurityMetadataSource` / voters). It is **deprecated**; use the `AuthorizationManager*` interceptors. In Security **6+**, keeping `@EnableGlobalMethodSecurity` may require the optional `spring-security-access` module.

If the call is **not** an HTTP request, `ExceptionTranslationFilter` will not map the exception to HTTP 403 — handle `AccessDeniedException` yourself (tests, messaging, scheduled jobs).

See [[What is EnableMethodSecurity]], [[What is PreAuthorize]], and [[What is MethodSecurityInterceptor]].

## Proxy limits and URL rules

Default `mode` is **proxy**. Self-invocation (`this.readCustomer(id)`), **private** methods, and **final** methods/classes follow Spring AOP rules: the advice never runs. AspectJ mode weaves bytecode and does not have the self-call hole — [[Why does method security skip self-invocation]], [[What are Spring AOP proxy limitations]].

Request-level rules (`authorizeHttpRequests` on `SecurityFilterChain`) are **coarse** and sit on the servlet chain. Method security is **fine-grained** (parameters and return values). They **complement**; they do not replace each other. **Unannotated** methods are **not** secured by method security — keep a catch-all HTTP rule. See [[Why does method security still matter if URL rules exist]].

> [!warning] Missing `@EnableMethodSecurity` is a silent no-op
> `@PreAuthorize` on a `@Service` does nothing until method security is enabled. After a Boot **3** / Security **6** upgrade, dropping `@EnableGlobalMethodSecurity` without adding `@EnableMethodSecurity` is the usual “annotations stopped working” bug. The security starter still only wires the **filter chain**.

> [!tip] Interview answer
> Method security is Spring AOP: `@EnableMethodSecurity` registers interceptors on the bean proxy. `@PreAuthorize` runs before the method; `@PostAuthorize` after. Denial is `AccessDeniedException`. It is not the servlet filter chain, Boot does not enable it for you, and `this.secured()` skips the proxy.
