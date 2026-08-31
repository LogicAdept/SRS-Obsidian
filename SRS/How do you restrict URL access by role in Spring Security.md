<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you restrict URL access by role in Spring Security?

> [!abstract] Short answer
> In **`authorizeHttpRequests`**, pair **`requestMatchers`** with **`hasRole` / `hasAnyRole`**. `hasRole("ADMIN")` requires authority **`ROLE_ADMIN`** (the `ROLE_` prefix is added for you). Rules are **first-match** — put `/admin/**` **before** `anyRequest()`. That is **URL** RBAC. Method-level `@PreAuthorize("hasRole('ADMIN')")` is a **different** filter (`AuthorizationFilter` vs method security).

## Pattern, then role

```java
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((authorize) -> authorize
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .requestMatchers("/user/**").hasRole("USER")
            .anyRequest().authenticated());
    return http.build();
}
```

**Listing 1.** Spring Security 6: `authorizeHttpRequests` + `requestMatchers` (not `authorizeRequests` / `antMatchers`). XML: `<intercept-url pattern="/admin/**" access="hasRole('ADMIN')"/>`. See [[How do you configure authorizeHttpRequests in Spring Security 6]].

| DSL | What must be on `Authentication` |
|---|---|
| `hasRole("ADMIN")` | `ROLE_ADMIN` (prefix added) |
| `hasAuthority("ADMIN")` | exactly `ADMIN` — **no** prefix |
| `hasAnyRole("USER", "ADMIN")` | either `ROLE_*` |
| `hasAllAuthorities("db", "ROLE_ADMIN")` | **both**; write `ROLE_` yourself here |

`hasRole` is a shortcut for `hasAuthority` with the default role prefix (`ROLE_` unless you change it). Do not pass `"ROLE_ADMIN"` to `hasRole` unless you want `ROLE_ROLE_ADMIN`.

```d2
direction: down
req: "GET /admin/users" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
m1: "requestMatchers /admin/**\nhasRole(ADMIN)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
m2: "anyRequest()\nauthenticated" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}

req -> m1: "first match — stop"
m1 -> m2: "only if no match"
```

**Fig. 1.** `AuthorizationFilter` applies **one** pair. A leading `anyRequest().authenticated()` never reaches `/admin/**`. See [[Why does authorization matcher order matter in Spring Security]].

`@PreAuthorize("hasRole('ADMIN')")` is **method** security (`@EnableMethodSecurity`), not a URL matcher. Use it when the same path must vary by method; use Listing 1 when the **URL** is the policy. See [[What is the difference between EnableWebSecurity and EnableMethodSecurity]].

> [!warning] `hasRole` vs `hasAuthority` prefix
> Users granted `ADMIN` fail `hasRole("ADMIN")`. Users granted `ROLE_ADMIN` fail `hasAuthority("ADMIN")`. Match the string you actually put in `GrantedAuthority`.

> [!tip] Interview answer
> Restrict URLs with authorizeHttpRequests requestMatchers("/admin/**").hasRole("ADMIN") — that looks for ROLE_ADMIN. Put specific patterns before anyRequest. hasAuthority does not add ROLE_. Method @PreAuthorize is a second layer, not a replacement for URL matchers.
