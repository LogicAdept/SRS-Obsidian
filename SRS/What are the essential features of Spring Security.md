<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# What are the essential features of Spring Security?

> [!abstract] Short answer
> Official one-liner: **authentication, authorization, and protection against common attacks**, for **Servlet and reactive** apps. On Servlet, that is a **`SecurityFilterChain`**: **`AuthenticationManager`**, **`AuthorizationManager` / `AuthorizationFilter`**, **CSRF**, **security headers** (clickjacking via **`X-Frame-Options`**), **session-fixation** (**`changeSessionId()`** on login). **Servlet API** wrapping is on by default. **Spring MVC** (`@AuthenticationPrincipal`, CSRF form tags) is **optional**. **JAAS**, **OAuth2/OIDC login**, **CAS**, **SAML** are **providers you add**, not `spring-boot-starter-security`.

## What the dump lists, mapped to current APIs

The interview list is the old Features chapter. Current docs still group the same work: authenticate, authorize, stop exploits, then optional integrations.

| Dump line | What ships |
| --- | --- |
| Flexible authentication / authorization | Many **`AuthenticationProvider`s** (DAO, JWT, OAuth2, SAML, CAS, JAAS, …). HTTP rules via **`authorizeHttpRequests`**. Method security is extra. |
| Session fixation, clickjacking, CSRF | **On by default** for a session-backed Servlet app. Fixation: **`HttpServletRequest.changeSessionId()`**. Clickjacking: **`HeaderWriterFilter`** / **`X-Frame-Options`**. CSRF: **`CsrfFilter`** on unsafe methods. |
| Servlet API integration | **`SecurityContextHolderAwareRequestFilter`**: **`getRemoteUser()`**, **`getUserPrincipal()`**, **`isUserInRole`**, Servlet 3 **`login` / `logout` / `authenticate`**. |
| Optional Spring MVC | **`@EnableWebSecurity`** registers **`@AuthenticationPrincipal`**, **`@CurrentSecurityContext`**, **`CsrfToken`** resolvers, MVC form CSRF. Path matchers can share MVC’s **`PathPatternParser`**. |
| JAAS | **`JaasAuthenticationProvider` / `DefaultJaasAuthenticationProvider`** — delegate to a **`LoginModule`**, map principals with **`AuthorityGranter`**. No `http.jaas()`. |
| SSO | **Not a default.** **`oauth2Login()`**, **SAML 2.0 Web Browser SSO**, or **CAS** (`CasAuthenticationEntryPoint` + ticket validation). |

```java
@GetMapping("/me")
String me(@AuthenticationPrincipal UserDetails user, HttpServletRequest request) {
	return user.getUsername() + " / " + request.getRemoteUser();
}
```

**Listing 1.** MVC resolver (optional) and Servlet wrapper (default) read the **same** `Authentication` ([[What are the core components of Spring Security]], [[How do you integrate Spring Security with Thymeleaf]]).

```d2
direction: down
core: "Authn + Authz\nFilterChainProxy" {
  width: 220
  height: 48
  style.fill: "#c8e6c9"
}
exploit: "CSRF, headers,\nsession fixation" {
  width: 220
  height: 48
  style.fill: "#fff3e0"
}
integ: "Servlet API\noptional MVC" {
  width: 200
  height: 48
  style.fill: "#e3f2fd"
}
sso: "OAuth2 / SAML / CAS\nJAAS LoginModule" {
  width: 240
  height: 48
  style.fill: "#ffcdd2"
}

core -> exploit
exploit -> integ
integ -> sso: "you configure" {
  style.stroke: "#c62828"
}
```

**Fig. 1.** Green/orange/blue are the starter’s job. Red is federation or JAAS — extra modules and DSL, not “add the starter” ([[How does Spring Security mitigate XSS CSRF and clickjacking]], [[How do you handle session fixation in Spring Security]], [[How do you implement OAuth2 login in Spring Security]], [[What is CAS authentication in Spring Security]], [[What is JAAS support in Spring Security]]).

Reactive WebFlux is first-class in the same product (`SecurityWebFilterChain`). The dump is Servlet-shaped.

> [!warning] SSO is not `starter-security`
> `spring-boot-starter-security` gives form/basic, CSRF, headers, session-fixation, Servlet wrapping. One account across apps still needs **`oauth2Login()`** (client registration), **SAML relying-party** metadata, or a **CAS server** plus `CasAuthenticationFilter`. JAAS is a **`LoginModule`**, not SSO.

> [!warning] MVC is optional; XSS is not a sanitizer
> A JAX-RS or WebFlux app still uses the filter (or WebFilter) chain. Spring Security does **not** HTML-encode templates; XSS is headers plus your encoding. **`X-Frame-Options` is clickjacking**, not an XSS filter.

> [!tip] Interview answer
> Essential features are authentication, authorization, and default exploit protection (CSRF, clickjacking headers, session-fixation on login), plus Servlet API integration. Spring MVC helpers are optional. JAAS, OAuth2 login, SAML, and CAS are pluggable, not automatic SSO.
