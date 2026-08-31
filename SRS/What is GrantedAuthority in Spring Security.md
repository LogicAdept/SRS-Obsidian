<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is GrantedAuthority in Spring Security?

> [!abstract] Short answer
> **`GrantedAuthority`** is an **authority granted to an `Authentication`**. The interface is one method: **`getAuthority()`** — a **`String`** precise enough for an **`AuthorizationManager`**, or **`null`** for a **complex** authority that a manager must understand by type. Stock providers put **`SimpleGrantedAuthority`** on the token. **`UserDetails.getAuthorities()`** is the usual source; **`DaoAuthenticationProvider`** copies them onto the successful **`Authentication`**. **`hasAuthority("…")`** matches that string **exactly**. **`hasRole("ADMIN")`** looks for **`ROLE_ADMIN`**. A role is **not** a separate type — it is a **`ROLE_`**-prefixed authority string.

## Strings on Authentication, then AuthorizationManager

Authorization architecture: the **`AuthenticationManager`** inserts **`GrantedAuthority`** objects; later **`AuthorizationManager`** instances **read** them ([[What is a principal in Spring Security]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is UserDetails and UserDetailsService in Spring Security]]).

**`SimpleGrantedAuthority`** stores the string as given — including any prefix (**`ROLE_ADMIN`**, **`SCOPE_read`**, a custom permission). **`User.roles("USER")`** is a shortcut that **prepends `ROLE_`** (and **rejects** a value that already starts with **`ROLE_`**). **`User.authorities("USER")`** stores **`USER`** with **no** prefix ([[What is SimpleGrantedAuthority]], [[What is DaoAuthenticationProvider]]).

HTTP and method rules go through **`AuthorityAuthorizationManager`** (**since 5.5**). **`hasRole` / `hasAnyRole`** prepend **`ROLE_`** (customizable via **`GrantedAuthorityDefaults`** / **`DefaultAuthorizationManagerFactory.setRolePrefix`**). Passing **`hasRole("ROLE_ADMIN")`** **throws**: *should not start with ROLE_ … Consider using hasAuthority instead.* **`hasAuthority` / `hasAnyAuthority`** do **not** prefix ([[What is hasRole versus hasAuthority in Spring Security]]).

**`FactorGrantedAuthority`** (**7.0**, e.g. **`FACTOR_PASSWORD`**) is also a **`GrantedAuthority`**. It records **how** the user authenticated for MFA, not an application role ([[How do you implement two-factor authentication in Spring Security]]). Anonymous traffic still has an **`Authentication`** with **`ROLE_ANONYMOUS`**.

```java
UserDetails user = User.builder()
	.username("user")
	.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
	.roles("USER")
	.build();

http.authorizeHttpRequests((authorize) -> authorize
	.requestMatchers("/admin/**").hasRole("ADMIN")
	.requestMatchers("/reports/**").hasAuthority("REPORT_READ")
	.anyRequest().authenticated());
```

**Listing 1.** **`roles("USER")`** stores **`ROLE_USER`**, so **`hasRole("USER")`** matches. **`hasAuthority("REPORT_READ")`** matches only if that **exact** string is on the token — **`roles("REPORT_READ")`** would have stored **`ROLE_REPORT_READ`**.

```java
AuthorityAuthorizationManager.hasRole("ADMIN");     // looks for ROLE_ADMIN
AuthorityAuthorizationManager.hasAuthority("ROLE_ADMIN"); // exact ROLE_ADMIN
```

**Listing 2.** Same check, two APIs. **`hasRole("ROLE_ADMIN")`** is illegal.

```d2
direction: down
uds: "UserDetails.getAuthorities\nSimpleGrantedAuthority strings" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
auth: "Authentication.getAuthorities" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
am: "AuthorityAuthorizationManager\nhasRole / hasAuthority" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

uds -> auth -> am
```

**Fig. 1.** Authentication **carries** authorities. Authorization **compares** `getAuthority()` strings (unless the authority is complex and returns **`null`**).

> [!warning] `ROLE_` is a string convention, not a class
> **`hasRole("ADMIN")`** and **`User.roles("ADMIN")`** both add **`ROLE_`**. Mixing **`authorities("ADMIN")`** with **`hasRole("ADMIN")`** looks for **`ROLE_ADMIN`** and **denies**. **`hasRole("ROLE_ADMIN")`** does not “be extra clear” — it **throws**. Fine-grained permissions belong in **`hasAuthority`** with the **full** stored string.

> [!warning] `getAuthority()` may be null
> A **complex** authority (thresholds per account, not a single name) **must** return **`null`**. String-based managers then **cannot** vote it; you need an **`AuthorizationManager`** that knows that type. Returning **`null`** from a normal role/permission is how rules silently fail. **`FactorGrantedAuthority`** strings are **not** application roles — do not **`hasRole("PASSWORD")`** expecting MFA.

> [!tip] Interview answer
> GrantedAuthority is the permission or role string hanging off Authentication. SimpleGrantedAuthority is the usual implementation; User.roles("USER") stores ROLE_USER. hasRole prepends ROLE_ and refuses a value that already has the prefix; hasAuthority matches the stored string exactly. Factors like FACTOR_PASSWORD are GrantedAuthority too, but they mean how you logged in, not an app role.
