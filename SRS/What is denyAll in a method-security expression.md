<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #Java/Spring/Security/FilterChain #SRS

# What is denyAll in a method-security expression?

> [!abstract] Short answer
> **`denyAll` is a SpEL root field/method that always refuses the invocation.** `@PreAuthorize("denyAll")` never consults `Authentication` and never runs the target. Denial is `AccessDeniedException`. Same *name* as HTTP `anyRequest().denyAll()`, **different stack**: AOP vs `AuthorizationFilter`.

## Always false, no user lookup

On `SecurityExpressionRoot` / `MethodSecurityExpressionRoot`, `denyAll` is a `final boolean` **and** `denyAll()` returns **`false`**. Official samples use the field form: `@PreAuthorize("denyAll")`. The method is not allowed **under any circumstances**; `Authentication` is **not** retrieved from the session (same note as `permitAll`).

Typical use: retire a method that must stay on the type (`myDeprecatedMethod` in the Security **7.1** reference), or a test that must be uncallable.

JSR-250 **`@DenyAll`** is a **different** annotation. It needs `@EnableMethodSecurity(jsr250Enabled = true)` and does not use SpEL.

```java
@Component
public class MyService {

    @PreAuthorize("denyAll")
    public MyResource myDeprecatedMethod() {
        return load();
    }
}
```

**Listing 1.** Conceptual Security **7.1** — lock the method. `denyAll()` in SpEL is the same always-false method.

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/admin/**").hasRole("ADMIN")
        .anyRequest().denyAll());
```

**Listing 2.** Conceptual — HTTP catch-all. This does **not** run when a scheduler or another bean calls `MyService` directly.

```d2
direction: down
http: "authorizeHttpRequests\n.denyAll()" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
aop: "@PreAuthorize(\"denyAll\")\nmethod interceptor" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
svc: "Target method\nnever runs" {
  width: 200
  height: 45
  style.fill: "#ffcdd2"
}
job: "Job / other bean" {
  width: 160
  height: 45
  style.fill: "#e8f5e9"
}

http -> svc: "HTTP only"
job -> aop -> svc
```

**Fig. 1.** URL `denyAll` is the servlet edge. Method `denyAll` is the proxy. See [[What is permitAll in a method-security expression]], [[Why does method security still matter if URL rules exist]], [[What exception does a failed method-security check throw]], [[What is PreAuthorize]].

> [!warning] HTTP `denyAll` does not lock the service
> `AuthorizationFilter` never sees a non-HTTP call. A job or test can still invoke the `@Service` unless the **method** is denied too. Self-invocation (`this.deprecated()`) skips the proxy even with `@PreAuthorize("denyAll")`.

> [!tip] Interview answer
> Method-security `denyAll` is SpEL that always returns false and skips the method — `AccessDeniedException`, no `Authentication` lookup. HTTP `denyAll()` only closes URLs. Use `@PreAuthorize("denyAll")` to lock a bean method; `@DenyAll` is JSR-250 and needs `jsr250Enabled`.
