<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you configure `authorizeHttpRequests` in Spring Security 6?

> [!abstract] Short answer
> Call **`http.authorizeHttpRequests(...)`** with a lambda of **pattern → rule** pairs: **`requestMatchers(...)`** then **`permitAll` / `hasRole` / `authenticated` / …**, and end with **`anyRequest()`**. Rules are **first-match**. That lives on the [[How do you configure a SecurityFilterChain bean in Spring Security 6]] you `build()`. It replaced `authorizeRequests` (`AuthorizationFilter` instead of `FilterSecurityInterceptor`).

Whenever you customize `HttpSecurity`, declare authorization. The minimum is every request authenticated:

```java
http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated());
```

**Listing 1.** Required floor: `AuthorizationFilter` then requires an authenticated `SecurityContext` for every endpoint.

```java
@Bean
SecurityFilterChain web(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((authorize) -> authorize
            .dispatcherTypeMatchers(DispatcherType.FORWARD, DispatcherType.ERROR).permitAll()
            .requestMatchers("/public/**", "/css/**").permitAll()
            .requestMatchers("/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated());
    return http.build();
}
```

**Listing 2.** Typical Spring Security 6 list: permit dispatcher types MVC/Boot need, public Ant patterns, role-restricted prefixes, then `anyRequest()`. `hasRole("ADMIN")` means authority `ROLE_ADMIN` (do not write the prefix). `requestMatchers` replaced `antMatchers` / `mvcMatchers`.

`AuthorizationFilter` walks the pairs in **declaration order** and applies **only the first match** — same idea as XML `intercept-url`. Read Listing 2 as: if FORWARD/ERROR → permit; else if `/public/**` → permit; else if `/admin/**` → `ROLE_ADMIN`; else authenticated. See [[Why does authorization matcher order matter in Spring Security]] and [[Does intercept-url order matter in Spring Security]].

| DSL rule | Meaning |
|---|---|
| `permitAll` / `denyAll` | Always allow / always refuse; **no** `Authentication` lookup |
| `authenticated` | Any authenticated principal |
| `hasAuthority` / `hasAnyAuthority` | Exact `GrantedAuthority` strings |
| `hasRole` / `hasAnyRole` | Same, with the `ROLE_` prefix added for you |
| `hasAllAuthorities` / `hasAllRoles` | All listed values (write `ROLE_` yourself on `hasAllAuthorities`) |
| `access(AuthorizationManager)` | Custom manager |

URI matching in Spring Security 6 `requestMatchers(String…)` is **Ant** by default (`/admin/**`); regex is a separate matcher. `anyRequest()` is the catch-all matcher.

```d2
direction: down
req: "GET /admin/users" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
authz: "AuthorizationFilter\nauthorizeHttpRequests list" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
m1: "requestMatchers /public/**\npermitAll" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
m2: "requestMatchers /admin/**\nhasRole(ADMIN)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
m3: "anyRequest()\nauthenticated" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}

req -> authz
authz -> m1: "no"
m1 -> m2: "yes — stop"
m2 -> m3: "only if no match"
```

**Fig. 1.** First matching rule wins; later lines do not merge.

`AuthorizationFilter` sits **last** in the default chain, so authentication and CSRF already ran. MVC controllers still go through it (`DispatcherServlet` is after the filter): every app endpoint needs a rule. It also runs on **every dispatch** (`REQUEST`, `FORWARD`, `ERROR`, `INCLUDE`). Permitting `FORWARD` and `ERROR` (Listing 2) avoids a second deny when MVC renders a view or Boot forwards `/error`.

> [!warning] Missing `anyRequest()` is deny, not public
> If no `requestMatchers` line matches, `RequestMatcherDelegatingAuthorizationManager` **denies** (`Denying request since did not find matching RequestMatcher`). Paths are not left open. Still end with `anyRequest().authenticated()` or `anyRequest().denyAll()` so the list is an explicit allow-list. A **narrow `securityMatcher` with no catch-all chain** is what leaves URLs **unprotected** — that is chain selection, not this DSL.

> [!tip] Interview answer
> In Spring Security 6 you call authorizeHttpRequests on HttpSecurity and list requestMatchers rules in first-match order, ending with anyRequest. That replaced authorizeRequests and antMatchers; AuthorizationFilter applies the first hit. Leave out anyRequest and unmatched URLs are denied, not public; leave out a catch-all SecurityFilterChain and they are actually unsecured.
