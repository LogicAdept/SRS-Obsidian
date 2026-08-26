<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# What is MethodSecurityInterceptor?

> [!abstract] Short answer
> **`MethodSecurityInterceptor`** is the **legacy** AOP Alliance `MethodInterceptor` that used to wrap secured bean methods. It extends **`AbstractSecurityInterceptor`**: look up `ConfigAttribute`s from a `MethodSecurityMetadataSource`, decide with an `AccessDecisionManager` (voters), optionally `RunAsManager`, proceed, then `AfterInvocationManager`. It is **deprecated**. Use `AuthorizationManagerBeforeMethodInterceptor` and `AuthorizationManagerAfterMethodInterceptor` instead.

## Old workflow

`invoke(MethodInvocation)` is the AOP Alliance entry. The parent `AbstractSecurityInterceptor` (also deprecated) then:

1. Reads `Authentication` from `SecurityContextHolder`.
2. Asks `MethodSecurityMetadataSource` whether this invocation is secured (`ConfigAttribute` list) or public (empty).
3. For a secured call: optionally re-authenticate, run `AccessDecisionManager`, apply `RunAsManager`, then **proceed** with the join point.
4. After the target returns: restore run-as if needed; `AfterInvocationManager` may replace the return value (post-invocation checks / filtering in the old model).

Subclass `AspectJMethodSecurityInterceptor` is the same interceptor for AspectJ join points. Both share `MethodSecurityMetadataSource` because they work on Java `Method`s.

This is the stack behind deprecated **`@EnableGlobalMethodSecurity`** / `GlobalMethodSecurityConfiguration` (metadata sources, attributes, decision managers, voters). Customizing meant **subclassing** that configuration class.

```java
// Conceptual — do not add this bean in new code
MethodSecurityInterceptor interceptor = new MethodSecurityInterceptor();
interceptor.setSecurityMetadataSource(methodSecurityMetadataSource);
interceptor.setAccessDecisionManager(accessDecisionManager);
```

**Listing 1.** Conceptual legacy wiring. The interceptor is a single around-advice that both **denies before** and **rewrites after** via collaborators.

## What replaced it (Security 5.6+, default in 6)

`@EnableMethodSecurity` publishes **native Spring AOP `Advisor`s**, one interceptor per annotation, each holding an `AuthorizationManager`:

| Annotation | Replacement |
|---|---|
| `@PreAuthorize` | `AuthorizationManagerBeforeMethodInterceptor.preAuthorize()` → `PreAuthorizeAuthorizationManager` |
| `@PostAuthorize` | `AuthorizationManagerAfterMethodInterceptor.postAuthorize()` |
| `@Secured` / JSR-250 | `AuthorizationManagerBeforeMethodInterceptor.secured()` / `.jsr250()` (flags off by default) |

Denial is still `AccessDeniedException`. There is **no** `MethodSecurityInterceptor` on this path. If you keep `@EnableGlobalMethodSecurity` on Security **6+**, you may need the optional **`spring-security-access`** module so the old types remain on the classpath. Prefer migrating: `@EnableGlobalMethodSecurity(prePostEnabled = true)` ≡ `@EnableMethodSecurity`.

```d2
direction: right
legacy: "MethodSecurityInterceptor\nMetadataSource + voters" {
  width: 240
  height: 70
  style.fill: "#ffcdd2"
}
modern: "AuthorizationManager*\nMethodInterceptor advisors" {
  width: 250
  height: 70
  style.fill: "#c8e6c9"
}
proxy: "Spring AOP proxy" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}

legacy -> proxy: "deprecated"
modern -> proxy: "@EnableMethodSecurity"
```

**Fig. 1.** Same proxy boundary; different interceptor API. See [[How does method security work in Spring]], [[What is EnableMethodSecurity]], and [[What is an Advisor in Spring AOP]].

> [!warning] Interview wording vs current code
> Saying “method security is `MethodSecurityInterceptor`” describes **Security 5-era / `@EnableGlobalMethodSecurity`** code. On `@EnableMethodSecurity`, look for `AuthorizationManagerBeforeMethodInterceptor` beans instead. A “missing interceptor” after a Boot **3** upgrade is usually **no `@EnableMethodSecurity` at all** (annotations compile, advisors never register) — not a missing `MethodSecurityInterceptor` class. Official docs do **not** document a supported “old + new enable annotations on the same app” setup; migrate, do not stack them.

> [!tip] Interview answer
> `MethodSecurityInterceptor` was the old around-interceptor: metadata source, voters, then proceed. It is deprecated. `@EnableMethodSecurity` registers `AuthorizationManager` before/after interceptors as Spring AOP advisors instead. Same proxy limits still apply.
