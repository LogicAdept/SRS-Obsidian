<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is LogoutFilter?

> [!abstract] Short answer
> **LogoutFilter** is a Spring Security servlet filter that matches the configured logout URL (default **`/logout`**) and, on a valid request, runs a chain of **LogoutHandler** instances to tear down the session and security context, then delegates to a **LogoutSuccessHandler** (default redirect to `/login?logout`).

## What it does on a logout request

When `@EnableWebSecurity` or `spring-boot-starter-security` is present, Spring Security registers logout support automatically. **`LogoutFilter`** is the filter that watches for logout requests.

On **`POST /logout`** (the default path when CSRF protection is enabled), the filter invokes handlers in order, including:

- **`SecurityContextLogoutHandler`** — invalidates the HTTP session and clears the security context held in `SecurityContextHolder` and the configured `SecurityContextRepository`
- remember-me cleanup (`TokenRememberMeServices` / `PersistentTokenRememberMeServices` when configured)
- **`CsrfLogoutHandler`** — clears the saved CSRF token
- **`LogoutSuccessEventPublishingLogoutHandler`** — publishes a logout success event

After handlers finish, the default **`LogoutSuccessHandler`** redirects to **`/login?logout`**. Custom handlers can be added through the `logout` DSL (`addLogoutHandler`, `deleteCookies`, and similar options).

```d2
direction: right
request: "POST /logout\n(+ CSRF token)" {
  width: 210
  height: 70
  style.fill: "#e3f2fd"
}
filter: "LogoutFilter\nmatches logout URL" {
  width: 210
  height: 70
  style.fill: "#fff3e0"
}
handlers: "LogoutHandler chain\nsession, context,\nremember-me, CSRF" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
success: "LogoutSuccessHandler\n(e.g. redirect)" {
  width: 210
  height: 70
  style.fill: "#fce4ec"
}

request -> filter -> handlers -> success
```

**Fig. 1.** LogoutFilter orchestrates cleanup handlers, then runs logout success logic.

## Where it sits in the filter chain

In a typical default chain, **`LogoutFilter` runs after `CsrfFilter` and before authentication filters** such as `UsernamePasswordAuthenticationFilter` and `BasicAuthenticationFilter`. Because it executes **before `AuthorizationFilter`**, the built-in `/logout` endpoint does not need an explicit `permitAll` rule — only custom MVC logout endpoints you add yourself usually do.

Custom authentication filters belong **after `LogoutFilter`**; exploit-protection filters belong after `SecurityContextHolderFilter`. See [[What is SecurityFilterChain]] for how the chain is built.

```java
http.logout(logout -> logout
    .logoutUrl("/logout")
    .logoutSuccessUrl("/login?logout"));
```

**Listing 1.** Conceptual `HttpSecurity#logout` customization of the URL the filter matches and the post-logout redirect.

> [!warning] CSRF and logout method matter
> With CSRF protection enabled (the default), **`LogoutFilter` processes logout as an unsafe HTTP request — typically `POST /logout` with a valid CSRF token**. That blocks forged logout attempts. A bare **`GET /logout`** does not perform logout directly in that setup; Spring Security shows a **logout confirmation page** that supplies the token for `POST /logout`. If CSRF is disabled, logout can happen without that confirmation step — which is usually undesirable for browser apps. For AJAX logout, send the CSRF token with `POST /logout` rather than assuming a tokenless GET will work.

> [!tip] Interview answer
> LogoutFilter watches the logout URL, runs LogoutHandlers to invalidate the session and clear the security context (plus remember-me and CSRF cleanup), then redirects or runs a custom success handler. It sits after CsrfFilter and before login filters, so default `/logout` does not need `permitAll`.
