<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Core/IoC/SpEL #SRS

# What is `SecurityExpressionRoot`?

> [!abstract] Short answer
> The **SpEL root object** (since **3.0**) for Security expressions. It implements **`SecurityExpressionOperations`**: **`hasAuthority` / `hasAnyAuthority` / `hasAllAuthorities`**, **`hasRole` / `hasAnyRole` / `hasAllRoles`**, **`permitAll` / `denyAll`**, **`isAnonymous` / `isAuthenticated` / `isRememberMe` / `isFullyAuthenticated`**, **`hasPermission`**, plus **`authentication`** and **`principal`**. **`@PreAuthorize("hasRole('ADMIN')")`** calls this. **`@Secured("ROLE_ADMIN")`** does **not** — it is a **role list**, not SpEL. **`hasRole("ADMIN")`** looks up **`ROLE_ADMIN`** by default.

## Root of the evaluation context

**`SecurityExpressionHandler`** puts an instance on the SpEL **`EvaluationContext`**. The class is **abstract**; web uses **`WebSecurityExpressionRoot`**, messaging **`MessageSecurityExpressionRoot`**. Method filtering (`filterObject`, `returnObject`, `this`) is **`MethodSecurityExpressionOperations`**.

Since **5.8** the constructor takes a **`Supplier<Authentication>`** (lazy). Since **7.0** prefer **`SecurityExpressionRoot(Supplier, T object)`**; **`setDefaultRolePrefix` / `setRoleHierarchy` / `setTrustResolver`** on the root are **deprecated** in favor of **`setAuthorizationManagerFactory`**.

| SpEL | Meaning |
| --- | --- |
| **`hasAuthority('permission:read')`** | Exact **`GrantedAuthority`** string |
| **`hasRole('ADMIN')`** | Same as **`hasAuthority`**, with default prefix **`ROLE_`** (also accepts **`ROLE_ADMIN`**) |
| **`hasAnyRole('A','B')`** | **OR** |
| **`permitAll` / `permitAll()`** | Always **true** (field **and** method so both spellings work) |
| **`denyAll` / `denyAll()`** | Always **false** |
| **`isFullyAuthenticated()`** | Authenticated **without** remember-me |
| **`authentication.name`** | **`getAuthentication()`** |
| **`principal`** | **`Authentication.getPrincipal()`** |
| **`hasPermission(target, 'read')`** | **`PermissionEvaluator`** (ACL); constants **`read` / `write` / `create` / `delete` / `admin`** |

```java
@PreAuthorize("hasRole('ADMIN') || #id == authentication.name")
public Order getOrder(String id) { /* ... */ }

@Secured("ROLE_ADMIN")
public void adminOnly() { /* ... */ }
```

**Listing 1.** Left: SpEL on the root (`hasRole`, `#id`, `authentication`). Right: **`@Secured`** matches authority strings only — **no** `||`, **no** `#id` ([[What are Spring Security expressions]], [[What is EnableMethodSecurity]]).

```d2
direction: down
spel: "@PreAuthorize SpEL" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
root: "SecurityExpressionRoot\nhasRole / principal" {
  width: 250
  height: 48
  style.fill: "#c8e6c9"
}
h: "SecurityExpressionHandler" {
  width: 220
  height: 36
  style.fill: "#fff3e0"
}

h -> root
spel -> root
```

**Fig. 1.** Custom root **methods** need a custom **handler** (or an **`@authz` bean**). Tweaking only **`HttpSecurity`** does not change this object for **`@PreAuthorize`** ([[What is SecurityExpressionHandler in Spring Security]], [[What is AuthorizationManager in method security]]).

> [!warning] `hasRole` still prefixes `ROLE_`
> **`hasRole("ROLE_ADMIN")`** and **`hasRole("ADMIN")`** both target **`ROLE_ADMIN`** with the default prefix. **`hasAuthority`** does **not** add a prefix. Empty prefix via **`GrantedAuthorityDefaults`** / factory — not by renaming the root class.

> [!warning] `@Secured` is not this API
> No `hasPermission`, no bean refs (`@authz.…`), no `returnObject`. Enabling only **`securedEnabled`** never instantiates **`SecurityExpressionRoot`**.

> [!tip] Interview answer
> SecurityExpressionRoot is the SpEL #root for Spring Security: hasRole, hasAuthority, permitAll, authentication, principal. @PreAuthorize evaluates against it. @Secured does not. hasRole adds ROLE_ by default. Custom methods belong on a custom root installed by SecurityExpressionHandler, or on a Spring bean called from the expression.
