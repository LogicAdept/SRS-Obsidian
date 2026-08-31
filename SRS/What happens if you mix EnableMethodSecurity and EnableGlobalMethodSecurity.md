<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What happens if you mix EnableMethodSecurity and EnableGlobalMethodSecurity?

> [!abstract] Short answer
> **They are replacements, not layers.** `@EnableMethodSecurity` **supersedes** deprecated `@EnableGlobalMethodSecurity`. Each annotation `@Import`s a **different** selector (`MethodSecuritySelector` vs `GlobalMethodSecuritySelector`). Mixing them registers **two independent AOP stacks** on the same context. Keep **only** `@EnableMethodSecurity`.

## Two selectors, two interceptor families

| | `@EnableMethodSecurity` (since 5.6) | `@EnableGlobalMethodSecurity` (deprecated) |
|---|---|---|
| Import | `MethodSecuritySelector` | `GlobalMethodSecuritySelector` |
| Pre/post default | `prePostEnabled = true` | `prePostEnabled = false` |
| Interceptors | `AuthorizationManagerBeforeMethodInterceptor` / `After…` | Legacy `MethodSecurityInterceptor` + `MethodSecurityMetadataSourceAdvisor` |
| Extra module | No | Security **6+** needs optional `spring-security-access` |

There is **no** mutual exclusion in those selectors. Both `@Configuration` classes can be scanned; both import lists run.

On Security **7.1**, `@EnableGlobalMethodSecurity` **fails fast** if `spring-security-access` is missing (`IllegalStateException`: add that module **or migrate**). Typical Boot **3** / Security **6** apps do **not** have that module, so the mix often **does not start** rather than “silently ignore `@PreAuthorize`.” Silent no-op is dropping the old annotation **without** adding the new one — [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]], [[What happens if MethodSecurityInterceptor is missing]].

If the access module **is** present and **both** enable pre/post (`@EnableGlobalMethodSecurity(prePostEnabled = true)` plus `@EnableMethodSecurity`), the same `@PreAuthorize` join point gets **two** advisors. Method security evaluates matching interceptors **in series**; both must pass. That is duplicate work and two expression-handler pipelines (`AuthorizationManager` vs metadata/voters), not a merge.

```java
// Wrong — two stacks
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
@EnableMethodSecurity
class MixedMethodSecurityConfig {
}
```

**Listing 1.** Conceptual — do not do this. Remove the deprecated annotation and any `GlobalMethodSecurityConfiguration` subclass.

```java
@Configuration
@EnableMethodSecurity // pre/post on; add securedEnabled / jsr250Enabled if you still need those
class MethodSecurityConfig {
}
```

**Listing 2.** Conceptual Security **7.1** replacement. `@EnableGlobalMethodSecurity(prePostEnabled = true)` ≡ `@EnableMethodSecurity` with no attributes.

```d2
direction: down
ems: "@EnableMethodSecurity\nMethodSecuritySelector" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
egms: "@EnableGlobalMethodSecurity\nGlobalMethodSecuritySelector" {
  width: 280
  height: 55
  style.fill: "#ffcdd2"
}
new: "AuthorizationManager* advisors" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
old: "MethodSecurityInterceptor\n(needs spring-security-access)" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}

ems -> new
egms -> old
```

**Fig. 1.** Parallel imports, not an override. After migration, **absence** of `MethodSecurityInterceptor` is expected — [[What is EnableMethodSecurity]], [[What is EnableGlobalMethodSecurity]], [[What is the difference between EnableMethodSecurity and EnableGlobalMethodSecurity]].

> [!warning] Defaults do not mean the same thing
> Bare `@EnableGlobalMethodSecurity` does **not** turn on `@PreAuthorize`. Bare `@EnableMethodSecurity` does. Adding the new annotation beside an old one that still has `prePostEnabled = false` looks “mixed” but only the **new** stack enforces pre/post — until you also set `prePostEnabled = true` on the old one and get **double** interceptors. Do not treat a leftover import as a SpEL bug.

> [!tip] Interview answer
> Do not mix them. `@EnableMethodSecurity` replaced `@EnableGlobalMethodSecurity` and they import different interceptors. Without `spring-security-access` the old annotation fails at startup on current Security; if both pre/post stacks are on, `@PreAuthorize` can run twice. Delete the old annotation and any `GlobalMethodSecurityConfiguration` subclass.
