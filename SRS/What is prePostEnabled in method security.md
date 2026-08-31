<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is prePostEnabled in method security?

> [!abstract] Short answer
> **`prePostEnabled` is the switch for `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, and `@PostFilter`.** On **`@EnableMethodSecurity` it defaults to `true`**. On deprecated **`@EnableGlobalMethodSecurity` it defaulted to `false`**. Bare `@EnableGlobalMethodSecurity` leaves those annotations decorative. `@EnableMethodSecurity` ≡ old `@EnableGlobalMethodSecurity(prePostEnabled = true)`.

## What the flag publishes

`true` registers the four pre/post AOP interceptors (`AuthorizationManagerBeforeMethodInterceptor` / `After` for authorize and filter). XML: `pre-post-enabled` on `<method-security>` (legacy `<global-method-security>`). It does **not** turn on `@Secured` or JSR-250 — those are `securedEnabled` / `jsr250Enabled`.

Official 7.1 migration: `@EnableGlobalMethodSecurity(prePostEnabled = true)` and `@EnableMethodSecurity` are functionally equivalent. If you only used `@Secured`, move to `@EnableMethodSecurity(securedEnabled = true, prePostEnabled = false)` or the new annotation would also activate pre/post.

Set `prePostEnabled = false` when you replace the defaults with your own advisors (for example only `@PostAuthorize`). `spring-boot-starter-security` still does **not** enable method security by itself.

```java
@Configuration
@EnableGlobalMethodSecurity   // prePostEnabled default false
public class OldConfig {
}
```

**Listing 1.** Conceptual — `@PreAuthorize` is a no-op. The old dump trap is copying this with no attributes.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
}

@Configuration
@EnableMethodSecurity(securedEnabled = true, prePostEnabled = false)
public class SecuredOnlyConfig {
}
```

**Listing 2.** Conceptual Security **7.1** — first form is the usual replacement (pre/post **on**). Second form is old `securedEnabled = true` only.

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
ann: "@PreAuthorize @PostAuthorize\n@PreFilter @PostFilter" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}

old -> ann: "off until true"
neu -> ann: "on"
```

**Fig. 1.** Same four annotations; opposite defaults. See [[What is EnableMethodSecurity]], [[What is EnableGlobalMethodSecurity]], [[What is PreAuthorize]], [[What is PostAuthorize in Spring Security]], [[What is PreFilter and PostFilter in Spring Security]], [[What is securedEnabled in method security]].

> [!warning] Boot 3 plus the old default `false`
> After Boot **3**, dropping `@EnableGlobalMethodSecurity` without adding `@EnableMethodSecurity` is silent open methods. Leaving the **old** annotation with no `prePostEnabled = true` is the same no-op. Do not mix the two enable annotations. `@Secured` / `@RolesAllowed` are **not** this flag.

> [!tip] Interview answer
> `prePostEnabled` turns on the four SpEL method annotations. It defaulted to false on `@EnableGlobalMethodSecurity`, which is why a bare old annotation left `@PreAuthorize` doing nothing. `@EnableMethodSecurity` defaults it to true, so you only set it to false when you want `@Secured` or custom interceptors without pre/post.
