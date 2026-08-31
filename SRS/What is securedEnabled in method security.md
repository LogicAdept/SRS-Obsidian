<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is securedEnabled in method security?

> [!abstract] Short answer
> **`securedEnabled = true` turns on Spring’s `@Secured`.** It is **`false` by default** on both `@EnableMethodSecurity` and deprecated `@EnableGlobalMethodSecurity`. Bare `@EnableMethodSecurity` enables **pre/post SpEL only** — `@Secured` stays decorative until you flip this flag. `@Secured` is literal authority strings, **not** SpEL.

## What the flag publishes

`@EnableMethodSecurity(securedEnabled = true)` (XML: `<sec:method-security secured-enabled="true"/>`) registers `AuthorizationManagerBeforeMethodInterceptor.secured()`, which uses `SecuredAuthorizationManager`. Legacy XML: `<global-method-security secured-enabled="true"/>` next to `@EnableGlobalMethodSecurity(securedEnabled = true)`.

`@Secured("ROLE_ADMIN")` matches that **exact** `GrantedAuthority`. There is no `hasRole()` prefixing. Several values are **OR**. **AND** of two roles needs `@PreAuthorize("hasRole('A') and hasRole('B')")`. No `#param`, no `hasPermission`, no `@PreFilter`.

Official 7.1 migration: old **`@EnableGlobalMethodSecurity(securedEnabled = true)`** (pre/post still **off**) must become **`@EnableMethodSecurity(securedEnabled = true, prePostEnabled = false)`**. Leaving `prePostEnabled` at the new default **`true`** also activates `@PreAuthorize` / filters.

This flag does **not** enable `@RolesAllowed` (`jsr250Enabled`) and does **not** enable pre/post. `spring-boot-starter-security` still does not turn method security on by itself.

```java
@Configuration
@EnableMethodSecurity(securedEnabled = true)
public class MethodSecurityConfig {
}
```

**Listing 1.** Conceptual Security **7.1**. `prePostEnabled` stays **`true`**; this only **adds** the `@Secured` interceptor.

```java
@Configuration
@EnableMethodSecurity(securedEnabled = true, prePostEnabled = false)
public class SecuredOnlyConfig {
}
```

**Listing 2.** Conceptual — equivalent of old `@EnableGlobalMethodSecurity(securedEnabled = true)` without accidentally turning pre/post on.

```d2
direction: down
flag: "securedEnabled = true\n(default false)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
adv: "AuthorizationManagerBeforeMethodInterceptor.secured" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
ann: "@Secured(\"ROLE_ADMIN\")" {
  width: 240
  height: 45
  style.fill: "#c8e6c9"
}

flag -> adv
adv -> ann
```

**Fig. 1.** Off until the flag is set. See [[What is Secured in Spring Security]], [[What is EnableMethodSecurity]], [[What is prePostEnabled in method security]], [[What is jsr250Enabled in method security]], [[What is hasRole in PreAuthorize versus Secured]].

> [!warning] Default `false`, and `@Secured` is not `hasRole`
> Forgetting `securedEnabled` is a silent open `@Secured` method. `@Secured({"ROLE_A", "ROLE_B"})` is **OR**. `@Secured("hasRole('ADMIN')")` looks up that literal string. Migrating a secured-only app to `@EnableMethodSecurity` without `prePostEnabled = false` also turns on SpEL annotations you never had.

> [!tip] Interview answer
> `securedEnabled` is the switch for `@Secured`. It defaults to false on `@EnableMethodSecurity`, so you must set it. `@Secured` takes literal authorities like `ROLE_ADMIN` — no SpEL, and several values mean OR. If you used only `@Secured` on the old annotation, set `prePostEnabled = false` when you migrate so you do not also enable `@PreAuthorize`.
