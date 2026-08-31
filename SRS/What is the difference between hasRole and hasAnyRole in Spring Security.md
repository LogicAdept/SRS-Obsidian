<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/MethodSecurity #SRS

# What is the difference between hasRole and hasAnyRole in Spring Security?

> [!abstract] Short answer
> Both test **`Authentication.getAuthorities()`** after **prepending `ROLE_`** (or the configured prefix). **`hasRole("ADMIN")`** requires **that one** role — **`ROLE_ADMIN`**. **`hasAnyRole("ADMIN", "MANAGER")`** is **OR**: any listed role is enough (**`ROLE_ADMIN` or `ROLE_MANAGER`**). Official HTTP DSL: **`hasRole`** is a shortcut for **`hasAuthority`**; **`hasAnyRole`** is a shortcut for **`hasAnyAuthority`**. Need **every** role? That is **`hasAllRoles`** (AND), **not** `hasAnyRole`. Prefix-free twins: **`hasAuthority` / `hasAnyAuthority`**.

## One role versus any of a list

There is no separate role type. **`User.roles("ADMIN")`** stores **`ROLE_ADMIN`**. Matchers add the same prefix ([[What is the difference between a role and an authority in Spring Security]], [[What is hasRole versus hasAuthority in Spring Security]]).

| Matcher | Logic | Looks for (default prefix) |
| --- | --- | --- |
| **`hasRole("ADMIN")`** | Single (same as one-arg **`hasAnyRole`**) | **`ROLE_ADMIN`** |
| **`hasAnyRole("ADMIN", "MANAGER")`** | **OR** | **`ROLE_ADMIN` or `ROLE_MANAGER`** |
| **`hasAllRoles("ADMIN", "MANAGER")`** | **AND** | **both** |
| **`hasAuthority` / `hasAnyAuthority`** | Same one / any, **no** prefix | Exact strings you pass |

**`AuthorityAuthorizationManager` since 5.5.** On **`authorizeHttpRequests`**, an argument that **already** starts with **`ROLE_`** **throws** (*should not start with ROLE_ … Consider using hasAuthority instead*). SpEL (**`@PreAuthorize`**, **`SecurityExpressionRoot`**) **strips** a leading **`ROLE_`** first, so **`hasRole('ROLE_ADMIN')`** still matches — that strip is **not** applied on the HTTP DSL ([[What is hasRole in PreAuthorize versus Secured]], [[What is GrantedAuthority in Spring Security]]).

Miss → **`AccessDeniedException`** → **403** for a fully authenticated user ([[What is AccessDeniedHandler]]).

```java
http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/admin/**").hasRole("ADMIN")
	.requestMatchers("/staff/**").hasAnyRole("ADMIN", "MANAGER")
	.requestMatchers("/dual/**").hasAllRoles("ADMIN", "AUDITOR")
	.anyRequest().authenticated());
```

**Listing 1.** One role, **any** of two (OR), **all** of two (AND). Omit **`ROLE_`** on these methods.

```java
@PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
public void staffAction() { }

@PreAuthorize("hasRole('ADMIN') and hasRole('AUDITOR')")
public void dualAction() { }
```

**Listing 2.** Expression **OR** via **`hasAnyRole`**. Expression **AND** via **`and`** (or **`hasAllRoles`**). **`hasAnyRole` is never AND**.

```d2
direction: down
one: "hasRole(\"ADMIN\")\none prefixed string" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
any: "hasAnyRole(\"ADMIN\", \"MANAGER\")\nOR" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
token: "ROLE_ADMIN / ROLE_MANAGER\non Authentication" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

one -> token
any -> token
```

**Fig. 1.** Same prefix rule. **`hasAnyRole`** is **any match**, not **all**.

> [!warning] `hasAnyRole` is OR
> A user with only **`ROLE_MANAGER`** passes **`hasAnyRole("ADMIN", "MANAGER")`** and fails **`hasRole("ADMIN")`**. For **both** roles use **`hasAllRoles`** or **`hasRole('A') and hasRole('B')`** in SpEL. **`hasAnyAuthority("ADMIN", "MANAGER")`** looks for **`ADMIN`**, not **`ROLE_ADMIN`**.

> [!warning] Do not pass `ROLE_` into HTTP `hasAnyRole`
> **`hasAnyRole("ROLE_ADMIN", "MANAGER")` throws** at configuration time, same as **`hasRole("ROLE_ADMIN")`**. Copying **`@PreAuthorize("hasAnyRole('ROLE_ADMIN')")`** into **`authorizeHttpRequests`** is the usual footgun.

> [!tip] Interview answer
> hasRole checks one ROLE_-prefixed authority. hasAnyRole is the same check for several names with OR — hasAnyRole("ADMIN", "MANAGER") succeeds if the token has ROLE_ADMIN or ROLE_MANAGER. AND is hasAllRoles, not hasAnyRole. I omit ROLE_ on the HTTP DSL; hasAuthority / hasAnyAuthority are the prefix-free equivalents.
