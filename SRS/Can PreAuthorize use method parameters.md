<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# Can PreAuthorize use method parameters?

> [!abstract] Short answer
> **Yes.** `@PreAuthorize` is SpEL. Method arguments are variables named **`#paramName`** (for example `#userId == authentication.name`). `@Secured` and `@RolesAllowed` take **authority/role strings only** — they cannot see arguments.

## How the name gets into SpEL

`PreAuthorizeAuthorizationManager` builds a `MethodSecurityEvaluationContext` from `MethodSecurityExpressionRoot`. That context **lazily** binds each argument as a SpEL variable once a `#name` is used. The name itself comes from `DefaultSecurityParameterNameDiscoverer`, in this order:

1. Spring Security **`@P("alias")`** on the parameter (`org.springframework.security.access.method.P`)
2. Spring Data **`@Param("alias")`** if Spring Data is on the classpath and at least one parameter has it
3. The **Java parameter name** from reflection if you compiled with **`-parameters`** (classes **and** interfaces)

Since Spring Framework **6.1**, `LocalVariableTableParameterNameDiscoverer` is gone. Debug-table names are **not** a reliable fallback. If you write `#id` in `@PreAuthorize`, **compile with `-parameters`** (or annotate). Same binding applies to `@PostAuthorize`, `@PreFilter`, and `@PostFilter`.

```java
@PreAuthorize("hasRole('ADMIN') or #userId == authentication.name")
public Account readAccount(String userId) {
    return load(userId);
}

@PreAuthorize("hasPermission(#c, 'write')")
public void updateContact(@P("c") Contact contact) {
    save(contact);
}

@PreAuthorize("#n == authentication.name")
Contact findContactByName(@Param("n") String name);
```

**Listing 1.** Conceptual Security **7.1** — `#userId` needs `-parameters` (or `@P` / `@Param`). `hasRole('ADMIN')` still means `ROLE_ADMIN`. `@Param` is Spring Data’s annotation.

```java
@Secured("ROLE_ADMIN")
public void update(Account account) { /* no #account */ }

@RolesAllowed("ADMIN")
public void delete(Account account) { /* no #account */ }
```

**Listing 2.** Conceptual — `@Secured` / `@RolesAllowed` are `String[]` names, not SpEL. `@EnableMethodSecurity(securedEnabled = true, jsr250Enabled = true)` is required before they run at all.

```d2
direction: down
call: "readAccount(userId)" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
disc: "DefaultSecurityParameterNameDiscoverer\n@P / @Param / -parameters" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
spel: "@PreAuthorize SpEL\n#userId == authentication.name" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

call -> disc -> spel
```

**Fig. 1.** The expression uses the **discovered** name. If discovery returns null, `#userId` is undefined.

See [[What is PreAuthorize]], [[What is the difference between Secured RolesAllowed and PreAuthorize]], [[How does method security work in Spring]].

> [!warning] `#userId` is not magically the source name
> Without `-parameters`, `@P`, or `@Param`, `#userId` does not bind. **Interfaces** never carried debug parameter names — use annotations or `-parameters`. If **only some** parameters have `@P` / `@Param`, `AnnotationParameterNameDiscoverer` still owns the method: unannotated parameters resolve to **`null`** (no fallback to `-parameters` for the rest). Annotate every argument you mention, or compile with `-parameters` and skip mixed annotations.

> [!tip] Interview answer
> Yes — `@PreAuthorize` SpEL can use `#paramName` for method arguments, including `hasRole('ADMIN') or #userId == authentication.name`. Compile with `-parameters` or name them with `@P` / `@Param`; otherwise the variable is missing. `@Secured` and `@RolesAllowed` cannot do this — they only list roles.
