<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/AppSec #Java/Spring/Security/CSRF #SRS

# What is `CsrfFilter` in Spring Security?

> [!abstract] Short answer
> The filter that applies the **synchronizer token** pattern. **`http.csrf`** is **on by default** with `@EnableWebSecurity`. Default matcher **skips GET, HEAD, TRACE, OPTIONS** and checks **every other method**. Missing or wrong token → **`AccessDeniedException`** → **403** (`Invalid CSRF token found…` in DEBUG). It sits **after** `CorsFilter` and **before** `LogoutFilter` / form login. Browser form login **needs** it. A **stateless JWT API** that does not serve browsers typically **`csrf((c) -> c.disable())`**.

## Skip safe methods, then compare tokens

```d2
direction: down
m: "DEFAULT_CSRF_MATCHER\nnot GET/HEAD/TRACE/OPTIONS?" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
ok: "continue FilterChain" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
load: "load CsrfToken +\nCsrfTokenRequestHandler" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
deny: "AccessDeniedHandler\n403" {
  width: 200
  height: 40
  style.fill: "#fce4ec"
}

m -> ok: "no"
m -> load: "yes"
load -> ok: "token matches"
load -> deny: "missing / invalid"
```

**Fig. 1.** CSRF chapter: deferred token, then validate. Safe methods must be **read-only** or the skip is unsafe. See [[What is CorsFilter in Spring Security]] (preflight `OPTIONS` is skipped here; CORS still must run **first**).

Default store: **`HttpSessionCsrfTokenRepository`**. SPAs often use **`CookieCsrfTokenRepository.withHttpOnlyFalse()`** (`XSRF-TOKEN` / `X-XSRF-TOKEN`). Token in the body/header (`_csrf`), **not** auto-sent like the session cookie.

```java
http.csrf(Customizer.withDefaults()); // default on

http.csrf((csrf) -> csrf.disable());  // non-browser / STATELESS API chain
```

**Listing 1.** Enable is implicit; disable **per chain**. Do not disable CSRF on the form-login catch-all. See [[How do you configure JWT and form login as two SecurityFilterChain beans]]. Tests: `.with(csrf())` on `MockMvc` POSTs.

A **403** with a valid JWT and CSRF still enabled is **`CsrfFilter`**, not `JwtDecoder`. Architecture: the response body is empty on purpose — `DEBUG` on `org.springframework.security.web.csrf.CsrfFilter` names the token. See [[How do you enable Spring Security debug logging for the filter chain]] and [[What is AuthorizationFilter in Spring Security]] (that 403 is a **different** `AccessDeniedException`).

> [!warning] Do not disable CSRF on a browser session
> `csrf.disable()` is for backends that **do not** serve browser traffic (mobile/JWT-only). If the same process serves a session cookie, keep CSRF and ignore only specific matchers (`ignoringRequestMatchers`). Mixing cookie session + disabled CSRF is the classic attack.

> [!tip] Interview answer
> CsrfFilter is the default synchronizer-token filter: it skips GET HEAD TRACE OPTIONS and 403s other methods without a matching token. It runs after CorsFilter. Form login needs it; a JWT-only chain usually disables it. A 403 on POST with a good Bearer token is often this filter still on.
