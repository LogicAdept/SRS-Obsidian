<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `AbstractAuthenticationProcessingFilter`?

> [!abstract] Short answer
> It is the **base servlet `Filter`** for **browser login submissions** (`GenericFilterBean`). A subclass builds an `Authentication` from the request (`attemptAuthentication`), the filter calls **`AuthenticationManager`**, then **success or failure handlers**. `UsernamePasswordAuthenticationFilter` (`http.formLogin()`) is the usual subclass. It is **not** the parent of **`BearerTokenAuthenticationFilter`**.

## Login POST, not every request

The filter runs only when `requiresAuthentication` matches (form login: **`POST /login`**). Otherwise it calls the rest of the chain. `AuthenticationManager` is required. Subclasses implement `attemptAuthentication` and must: return a populated `Authentication`, return **`null`** (login still in progress — e.g. multi-step OIDC), or throw `AuthenticationException`.

```d2
direction: down
req: "requiresAuthentication?" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
attempt: "attemptAuthentication\nAuthenticationManager" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
ok: "successfulAuthentication\nSecurityContext + SuccessHandler" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
fail: "unsuccessfulAuthentication\nclear context + FailureHandler" {
  width: 300
  height: 50
  style.fill: "#fce4ec"
}
skip: "filterChain.doFilter" {
  width: 220
  height: 40
  style.fill: "#eceff1"
}

req -> attempt: "yes"
req -> skip: "no"
attempt -> ok: "Authentication"
attempt -> fail: "AuthenticationException"
attempt -> skip: "null (in progress)"
```

**Fig. 1.** Servlet authentication architecture: this class is the shared skeleton; the token type is the subclass. See [[How does Spring Security authenticate an HTTP request end to end]].

**Success:** `SessionAuthenticationStrategy` (session fixation), merge authorities from an already-authenticated `Authentication`, set `SecurityContextHolder`, `RememberMeServices.loginSuccess`, `InteractiveAuthenticationSuccessEvent`, `AuthenticationSuccessHandler` (default `SavedRequestAwareAuthenticationSuccessHandler` → saved request or `/`). **Default `SecurityContextRepository` does not save** — `formLogin()` wires a repository so the next request still has the user (`SecurityContextHolderFilter`).

**Failure:** clear `SecurityContextHolder`, `RememberMeServices.loginFail`, `AuthenticationFailureHandler` (class default `SimpleUrlAuthenticationFailureHandler` → **401**; form login typically redirects to `/login?error`).

Known subclasses include `UsernamePasswordAuthenticationFilter`, `OAuth2LoginAuthenticationFilter`, `CasAuthenticationFilter`, `Saml2WebSsoAuthenticationFilter`. `http.formLogin()` installs the username/password filter and a `LoginUrlAuthenticationEntryPoint`. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

```java
public Authentication attemptAuthentication(HttpServletRequest req, HttpServletResponse res) {
    String username = req.getParameter("username");
    String password = req.getParameter("password");
    UsernamePasswordAuthenticationToken token =
            UsernamePasswordAuthenticationToken.unauthenticated(username, password);
    return getAuthenticationManager().authenticate(token);
}
```

**Listing 1.** Shape of `UsernamePasswordAuthenticationFilter` — not framework source. Custom login filters extend this class and override `attemptAuthentication`; they are not a random `OncePerRequestFilter` unless you want Bearer-style “continue the chain.”

> [!warning] Bearer JWT is not this hierarchy
> `BearerTokenAuthenticationFilter` extends **`OncePerRequestFilter`**. It converts a token on **each** request, authenticates, **saves context**, then **`filterChain.doFilter`**. No `attemptAuthentication`, no `SavedRequestAwareAuthenticationSuccessHandler`. Same idea (`AuthenticationManager`) — different type. See [[How do you configure JWT and form login as two SecurityFilterChain beans]].

> [!tip] Interview answer
> AbstractAuthenticationProcessingFilter is the form-login style base filter: match the login URL, attemptAuthentication, AuthenticationManager, then success or failure handlers and SecurityContext. UsernamePasswordAuthenticationFilter is the usual subclass. BearerTokenAuthenticationFilter is OncePerRequestFilter, not a child of this class.
