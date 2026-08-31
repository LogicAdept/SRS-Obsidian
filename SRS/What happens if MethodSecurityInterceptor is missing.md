<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# What happens if MethodSecurityInterceptor is missing?

> [!abstract] Short answer
> **`@PreAuthorize` still compiles, but nothing enforces it** — the annotation is decorative. That is silent: no startup error, admin methods stay open. After `@EnableMethodSecurity`, **`MethodSecurityInterceptor` is supposed to be absent** (deprecated). Look for **`AuthorizationManagerBeforeMethodInterceptor`** / **`AuthorizationManagerAfterMethodInterceptor`**, not the old bean.

## Two different “missing”

`MethodSecurityInterceptor` is the **legacy** AOP Alliance interceptor (`AbstractSecurityInterceptor` + `MethodSecurityMetadataSource`). It is **deprecated**; use `AuthorizationManagerBeforeMethodInterceptor` and `AuthorizationManagerAfterMethodInterceptor`. `@EnableMethodSecurity` publishes those advisors (pre/post on by default). It does **not** register `MethodSecurityInterceptor`. Hunting for that class after a Boot **3** / Security **6** migration is a false alarm.

What actually leaves methods open is **no method-security advisor at all**:

- `spring-boot-starter-security` **does not** turn method security on
- `@EnableGlobalMethodSecurity` dropped without `@EnableMethodSecurity`
- `@EnableMethodSecurity(prePostEnabled = false)` with no replacement `AuthorizationManagerBeforeMethodInterceptor.preAuthorize()` `@Bean`
- Keeping `@EnableGlobalMethodSecurity` on Security **6+** without the optional `spring-security-access` module (that path needs the old types on the classpath — migrate instead)

`@PreAuthorize` is a runtime annotation, not a bean. Nothing at startup checks that an interceptor matches it.

```java
// Compiles with or without method security — enforcement needs an advisor
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(String id) { /* ... */ }
```

**Listing 1.** Conceptual — the annotation is metadata. Without `@EnableMethodSecurity` (or an equivalent `Advisor` `@Bean`), the call is a raw method invocation.

```java
@Bean
@Role(BeanDefinition.ROLE_INFRASTRUCTURE)
static Advisor preAuthorizeMethodInterceptor() {
    return AuthorizationManagerBeforeMethodInterceptor.preAuthorize();
}
```

**Listing 2.** Conceptual Security **7.1** — this is what `@EnableMethodSecurity` publishes for `@PreAuthorize`. This is the bean to look for, not `MethodSecurityInterceptor`.

```d2
direction: down
ann: "@PreAuthorize on @Service" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
miss: "No EnableMethodSecurity\nno AuthorizationManager* advisor" {
  width: 280
  height: 55
  style.fill: "#ffcdd2"
}
ok: "AuthorizationManagerBeforeMethodInterceptor\nAccessDeniedException" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

ann -> miss: "call proceeds"
ann -> ok: "check runs"
```

**Fig. 1.** Missing interceptor is a silent allow, not a boot failure. See [[What is MethodSecurityInterceptor]], [[What is EnableMethodSecurity]], [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]], [[How does method security work in Spring]].

> [!warning] Do not grep for the deprecated class after migrating
> A context with `@EnableMethodSecurity` and **no** `MethodSecurityInterceptor` is **healthy**. Confirm an `AuthorizationManagerBeforeMethodInterceptor` (or that `@EnableMethodSecurity` is on a scanned `@Configuration`). Self-invocation and private methods also skip the proxy — that looks like a missing interceptor but is AOP, not a missing bean.

> [!tip] Interview answer
> If there is no method-security interceptor, `@PreAuthorize` is a no-op and there is no startup error. `MethodSecurityInterceptor` itself is deprecated — `@EnableMethodSecurity` registers `AuthorizationManagerBeforeMethodInterceptor` instead. After Boot 3, dropping `@EnableGlobalMethodSecurity` without adding `@EnableMethodSecurity` is the usual way this happens; the security starter does not enable method security for you.
