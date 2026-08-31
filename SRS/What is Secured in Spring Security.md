<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is Secured in Spring Security?

> [!abstract] Short answer
> **`@Secured` is Spring’s legacy method annotation for a list of authority strings.** No SpEL, no `#param`. `@Secured("ROLE_ADMIN")` looks up that **literal** `GrantedAuthority`. Enable with **`securedEnabled = true`** (default **`false`**). Several values are **OR**. Prefer `@PreAuthorize` for AND, `hasRole`, or arguments. The 7.1 reference calls `@Secured` legacy; `@PreAuthorize` supersedes it.

## Literal attributes, not expressions

Package: `org.springframework.security.access.annotation.Secured`. JavaDoc: a list of security configuration attributes (`ROLE_USER`, `ROLE_ADMIN`). `@EnableMethodSecurity(securedEnabled = true)` (XML: `secured-enabled="true"`) publishes `AuthorizationManagerBeforeMethodInterceptor.secured()` / `SecuredAuthorizationManager`. That manager copies `value()` and `AuthoritiesAuthorizationManager` grants if the `Authentication` contains **any** of them.

There is **no** `hasRole()` call and **no** automatic `ROLE_` prefix. `@Secured("ADMIN")` looks for `ADMIN`, not `ROLE_ADMIN`. `@Secured("hasRole('ADMIN')")` looks for an authority named `hasRole('ADMIN')`. `@Secured` cannot see method parameters; `@PreAuthorize("#id == authentication.name")` can.

Same *power class* as Jakarta `@RolesAllowed`, opposite prefix habit: `@RolesAllowed("ADMIN")` → `ROLE_ADMIN`; `@Secured` wants the full string. `@RolesAllowed` needs `jsr250Enabled`, not this flag.

```java
@Configuration
@EnableMethodSecurity(securedEnabled = true)
public class MethodSecurityConfig {
}
```

**Listing 1.** Conceptual Security **7.1**. Pre/post stays **on** unless you also set `prePostEnabled = false`.

```java
@Secured("ROLE_ADMIN")
public void delete(Contact contact) { }

@Secured({ "ROLE_USER", "ROLE_ADMIN" })
public void update(Contact contact) { }

@PreAuthorize("hasRole('USER') and hasRole('ADMIN')")
public void updateAnd(Contact contact) { }
```

**Listing 2.** Conceptual — array is **OR**. **AND** needs `@PreAuthorize`. `#contact` is invisible to `@Secured`.

```d2
direction: down
ann: "@Secured(\"ROLE_ADMIN\")\nliteral attribute" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
flag: "securedEnabled = true" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
auth: "GrantedAuthority ROLE_ADMIN" {
  width: 240
  height: 45
  style.fill: "#c8e6c9"
}

flag -> ann
ann -> auth: "no extra prefix"
```

**Fig. 1.** Spring annotation; still off until the flag. See [[What is securedEnabled in method security]], [[What is hasRole in PreAuthorize versus Secured]], [[What is RolesAllowed in Spring Security]], [[What is PreAuthorize]], [[Can PreAuthorize use method parameters]].

> [!warning] Not SpEL, and default `false`
> `@Secured("hasRole('ADMIN')")` is not `hasRole`. Forgetting `securedEnabled` leaves `@Secured` decorative while `@PreAuthorize` still runs. `@Secured("ADMIN")` does not prefix. Multiple values are OR, never AND.

> [!tip] Interview answer
> `@Secured` is Spring’s old method annotation: a list of literal authorities like `ROLE_ADMIN`, no SpEL and no method parameters. You must set `securedEnabled = true`. Several values mean OR. Use `@PreAuthorize` when you need AND, `hasRole`, or `#param`.
