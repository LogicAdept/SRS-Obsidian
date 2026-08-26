<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the difference between Secured RolesAllowed and PreAuthorize?

> [!abstract] Short answer
> All three are **before-method** AOP checks. **`@PreAuthorize`** takes **SpEL** (arguments, `and`/`or`, `authentication`) and is **on by default** with `@EnableMethodSecurity`. **`@Secured`** (Spring) and **`@RolesAllowed`** (JSR-250) take **role/authority names only** — no SpEL — and stay **off** until `securedEnabled` / `jsr250Enabled`. Spring documents `@PreAuthorize` as the recommended replacement.

## What you write vs what is enabled

| | `@PreAuthorize` | `@Secured` | `@RolesAllowed` |
|---|---|---|---|
| Spec | Spring Security (3.0+) | Spring `@Secured` | JSR-250 / Jakarta (`@PermitAll`, `@DenyAll` too) |
| Payload | SpEL `value` | `String[]` attributes | `String[]` role names |
| Enable | `prePostEnabled` **true** | `securedEnabled` **false** | `jsr250Enabled` **false** |
| Interceptor | `AuthorizationManagerBeforeMethodInterceptor.preAuthorize()` | `.secured()` → `SecuredAuthorizationManager` | `.jsr250()` → `Jsr250AuthorizationManager` |
| Docs stance | Recommended | Legacy; `@PreAuthorize` supersedes it | Supported; `@PreAuthorize` has more power |

SpEL also lives on `@PostAuthorize`, `@PreFilter`, and `@PostFilter`. `@Secured` and `@RolesAllowed` cannot express those.

```java
@EnableMethodSecurity(securedEnabled = true, jsr250Enabled = true)
public class MethodSecurityConfig {
}

@PreAuthorize("hasAuthority('order:read') and #id == authentication.name")
public Order read(String id) { ... }

@Secured({ "ROLE_USER", "ROLE_ADMIN" })
public void update(Order order) { ... }

@RolesAllowed("ADMIN")
public void delete(Order order) { ... }
```

**Listing 1.** Conceptual — pre/post is already on; the other two flags are extra. `@Secured` values are **literal** authority strings (examples use `ROLE_USER`). `@RolesAllowed("ADMIN")` is prefixed to `ROLE_ADMIN` by `Jsr250AuthorizationManager` (default prefix `ROLE_`).

Default matcher for both `@Secured` and `@RolesAllowed` is `AuthoritiesAuthorizationManager`: the `Authentication` needs **any one** of the listed authorities (OR), not all of them. `@PreAuthorize` can require **all** with `and` / `hasAllAuthorities`.

```d2
direction: down
pre: "@PreAuthorize\nSpEL, default on" {
  width: 220
  height: 60
  style.fill: "#c8e6c9"
}
sec: "@Secured\nexact authority strings" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
jsr: "@RolesAllowed\nROLE_ prefix + names" {
  width: 220
  height: 60
  style.fill: "#ffe0b2"
}
aop: "Spring AOP before interceptor\nAccessDeniedException" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}

pre -> aop
sec -> aop
jsr -> aop
```

**Fig. 1.** Same proxy boundary; different metadata and enablement. See [[What is PreAuthorize]], [[What is EnableMethodSecurity]], and [[How does method security work in Spring]].

> [!warning] Prefix and enablement traps
> `@Secured("ADMIN")` looks for authority **`ADMIN`**, not `ROLE_ADMIN`. `@RolesAllowed("ADMIN")` looks for **`ROLE_ADMIN`**. `hasRole('ADMIN')` in `@PreAuthorize` also applies the default `ROLE_` prefix. After Boot **3**, dropping `@EnableGlobalMethodSecurity` without `@EnableMethodSecurity` makes `@PreAuthorize` a no-op — [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]]. All three skip `this.secured()` in proxy mode — [[Why does method security skip self-invocation]].

> [!tip] Interview answer
> `@PreAuthorize` is SpEL before the method and is enabled by default. `@Secured` and `@RolesAllowed` only check authorities and need extra flags. Prefer `@PreAuthorize`; remember `@Secured` does not add `ROLE_` while `@RolesAllowed` does.
