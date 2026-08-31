<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is AuthenticationFailureHandler?

> [!abstract] Short answer
> **`AuthenticationFailureHandler`** handles a **failed authentication attempt** — **`onAuthenticationFailure(request, response, AuthenticationException)`**. **`AbstractAuthenticationProcessingFilter`** (form **`POST /login`**) calls it after clearing **`SecurityContextHolder`**, storing the exception for the view, and **`RememberMeServices.loginFail`**. Default **`SimpleUrlAuthenticationFailureHandler`** **redirects** to **`/login?error`**. With **no** failure URL it sends **401**. This is **not** **`AuthenticationEntryPoint`** (unauthenticated **commence**) and **not** **`AccessDeniedHandler`** (**403** after you are already logged in).

## Report a rejected attempt, do not start login

Javadoc (**since 3.0**): typical behaviour is **redirect back to the login page** so the user can retry. Implementations may **branch on exception type** (e.g. **`CredentialsExpiredException`** → change-password URL) ([[How does form login work internally in Spring Security]], [[How do you handle authentication exceptions in Spring Security]]).

**`unsuccessfulAuthentication`** (always, then the handler):

1. Clear **`SecurityContextHolder`**
2. Cache the **`AuthenticationException`** (session, unless **forward** → request attribute)
3. **`RememberMeServices.loginFail`**
4. **`failureHandler.onAuthenticationFailure`**

The processing filter **catches** **`AuthenticationException`**. **`ExceptionTranslationFilter`** does **not** run this path.

**`formLogin.failureUrl("/login?error")`** is a shortcut for **`SimpleUrlAuthenticationFailureHandler`**. **`failureHandler(...)`** **replaces** that shortcut if both are set. **`failureForwardUrl`** uses a **forward**. **`ExceptionMappingAuthenticationFailureHandler`** maps **exception class names** to URLs, else the parent 401/redirect. Generated login pages read **`param.error`** and **`SPRING_SECURITY_LAST_EXCEPTION`** ([[How do you create a custom login form in Spring Security]], [[What account status flags does UserDetails expose]]).

**`AuthenticationFilter`** (bearer-style) defaults to **`AuthenticationEntryPointFailureHandler`** wrapping **`HttpStatusEntryPoint(UNAUTHORIZED)`** — **401**, not **`/login?error`**. HTTP Basic **bad credentials** go back to **`BasicAuthenticationEntryPoint`**, not this interface.

**`AccessDeniedHandler`** is **authorization** after a trusted **`Authentication`**. A **locked** account on **POST `/login`** is still **`LockedException` → this handler** (**`/login?error`**), not **403** ([[What is AuthenticationEntryPoint]], [[What is AccessDeniedHandler]]).

```java
http.formLogin((form) -> form
	.failureUrl("/login?error")
);
```

**Listing 1.** Default form behaviour made explicit. **`SimpleUrlAuthenticationFailureHandler`**: redirect (or **401** if the URL is unset).

```java
http.formLogin((form) -> form
	.failureHandler((request, response, ex) -> {
		response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		response.getWriter().write("{\"error\":\"unauthorized\"}");
	})
);
```

**Listing 2.** REST login **POST**: **401** JSON instead of a browser redirect.

```d2
direction: down
post: "POST /login\nAuthenticationException" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
filter: "AbstractAuthenticationProcessingFilter\nclear context, save exception" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
fh: "AuthenticationFailureHandler\n/login?error or 401" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ep: "AuthenticationEntryPoint\nnever called here" {
  width: 240
  height: 50
  style.fill: "#eceff1"
}

post -> filter -> fh
```

**Fig. 1.** Failure handler **finishes** a login attempt. Entry point **begins** one.

> [!warning] 401 JSON vs `/login?error`
> Leaving the default handler on a JSON API **302s** to HTML. **`exceptionHandling.authenticationEntryPoint`** does **not** replace **`failureHandler`** — you must set **both** if unauthenticated GETs and failed POSTs should both return JSON.

> [!warning] Not 403, not “user not found” vs “bad password”
> **`hideUserNotFoundExceptions`** (default **true**) turns a missing user into **`BadCredentialsException`** — same handler, same **`/login?error`**. **`DisabledException` / `LockedException`** still use this handler; map them with **`ExceptionMappingAuthenticationFailureHandler`** if the UI must differ. **`AccessDeniedHandler`** is the wrong type for a bad password.

> [!tip] Interview answer
> AuthenticationFailureHandler.onAuthenticationFailure runs when form login (or another AbstractAuthenticationProcessingFilter) fails after AuthenticationManager throws. The default SimpleUrlAuthenticationFailureHandler redirects to /login?error; APIs should write 401 instead. I do not confuse it with AuthenticationEntryPoint, which challenges an anonymous request, or AccessDeniedHandler, which is 403 for an already authenticated user.
