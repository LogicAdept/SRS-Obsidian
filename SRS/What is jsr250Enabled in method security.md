<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is jsr250Enabled in method security?

> [!abstract] Short answer
> **`jsr250Enabled = true` turns on JSR-250 method annotations: `@RolesAllowed`, `@PermitAll`, and `@DenyAll`.** It is **`false` by default** on both `@EnableMethodSecurity` and deprecated `@EnableGlobalMethodSecurity`. Bare `@EnableMethodSecurity` enables **pre/post SpEL only** — `@RolesAllowed` stays decorative until you flip this flag. `@RolesAllowed` is role strings, **not** SpEL.

## What the flag publishes

`@EnableMethodSecurity(jsr250Enabled = true)` (XML: `<sec:method-security jsr250-enabled="true"/>`) registers `AuthorizationManagerBeforeMethodInterceptor.jsr250()`, which uses `Jsr250AuthorizationManager`. Deprecated XML was `<global-method-security jsr250-annotations="enabled"/>` next to `@EnableGlobalMethodSecurity(jsr250Enabled = true)`.

| Annotation (`jakarta.annotation.security`) | Effect |
|---|---|
| `@RolesAllowed("ADMIN")` | Any listed role, after prefixing **`ROLE_`** → authority `ROLE_ADMIN` |
| `@PermitAll` | Always allow |
| `@DenyAll` | Always deny |

Several values on `@RolesAllowed` are **OR** (same `AuthoritiesAuthorizationManager` as `@Secured`). There is **no** SpEL, **no** `#param`, **no** `hasPermission`. `@PreAuthorize` remains the more expressive option; the 7.1 reference recommends it.

`Jsr250AuthorizationManager` **always concatenates** the role prefix (default `"ROLE_"`) onto each `@RolesAllowed` value. `@RolesAllowed("ADMIN")` is correct. `@RolesAllowed("ROLE_ADMIN")` looks for **`ROLE_ROLE_ADMIN`**. That is stricter than Security **7** `hasRole("ROLE_ADMIN")`, which still maps to `ROLE_ADMIN`.

JSR-250 `@PermitAll` / `@DenyAll` are **not** the SpEL fields `permitAll` / `denyAll` on `@PreAuthorize`. Those SpEL forms do **not** need this flag.

```java
@Configuration
@EnableMethodSecurity(jsr250Enabled = true)
public class MethodSecurityConfig {
}
```

**Listing 1.** Conceptual Security **7.1**. `prePostEnabled` stays **`true`**; this only **adds** the JSR-250 interceptor.

```java
public interface ContactService {

    @RolesAllowed("USER")
    void create(Contact contact);

    @RolesAllowed({ "USER", "ADMIN" })
    void update(Contact contact);

    @DenyAll
    void retire();
}
```

**Listing 2.** Conceptual — `@RolesAllowed("USER")` requires `ROLE_USER`. The array is OR. No `#contact`.

```d2
direction: down
flag: "jsr250Enabled = true\n(default false)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
adv: "AuthorizationManagerBeforeMethodInterceptor.jsr250" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
ann: "@RolesAllowed / @PermitAll / @DenyAll" {
  width: 280
  height: 45
  style.fill: "#c8e6c9"
}

flag -> adv
adv -> ann
```

**Fig. 1.** Off until the flag is set. See [[What is EnableMethodSecurity]], [[What is RolesAllowed in Spring Security]], [[What is denyAll in a method-security expression]], [[What is permitAll in a method-security expression]], [[What is securedEnabled in method security]].

> [!warning] Default `false`, and do not write `ROLE_` in `@RolesAllowed`
> `@EnableMethodSecurity` does **not** turn on `@RolesAllowed`. Forgetting `jsr250Enabled` is a silent open method. `@RolesAllowed("ROLE_ADMIN")` double-prefixes. `@PreAuthorize("hasRole('ADMIN')")` and JSR-250 `@DenyAll` are different stacks — do not assume the SpEL names enable these annotations.

> [!tip] Interview answer
> `jsr250Enabled` is the switch for JSR-250 `@RolesAllowed`, `@PermitAll`, and `@DenyAll`. It defaults to false on `@EnableMethodSecurity`, so you must set it. `@RolesAllowed("ADMIN")` prefixes `ROLE_` and is not SpEL — write the short role name, not `ROLE_ADMIN`. Prefer `@PreAuthorize` when you need expressions or method arguments.
