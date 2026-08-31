<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between HTTP 401 and 403 in Spring Security?

> [!abstract] Short answer
> **401** means **authenticate** (or send credentials again): Spring does **not** accept **who** you are. **403** means **authorization failed** for a **fully authenticated** user: Spring knows **who** you are and **refuses** the action. **`ExceptionTranslationFilter` does not map those numbers 1:1.** **`AuthenticationException`** goes to **`AuthenticationEntryPoint`** — Basic/JWT **401**, form login **302** to **`/login`**, and with **no** form/Basic the default is **`Http403ForbiddenEntryPoint` (403)**. **`AccessDeniedException`** is **403** only when **`isFullyAuthenticated`**. Anonymous and remember-me ADE **commence login** instead. The HTTP name **Unauthorized** is **identity**, not “not allowed.”

## Status is chosen by the handler, not the exception name

HTTP: **401** is “lacking valid authentication credentials” (typically **`WWW-Authenticate`**). **403** is “understood, refused.” Spring implements that split through **entry point vs access-denied handler**, not by always calling **`sendError(401)`** ([[What is the difference between AuthenticationException and AccessDeniedException]], [[What is AuthenticationEntryPoint]], [[What is AccessDeniedHandler]]).

| Situation | Typical status | Who writes it |
| --- | --- | --- |
| No credentials, **HTTP Basic** | **401** + **`WWW-Authenticate: Basic`** | **`BasicAuthenticationEntryPoint`** |
| No credentials, **form login** | **302** **`GET /login`** | **`LoginUrlAuthenticationEntryPoint`** |
| No credentials, **neither** form nor Basic | **403** | **`Http403ForbiddenEntryPoint`** (configurer default) |
| Failed **form POST /login** | **302** **`/login?error`** (or **401** if no failure URL) | **`AuthenticationFailureHandler`** |
| Logged-in user, missing **role** / **`@PreAuthorize`** | **403** | **`AccessDeniedHandlerImpl`** |
| **Anonymous / remember-me** + **`AccessDeniedException`** | Same as unauthenticated (login / **401**) | Entry point via **`InsufficientAuthenticationException`** |
| Invalid **CSRF** on a session user | **403** | **`CsrfFilter`** → same **`AccessDeniedHandler`** |

A JSON API that wants **401** must set **`authenticationEntryPoint`** (or **`httpBasic` / `oauth2ResourceServer`**). **`formLogin()`** alone **redirects** browsers; it does **not** send 401. **`HttpStatusEntryPoint(UNAUTHORIZED)`** is the usual API commence ([[How do you handle authentication exceptions in Spring Security]], [[How do you configure HTTP Basic authentication in Spring Security]]).

```java
http
	.authorizeHttpRequests((authorize) -> authorize
		.requestMatchers("/admin/**").hasRole("ADMIN")
		.anyRequest().authenticated())
	.httpBasic(Customizer.withDefaults());
```

**Listing 1.** Missing **`Authorization`** → **401**. Logged-in **`USER`** on **`/admin`** → **403**.

```java
http.exceptionHandling((exceptions) -> exceptions
	.authenticationEntryPoint((request, response, ex) ->
		response.sendError(HttpServletResponse.SC_UNAUTHORIZED))
	.accessDeniedHandler((request, response, ex) ->
		response.sendError(HttpServletResponse.SC_FORBIDDEN)));
```

**Listing 2.** Explicit **401 vs 403** for an API. Without this, a chain with **no** form/Basic already answers unauthenticated calls with **403**.

```d2
direction: down
who: "who are you?\nAuthenticationException / anonymous ADE" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
what: "you may not\nADE + fully authenticated" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ep: "AuthenticationEntryPoint\n401 / 302 login / default 403" {
  width: 300
  height: 70
  style.fill: "#f3e5f5"
}
adh: "AccessDeniedHandler\n403" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

who -> ep
what -> adh
```

**Fig. 1.** **401** is a **challenge** (or a login redirect). **403** is a **final no** for a known user.

> [!warning] 401 is not “not allowed”
> Interview mix-up: **Unauthorized** = **not authenticated**. **Forbidden** = **authenticated, denied**. Form login’s unauthenticated path is often **302**, so “I never see 401” is expected. **`Http403ForbiddenEntryPoint`** makes missing login look like **authorization failed**.

> [!warning] Empty `Authentication` is not a 403 rule
> **`AnonymousAuthenticationFilter`** still installs a principal. A filter that **never** authenticates a real user keeps you **anonymous**: **`hasRole("ADMIN")`** becomes a **login challenge**, not **403**. CSRF **403** on POST is **ADE**, not a failed login ([[What is CsrfFilter in Spring Security]], [[What is AuthenticationFailureHandler]], [[How do you customize the access denied page in Spring Security]]).

> [!tip] Interview answer
> 401 means Spring Security wants authentication — Basic and JWT send 401 plus WWW-Authenticate; form login usually redirects to /login instead. 403 means a fully authenticated user failed authorization, including @PreAuthorize and CSRF. ExceptionTranslationFilter maps exception types to those handlers; it does not always emit 401 for AuthenticationException or 403 for AccessDeniedException. Anonymous AccessDeniedException is a challenge, not 403.
