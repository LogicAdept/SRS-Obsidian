<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is hasRole in PreAuthorize versus Secured?

> [!abstract] Short answer
> **`@PreAuthorize("hasRole('ADMIN')")` is SpEL and prefixes `ROLE_`. `@Secured("ROLE_ADMIN")` is a literal authority string — no SpEL, no `hasRole()` function.** Official 7.1: `hasRole('ADMIN')` requires the `ROLE_ADMIN` authority. `@Secured({ "ROLE_USER", "ROLE_ADMIN" })` is **OR**. **AND**, method arguments, and `hasPermission` need `@PreAuthorize`. `@Secured` is legacy and off until `securedEnabled = true`.

## SpEL prefix vs literal attribute

`hasRole` on `SecurityExpressionRoot` is a shortcut for `hasAuthority` that prefixes **`ROLE_`** (or `GrantedAuthorityDefaults` / `AuthorizationManagerFactory` role prefix). `hasRole('ADMIN')` ≡ `hasAuthority('ROLE_ADMIN')`. The same prefix rule is used for HTTP `hasRole`. On Security **7**, `hasRole("ADMIN")` and `hasRole("ROLE_ADMIN")` both look for `ROLE_ADMIN` when the default prefix is `"ROLE_"`.

`@Secured` is **not** an expression. JavaDoc: a list of security configuration attributes (`ROLE_USER`, `ROLE_ADMIN`). `SecuredAuthorizationManager` copies `value()` as authority strings and `AuthoritiesAuthorizationManager` grants if the `Authentication` contains **any** of them. There is no `hasRole` call and **no** automatic `ROLE_` prefix on those strings. `@Secured("ADMIN")` looks for an authority named **`ADMIN`**, which will not match `ROLE_ADMIN`. `@Secured("hasRole('ADMIN')")` looks for an authority whose name is the characters `hasRole('ADMIN')`.

`@PreAuthorize` is on by default with `@EnableMethodSecurity`. `@Secured` needs `@EnableMethodSecurity(securedEnabled = true)`. The 7.1 reference calls `@Secured` a legacy option; `@PreAuthorize` supersedes it.

```java
@PreAuthorize("hasRole('ADMIN')")
public void writeResource() { }

@Secured("ROLE_ADMIN")
public void deleteContact() { }
```

**Listing 1.** Conceptual Security **7.1** — same intended check. SpEL adds the prefix; `@Secured` must include it in the string.

```java
@Secured({ "ROLE_USER", "ROLE_ADMIN" })
public void updateContact(Contact contact) { }

@PreAuthorize("hasRole('USER') and hasRole('ADMIN')")
public void updateContactAnd(Contact contact) { }
```

**Listing 2.** Conceptual — `@Secured` array is **OR** (any listed authority). **AND** is a SpEL operator on `@PreAuthorize`. `@Secured` cannot see `#contact`.

```d2
direction: down
pre: "@PreAuthorize(\"hasRole('ADMIN')\")\nSpEL + ROLE_ prefix" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}
sec: "@Secured(\"ROLE_ADMIN\")\nliteral authority" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
auth: "GrantedAuthority ROLE_ADMIN" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}

pre -> auth
sec -> auth
```

**Fig. 1.** Same authority, two syntaxes. See [[What is hasRole versus hasAuthority in Spring Security]], [[What is PreAuthorize]], [[What is Secured in Spring Security]], [[What is securedEnabled in method security]], [[Can PreAuthorize use method parameters]].

> [!warning] Do not put SpEL inside `@Secured`
> `@Secured("hasRole('ADMIN')")` is not `hasRole`. It is a required authority named `hasRole('ADMIN')` and never matches `ROLE_ADMIN`. `@Secured("ADMIN")` does not prefix. Multiple values are **OR**, not AND. Leaving `securedEnabled` at the default **`false`** makes `@Secured` a no-op while `@PreAuthorize("hasRole('ADMIN')")` still runs.

> [!tip] Interview answer
> `hasRole` only exists in SpEL, so `@PreAuthorize("hasRole('ADMIN')")` prefixes `ROLE_` and looks for `ROLE_ADMIN`, same idea as HTTP `hasRole`. `@Secured` is a list of literal authorities — you write `ROLE_ADMIN` yourself, there is no `hasRole()` function, and several values mean OR. Use `@PreAuthorize` when you need AND, arguments, or anything beyond an authority string.
