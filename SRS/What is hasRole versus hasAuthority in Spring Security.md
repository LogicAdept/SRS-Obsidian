<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/MethodSecurity #SRS

# What is hasRole versus hasAuthority in Spring Security?

> [!abstract] Short answer
> Both test **`Authentication.getAuthorities()`**. **`hasAuthority("READ_REPORTS")`** matches that **exact** `GrantedAuthority` string. **`hasRole("ADMIN")`** is a shortcut that **prepends `ROLE_`** (or the configured prefix) and then does the same check — it looks for **`ROLE_ADMIN`**. Official HTTP sample: **`hasRole("ADMIN")`** does **not** include the prefix; **`hasAllAuthorities("db", "ROLE_ADMIN")`** **must** spell **`ROLE_ADMIN`**. **`hasRole("ROLE_ADMIN")` on `authorizeHttpRequests` throws.** SpEL **`hasRole('ROLE_ADMIN')`** still works because **`SecurityExpressionRoot`** **strips** a leading **`ROLE_`** first.

## Same strings, different prefix rule

There is no separate “role type.” A role is an authority whose `getAuthority()` is **`ROLE_` + name** ([[What is GrantedAuthority in Spring Security]], [[What is SimpleGrantedAuthority]]). **`User.roles("USER")`** stores **`ROLE_USER`**. **`User.authorities("USER")`** stores **`USER`**. **`hasRole("USER")`** looks for the former ([[What is UserDetails and UserDetailsService in Spring Security]]).

HTTP (**`authorizeHttpRequests`**, **`AuthorityAuthorizationManager` since 5.5**):

| DSL | What must be on the token |
| --- | --- |
| **`hasRole("ADMIN")`** / **`hasAnyRole`** / **`hasAllRoles`** | **`ROLE_ADMIN`** (prefix added; argument **must not** already start with **`ROLE_`**) |
| **`hasAuthority("…")`** / **`hasAnyAuthority`** / **`hasAllAuthorities`** | The **exact** strings you pass |

Miss → **`AccessDeniedException`** → **403** for a fully authenticated user ([[What is AccessDeniedHandler]], [[How do you customize the access denied page in Spring Security]]).

Expressions (**`@PreAuthorize`**, XML **`access=`**, **`WebExpressionAuthorizationManager`**) use **`SecurityExpressionRoot`**: **`hasRole` / `hasAnyRole`** still mean “prefix then match,” but if the argument **already** starts with **`ROLE_`**, **7.x strips it** before calling the factory (old **`hasRole('ROLE_A')`** still matches **`ROLE_A`**). That strip is **not** applied on the HTTP DSL. **`@Secured("ROLE_ADMIN")`** is a different API: it wants the **full** string ([[What is hasRole in PreAuthorize versus Secured]]).

**`@EnableMultiFactorAuthentication`** wraps **`hasRole` / `authenticated()`** so those rules also require **`FactorGrantedAuthority`** values — still not application roles ([[How do you implement two-factor authentication in Spring Security]]).

```java
http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/admin/**").hasRole("ADMIN")
	.requestMatchers("/db/**").hasAllAuthorities("db", "ROLE_ADMIN")
	.requestMatchers("/reports/**").hasAuthority("REPORT_READ")
	.anyRequest().authenticated());
```

**Listing 1.** Official pairing: **`hasRole`** omits **`ROLE_`**; **`hasAllAuthorities`** (and **`hasAuthority`**) use the **stored** strings, so a role there is **`ROLE_ADMIN`**.

```java
AuthorityAuthorizationManager.hasRole("ADMIN");      // ROLE_ADMIN
AuthorityAuthorizationManager.hasAuthority("ROLE_ADMIN"); // same check, full string
```

**Listing 2.** Equivalent managers. **`hasRole("ROLE_ADMIN")`** → *ROLE_ADMIN should not start with ROLE_ … Consider using hasAuthority instead.*

```d2
direction: down
role: "hasRole(\"ADMIN\")\nprepend ROLE_" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
auth: "hasAuthority(\"REPORT_READ\")\nexact string" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
token: "Authentication.getAuthorities()" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

role -> token
auth -> token
```

**Fig. 1.** Prefix is a **matcher** concern. The token only stores strings.

> [!warning] Do not write `ROLE_` into `hasRole` on the HTTP DSL
> **`requestMatchers(…).hasRole("ROLE_ADMIN")` throws** at configuration time. Copying **`@PreAuthorize("hasRole('ROLE_ADMIN')")`** into **`authorizeHttpRequests`** is the usual footgun: expressions **strip** the prefix; the DSL **does not**. **`hasAllAuthorities("ADMIN")`** looks for **`ADMIN`**, not **`ROLE_ADMIN`**.

> [!warning] Storage must match the matcher
> **`authorities("ADMIN")` + `hasRole("ADMIN")`** looks for **`ROLE_ADMIN`** and **denies**. Fine-grained permissions belong in **`hasAuthority`** with the **same** string **`UserDetails`** returned. **`hasAny*`** is OR; **`hasAll*`** is AND.

> [!tip] Interview answer
> hasAuthority matches the GrantedAuthority string exactly. hasRole is the same check after prepending ROLE_, so hasRole("ADMIN") is hasAuthority("ROLE_ADMIN"). I never pass ROLE_ into the HTTP hasRole DSL — that throws — and I do pass ROLE_ when the method is hasAuthority or hasAllAuthorities. If I stored ADMIN without the prefix, hasRole("ADMIN") fails.
