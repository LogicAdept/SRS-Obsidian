<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is the difference between EnableMethodSecurity and EnableGlobalMethodSecurity?

> [!abstract] Short answer
> **`@EnableMethodSecurity` is the current switch; `@EnableGlobalMethodSecurity` is the deprecated one.** New: **`prePostEnabled` defaults to `true`**, `AuthorizationManager` AOP advisors, customize with **beans**. Old: **`prePostEnabled` defaults to `false`**, `MethodSecurityInterceptor` / voters, customize by **subclassing `GlobalMethodSecurityConfiguration`**. `@EnableMethodSecurity` ≡ `@EnableGlobalMethodSecurity(prePostEnabled = true)`. Do **not** use both.

## Same job, two implementations

| | `@EnableGlobalMethodSecurity` | `@EnableMethodSecurity` |
|---|---|---|
| Status | Deprecated (since **3.2**) | Current (Security **6** / Boot **3** default path) |
| XML | `<global-method-security/>` | `<method-security/>` |
| `prePostEnabled` | **`false`** | **`true`** |
| `securedEnabled` / `jsr250Enabled` | `false` | `false` |
| Interceptors | One `MethodSecurityInterceptor` (metadata, `AccessDecisionManager`, voters) | Per-annotation `AuthorizationManagerBeforeMethodInterceptor` / `After` |
| Customize | Extend `GlobalMethodSecurityConfiguration` | Publish beans (`MethodSecurityExpressionHandler`, …) |
| `PermissionEvaluator` | Unique bean picked up on the old config class | **Not** auto-detected — `setPermissionEvaluator` on a **static** handler bean |
| 6+ / **7.1** | Types in optional **`spring-security-access`**; **7.1** fails fast without it | No access module |

Official 7.1: the new annotation uses `AuthorizationManager`, native Spring AOP, bean-based config, and turns pre/post **on** by default. Secured-only old apps must set `prePostEnabled = false` on the new annotation or they also get `@PreAuthorize`.

Mixing `@Import`s two independent selectors. Two pre/post stacks can run `@PreAuthorize` twice. Official docs do not support stacking them.

Boot **3** / Security **6**: `spring-boot-starter-security` still does **not** enable method security. Dropping the old annotation without adding `@EnableMethodSecurity` leaves `@PreAuthorize` decorative. Bare **old** annotation without `prePostEnabled = true` is the same no-op. On **7.1**, keeping only the old annotation **without** `spring-security-access` fails at startup — it is not a silent missing interceptor.

```java
@EnableGlobalMethodSecurity(prePostEnabled = true)

@EnableMethodSecurity
```

**Listing 1.** Conceptual Security **7.1** — functionally equivalent.

```java
@EnableGlobalMethodSecurity(securedEnabled = true)

@EnableMethodSecurity(securedEnabled = true, prePostEnabled = false)
```

**Listing 2.** Conceptual — secured-only. Omitting `prePostEnabled = false` on the new annotation also activates pre/post.

```d2
direction: down
old: "@EnableGlobalMethodSecurity\nprePostEnabled default false" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
neu: "@EnableMethodSecurity\nprePostEnabled default true" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}
msi: "MethodSecurityInterceptor\nvoters / GMSC" {
  width: 260
  height: 50
  style.fill: "#ffcdd2"
}
am: "AuthorizationManager*\nadvisors / beans" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}

old -> msi
neu -> am
```

**Fig. 1.** Same method AOP idea; different wiring. See [[What is EnableMethodSecurity]], [[What is EnableGlobalMethodSecurity]], [[What happens if you mix EnableMethodSecurity and EnableGlobalMethodSecurity]], [[What is GlobalMethodSecurityConfiguration]], [[What is prePostEnabled in method security]], [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]].

> [!warning] Replace, do not stack, and watch the default `false`
> The old annotation compiling on Boot **3** is not “method security is on.” Without `prePostEnabled = true` (old) or `@EnableMethodSecurity` (new), `@PreAuthorize` does nothing. **7.1** old annotation without `spring-security-access` fails fast. Two enable annotations are two interceptor families — delete the old one and any `GlobalMethodSecurityConfiguration` subclass.

> [!tip] Interview answer
> `@EnableGlobalMethodSecurity` is the old, deprecated switch: `prePostEnabled` defaulted to false and it wired `MethodSecurityInterceptor` via `GlobalMethodSecurityConfiguration`. `@EnableMethodSecurity` is the replacement: pre/post is on by default and it uses `AuthorizationManager` advisors you customize with beans. They are not both needed — migrate, do not mix — and a Boot 3 upgrade that drops the old annotation without adding the new one leaves method security off.
