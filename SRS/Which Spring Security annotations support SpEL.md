<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# Which Spring Security annotations support SpEL?

> [!abstract] Short answer
> **Four: `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, and `@PostFilter`.** `@Secured` and JSR-250 `@RolesAllowed` / `@PermitAll` / `@DenyAll` do **not**. `@Secured("hasRole('ADMIN')")` is a literal authority named `hasRole('ADMIN')`. `@EnableMethodSecurity` turns the four SpEL annotations **on by default**; `securedEnabled` / `jsr250Enabled` are extra flags.

## SpEL vs attribute lists

The 7.1 method-security page evaluates those four with `MethodSecurityExpressionHandler` / `MethodSecurityExpressionRoot` (`hasRole`, `authentication`, `returnObject`, `filterObject`, …). Each may be a meta-annotation and may sit on a type. They need **`prePostEnabled`** (default **`true`** on `@EnableMethodSecurity`; default **`false`** on deprecated `@EnableGlobalMethodSecurity`).

| Annotation | SpEL? | What `value` is |
|---|---|---|
| `@PreAuthorize` | Yes | Expression before invoke |
| `@PostAuthorize` | Yes | Expression after return (`returnObject`) |
| `@PreFilter` / `@PostFilter` | Yes | Per-element `filterObject` |
| `@Secured` | **No** | Literal authorities (`ROLE_ADMIN`); **OR** |
| `@RolesAllowed` | **No** | Role names; Spring prefixes `ROLE_` |
| `@PermitAll` / `@DenyAll` (Jakarta) | **No** | Always allow / deny |

`@EnableMethodSecurity`, `@EnableWebSecurity`, `@AuthenticationPrincipal`, `@AuthorizeReturnObject` are not SpEL annotations. Spring Data `@Query("… ?#{ principal?.id }")` uses `SecurityEvaluationContextExtension` — that is **not** a Spring Security annotation.

HTTP `authorizeHttpRequests` can use the same *expression language* in other APIs; it is not these four annotations.

```java
@PreAuthorize("hasRole('ADMIN') and #id == authentication.name")
@PostAuthorize("returnObject.owner == authentication.name")
@PreFilter("filterObject.owner == authentication.name")
@PostFilter("filterObject.owner == authentication.name")
```

**Listing 1.** Conceptual Security **7.1** — the only method annotations whose `value` is SpEL.

```java
@Secured("hasRole('ADMIN')")          // looks up that literal string
@Secured("ROLE_ADMIN")                // correct for @Secured
@RolesAllowed("ADMIN")                // ROLE_ADMIN after prefix
@PreAuthorize("hasRole('ADMIN')")     // SpEL
```

**Listing 2.** Conceptual — the usual trick. `@RolesAllowed("ROLE_ADMIN")` double-prefixes.

```d2
direction: right
spel: "@PreAuthorize @PostAuthorize\n@PreFilter @PostFilter" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}
lit: "@Secured @RolesAllowed\n@PermitAll @DenyAll" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Four expressions; the rest are labels. See [[What is PreAuthorize]], [[What is PostAuthorize in Spring Security]], [[What is PreFilter and PostFilter in Spring Security]], [[What is Secured in Spring Security]], [[What is RolesAllowed in Spring Security]], [[What is prePostEnabled in method security]], [[What is hasRole in PreAuthorize versus Secured]].

> [!warning] Default flags hide two of the families
> Bare `@EnableMethodSecurity` enables **only** the SpEL four. `@Secured` and `@RolesAllowed` stay decorative until `securedEnabled` / `jsr250Enabled`. Bare `@EnableGlobalMethodSecurity` enables **none** of the four until `prePostEnabled = true`. Do not put SpEL inside `@Secured`.

> [!tip] Interview answer
> Only `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, and `@PostFilter` take SpEL. `@Secured` and `@RolesAllowed` are lists of role or authority strings — `hasRole` inside `@Secured` is not a function call. `@EnableMethodSecurity` turns the SpEL four on by default; you still flip extra flags for `@Secured` or JSR-250.
