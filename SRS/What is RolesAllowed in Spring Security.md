<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is RolesAllowed in Spring Security?

> [!abstract] Short answer
> **`@RolesAllowed` is the Jakarta (JSR-250) role annotation.** It is not a Spring type. Spring Security honors it only when **`jsr250Enabled = true`**. `@RolesAllowed("ADMIN")` means authority **`ROLE_ADMIN`** — the manager **always prefixes** `ROLE_`. No SpEL, no method arguments. `@PreAuthorize("hasRole('ADMIN')")` is the more powerful Spring spelling.

## Jakarta annotation, Spring interceptor

Package: `jakarta.annotation.security.RolesAllowed` (`TYPE` and `METHOD`). Jakarta: a list of security **role names**; method-level overrides class-level if they conflict. Spring Security does not ship a replacement annotation.

`@EnableMethodSecurity(jsr250Enabled = true)` publishes `AuthorizationManagerBeforeMethodInterceptor.jsr250()` / `Jsr250AuthorizationManager`. Default **`jsr250Enabled` is `false`** — the annotation compiling on the method is not enough. Same flag on deprecated `@EnableGlobalMethodSecurity`.

`Jsr250AuthorizationManager` concatenates the role prefix (default `"ROLE_"`) onto **each** `value()`. Several roles are **OR** (any listed authority). `@PermitAll` / `@DenyAll` ride the same interceptor; they are not `@RolesAllowed`.

That is the same *power class* as `@Secured`: role/authority strings, no expressions. Differences that interviews hit:

| Annotation | Flag | What you write | Matched authority |
|---|---|---|---|
| `@RolesAllowed("ADMIN")` | `jsr250Enabled` | short role name | `ROLE_ADMIN` |
| `@Secured("ROLE_ADMIN")` | `securedEnabled` | full authority | `ROLE_ADMIN` (no extra prefix) |
| `@PreAuthorize("hasRole('ADMIN')")` | `prePostEnabled` (default **true**) | SpEL | `ROLE_ADMIN` |

`@RolesAllowed("ROLE_ADMIN")` looks for **`ROLE_ROLE_ADMIN`**. Security **7** `hasRole("ROLE_ADMIN")` does **not** double-prefix.

```java
@Configuration
@EnableMethodSecurity(jsr250Enabled = true)
public class MethodSecurityConfig {
}
```

**Listing 1.** Conceptual Security **7.1** — without this flag, `@RolesAllowed` is decorative.

```java
@RolesAllowed("USER")
void create(Contact contact);

@RolesAllowed({ "USER", "ADMIN" })
void update(Contact contact);

@Secured("ROLE_ADMIN")
void delete(Contact contact);

@PreAuthorize("hasRole('ADMIN') and #contact.owner == authentication.name")
void transfer(Contact contact);
```

**Listing 2.** Conceptual — `@RolesAllowed` array is OR. `#contact` only works on `@PreAuthorize`.

```d2
direction: down
jak: "jakarta.annotation.security\n@RolesAllowed(\"ADMIN\")" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
flag: "jsr250Enabled = true" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
auth: "GrantedAuthority ROLE_ADMIN" {
  width: 240
  height: 45
  style.fill: "#c8e6c9"
}

flag -> jak
jak -> auth: "prefix ROLE_"
```

**Fig. 1.** Standard annotation; Spring only if the flag is on. See [[What is jsr250Enabled in method security]], [[What is Secured in Spring Security]], [[What is hasRole in PreAuthorize versus Secured]], [[What is PreAuthorize]], [[What is EnableMethodSecurity]].

> [!warning] Default `false`, and do not write `ROLE_` in the value
> Forgetting `jsr250Enabled` is a silent open method. `@RolesAllowed("ROLE_ADMIN")` double-prefixes. `@RolesAllowed` cannot see parameters or `hasPermission`. Class-level roles apply to every method until a method-level `@RolesAllowed` overrides them.

> [!tip] Interview answer
> `@RolesAllowed` is JSR-250 / Jakarta, not a Spring annotation. Spring Security enforces it only with `jsr250Enabled = true`, and it prefixes `ROLE_` onto the short name. It is role-only, like `@Secured` but with the opposite prefix convention. Use `@PreAuthorize` when you need SpEL or method arguments.
