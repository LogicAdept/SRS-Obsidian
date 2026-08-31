<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #Security/JWT #SRS

# How do you configure JWT and form login as two `SecurityFilterChain` beans?

> [!abstract] Short answer
> Publish **two** `SecurityFilterChain` beans. Give the **JWT / resource-server** chain a **tighter `securityMatcher`** and a **higher priority** (`@Order(1)`): `oauth2ResourceServer(jwt)`. Leave the **form-login** chain **without** a matcher (tried last) so it is the catch-all. `FilterChainProxy` runs **only the first match** — the two chains are not merged.

## Specific API chain, then UI catch-all

This is the multiple-`HttpSecurity` layout: a scoped `/api/**` chain plus a form-login catch-all, with JWT instead of HTTP Basic:

```java
@Configuration
@EnableWebSecurity
public class DualAuthConfig {

    @Bean
    @Order(1)
    SecurityFilterChain api(HttpSecurity http) throws Exception {
        http.securityMatcher("/api/**")
            .authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
            .oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()))
            .sessionManagement((session) -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .csrf((csrf) -> csrf.disable());
        return http.build();
    }

    @Bean
    SecurityFilterChain ui(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

**Listing 1.** JWT resource-server chain for `/api/**` (`BearerTokenAuthenticationFilter` via `oauth2ResourceServer().jwt()`), form login for everything else. No `@Order` on `ui` means **last**. Provide a `JwtDecoder` bean (or Boot’s issuer-uri auto-config). See [[How do you configure a SecurityFilterChain bean in Spring Security 6]] and [[What is securityMatcher in Spring Security]].

`oauth2ResourceServer((oauth2) -> oauth2.jwt(...))` is the documented resource-server `SecurityFilterChain`. `formLogin` belongs on a chain that **matches `/login`**: `UsernamePasswordAuthenticationFilter` serves `GET`/`POST /login` only if that chain’s `securityMatcher` includes those URLs. Putting form login on the **unscoped** catch-all avoids a surprising 404.

`SessionCreationPolicy.STATELESS` on the API chain uses a `NullSecurityContextRepository` (Bearer authentication is already a per-request mechanism). CSRF stays **on** for the UI chain; `csrf.disable()` applies **only** to the `HttpSecurity` you call it on. Disable or `csrf.ignoringRequestMatchers` on the API chain when that API is not a browser session (CSRF is for cookie-authenticated browser calls). Do not disable CSRF on the form-login chain.

```d2
direction: down
req: "Request" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
fcp: "FilterChainProxy\nfirst match" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
api: "@Order(1) /api/**\noauth2ResourceServer jwt" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
ui: "no matcher (last)\nformLogin" {
  width: 220
  height: 55
  style.fill: "#fce4ec"
}

req -> fcp
fcp -> api: "/api/**"
fcp -> ui: "else"
```

**Fig. 1.** Two isolated chains: JWT filters on the API matcher, form-login filters on the rest. Later chains never add filters to `/api/**`.

> [!warning] Catch-all must not win `@Order`
> A chain **without** `securityMatcher` matches every request. If that UI bean has a **lower** `@Order` value than the JWT bean (or the JWT bean has **no** `securityMatcher`), `/api/**` never reaches Bearer JWT. Put the **narrow** matcher first; leave the form-login chain **last**. See [[Why does authorization matcher order matter in Spring Security]] for the same first-match idea **inside** a chain.

> [!tip] Interview answer
> Use two SecurityFilterChain beans: @Order(1) with securityMatcher("/api/**") and oauth2ResourceServer jwt, then a catch-all bean with formLogin and no matcher. FilterChainProxy picks the first match, so a catch-all with a better Order starves JWT. Keep CSRF and sessions on the UI chain; STATELESS and csrf.disable belong only on the Bearer API HttpSecurity.
