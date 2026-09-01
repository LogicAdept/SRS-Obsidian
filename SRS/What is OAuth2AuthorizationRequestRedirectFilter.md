<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/OAuth2 #Java/Spring/Security/OAuth2 #SRS

# What is `OAuth2AuthorizationRequestRedirectFilter`?

> [!abstract] Short answer
> An **`OncePerRequestFilter`** (since **5.0**) that **starts the Authorization Code grant**: it builds the Authorization Request and **redirects the browser to the Authorization Server**. Default match: **`/oauth2/authorization/{registrationId}`**. Installed by **`http.oauth2Login()`** (and used by `oauth2Client` code-grant). It is **OAuth2 Client / SSO**, **not** [[What is BearerTokenAuthenticationFilter]] on a resource server. It sits **after `LogoutFilter`**, **before** [[What is UsernamePasswordAuthenticationFilter]].

## Redirect out; a different filter comes back

```d2
direction: down
hit: "GET /oauth2/authorization/{id}" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
redir: "OAuth2AuthorizationRequestRedirectFilter\n302 to AS /authorize" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
cb: "GET /login/oauth2/code/{id}?code=\nOAuth2LoginAuthenticationFilter" {
  width: 340
  height: 50
  style.fill: "#fff3e0"
}

hit -> redir
redir -> cb: "after user consents"
```

**Fig. 1.** Javadoc: request includes client id, scopes, `state`, `response_type`, redirect URI. Callback default is `{baseUrl}/login/oauth2/code/{registrationId}` — **another** filter. Default login page ([[What is DefaultLoginPageGeneratingFilter]]) links to `DEFAULT_AUTHORIZATION_REQUEST_BASE_URI + "/{registrationId}"`. See [[What is FilterOrderRegistration]] and [[What is HttpSecurity in Spring Security]].

Dump “~600” is **wrong** (`FilterOrderRegistration` registers this by **class name** right after `LogoutFilter`, order **1300**). Override the base URI with `oauth2Login().authorizationEndpoint().baseUri(...)`. Needs a **`ClientRegistrationRepository`**.

```java
http.oauth2Login(Customizer.withDefaults());
// GET /oauth2/authorization/google → 302 to Google's authorization endpoint
```

**Listing 1.** `HttpSecurity.oauth2Login` (Authorization Code / OIDC). Boot `spring.security.oauth2.client.registration.*` supplies the `ClientRegistration`. Customize resolver via `OAuth2AuthorizationRequestResolver`.

> [!warning] Client redirect, not Bearer
> Resource-server JWT/opaque tokens never hit this filter. `securityMatcher("/api/**")` + `oauth2ResourceServer` is **Bearer**. A missing `ClientRegistration` or a login-page link that does not match `authorizationEndpoint().baseUri()` starts **no** flow. Do not confuse `/oauth2/authorization/{id}` (this app → IdP) with an **Authorization Server’s** `/oauth2/authorize`.

> [!tip] Interview answer
> OAuth2AuthorizationRequestRedirectFilter is the OAuth2 Login kickoff: GET /oauth2/authorization/{registrationId} redirects the browser to the IdP. The code callback is a different filter. It is not BearerTokenAuthenticationFilter. Spring Security 6 installs it with oauth2Login, after LogoutFilter and before form login.
