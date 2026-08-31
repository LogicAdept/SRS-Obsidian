<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/MethodSecurity #SRS

# What is the difference between a role and an authority in Spring Security?

> [!abstract] Short answer
> Spring Security **does not store roles as a separate type**. Everything on **`Authentication.getAuthorities()`** is a **`GrantedAuthority`** (usually **`SimpleGrantedAuthority`**). A **role** is a **convention**: an authority whose **`getAuthority()`** is **`ROLE_` + name** (default prefix). **`User.roles("ADMIN")`** stores **`ROLE_ADMIN`**. **`User.authorities("ADMIN")`** stores **`ADMIN`**. **`hasRole("ADMIN")`** looks for **`ROLE_ADMIN`**. **`hasAuthority("READ_REPORTS")`** looks for that **exact** string. Mix storage and matcher and a logged-in user gets **403**.

## One type, a prefix convention

Authorization architecture: the **`AuthenticationManager`** puts **`GrantedAuthority`** objects on the token; **`AuthorizationManager`** later **reads** **`getAuthority()`** strings. There is **no** `Role` interface. The field on **`SimpleGrantedAuthority`** is even named **`role`** — it is still just that string ([[What is GrantedAuthority in Spring Security]], [[What is SimpleGrantedAuthority]]).

| Builder | Stored string | **`hasRole("ADMIN")`** | **`hasAuthority("ADMIN")`** |
| --- | --- | --- | --- |
| **`User.roles("ADMIN")`** | **`ROLE_ADMIN`** | Match | Miss |
| **`User.authorities("ADMIN")`** | **`ADMIN`** | Miss | Match |
| **`User.authorities("ROLE_ADMIN")`** | **`ROLE_ADMIN`** | Match | Miss (`hasAuthority("ADMIN")`) |

**`User.roles(...)`** **prepends `ROLE_`** and **rejects** a value that already starts with **`ROLE_`**. **`User.authorities(...)`** / **`new SimpleGrantedAuthority("…")`** store the text **as given**. JDBC **`authorities.authority`** is loaded the same way — the column is **not** auto-prefixed ([[What is UserDetails and UserDetailsService in Spring Security]], [[What is JdbcUserDetailsManager]]).

Matchers (**`AuthorityAuthorizationManager` since 5.5**): **`hasRole` / `hasAnyRole` / `hasAllRoles`** prepend the prefix (override with **`GrantedAuthorityDefaults`**). **`hasAuthority` / `hasAnyAuthority` / `hasAllAuthorities`** do **not**. Official HTTP sample: **`hasRole("ADMIN")`** omits the prefix; **`hasAllAuthorities("db", "ROLE_ADMIN")`** **must** spell **`ROLE_ADMIN`**. **`hasRole("ROLE_ADMIN")` on `authorizeHttpRequests` throws.** SpEL **`hasRole('ROLE_ADMIN')`** still works because **`SecurityExpressionRoot`** **strips** a leading **`ROLE_`** first ([[What is hasRole versus hasAuthority in Spring Security]], [[What is hasRole in PreAuthorize versus Secured]]).

**`FactorGrantedAuthority`** (**7.0**, e.g. **`FACTOR_PASSWORD`**) is also an authority. It records **how** the user authenticated, not an application role. Anonymous traffic still has **`ROLE_ANONYMOUS`** — that is a **role-shaped** string, not a logged-in user ([[How do you implement two-factor authentication in Spring Security]]).

```java
UserDetails admin = User.builder()
	.username("admin")
	.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
	.roles("ADMIN")
	.build();
```

**Listing 1.** Stores **`ROLE_ADMIN`**. Pair with **`hasRole("ADMIN")`** or **`hasAuthority("ROLE_ADMIN")`**, not **`hasAuthority("ADMIN")`**.

```java
http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/admin/**").hasRole("ADMIN")
	.requestMatchers("/reports/**").hasAuthority("REPORT_READ")
	.anyRequest().authenticated());
```

**Listing 2.** Role shortcut vs exact permission. **`roles("REPORT_READ")`** would have stored **`ROLE_REPORT_READ`** and this **`hasAuthority`** would miss.

```d2
direction: down
store: "GrantedAuthority string" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
role: "ROLE_ADMIN\n(role convention)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
perm: "REPORT_READ\n(plain authority)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}

store -> role
store -> perm
```

**Fig. 1.** Both are **`getAuthority()`** strings. **Role** means the **`ROLE_`** prefix, not a second type.

> [!warning] `authorities("ADMIN")` plus `hasRole("ADMIN")` denies
> The matcher looks for **`ROLE_ADMIN`**. Login succeeds; **`AccessDeniedException`** → **403**. The same miss happens if JDBC stored **`ADMIN`** and the HTTP rule used **`hasRole`**. Fine-grained names belong in **`authorities` + `hasAuthority`** with the **same** spelling ([[What is AccessDeniedHandler]]).

> [!warning] Do not paste `ROLE_` into HTTP `hasRole`
> **`requestMatchers(…).hasRole("ROLE_ADMIN")` throws** at configuration time. Copying **`@PreAuthorize("hasRole('ROLE_ADMIN')")`** into **`authorizeHttpRequests`** is the usual footgun: expressions **strip**; the DSL **does not**.

> [!tip] Interview answer
> Spring Security only stores GrantedAuthority strings. A role is the convention that the string starts with ROLE_. User.roles("ADMIN") stores ROLE_ADMIN; User.authorities("ADMIN") stores ADMIN. hasRole("ADMIN") looks for ROLE_ADMIN; hasAuthority matches whatever I stored exactly. Mixing those two is the classic 403 after a successful login.
