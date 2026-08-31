<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# What is AccessDeniedHandler?

> [!abstract] Short answer
> **`AccessDeniedHandler`** is the servlet callback that turns an **`AccessDeniedException`** into an HTTP response. **`ExceptionTranslationFilter`** invokes **`handle(request, response, ex)`** only when the caller is **fully authenticated** (not anonymous, not remember-me). Default **`AccessDeniedHandlerImpl`** sends **403** (`sendError`), or **forwards** to an error page if **`accessDeniedPage`** set it. **`CsrfFilter`** uses the **same** handler for a missing/invalid CSRF token. Unauthenticated denials go to **`AuthenticationEntryPoint`**, not this type.

## Translate authorization failure to HTTP

The interface is one method: **`handle(HttpServletRequest, HttpServletResponse, AccessDeniedException)`**. It does **not** decide access; **`AuthorizationFilter`** / method security already threw. The handler only **renders** the denial ([[What is ExceptionTranslationFilter in Spring Security]], [[What is the difference between AuthenticationException and AccessDeniedException]], [[What is AuthenticationEntryPoint]]).

**`ExceptionTranslationFilter`** (default handler **`AccessDeniedHandlerImpl`**):

- **`AuthenticationException`** → **`AuthenticationEntryPoint.commence`**
- **`AccessDeniedException`** + **anonymous or remember-me** → **`InsufficientAuthenticationException`** then the **entry point**
- **`AccessDeniedException`** + fully authenticated → **`accessDeniedHandler.handle`**

**`AccessDeniedHandlerImpl`**: if the response is already committed, it returns. With no **`errorPage`**, **`sendError(403)`**. With a page (must start with `/`), it sets status **403**, stores the exception as **`WebAttributes.ACCESS_DENIED_403`**, **forwards** (SecurityContext stays populated), and does **not** redirect.

Wire it with **`http.exceptionHandling(Customizer)`**: **`accessDeniedHandler(...)`**, shortcut **`accessDeniedPage("/errors/access-denied")`**, or **`defaultAccessDeniedHandlerFor`** (**since 5.1**, **`RequestMatcherDelegatingAccessDeniedHandler`** when several matchers). An explicit handler **replaces** those defaults ([[How do you customize the access denied page in Spring Security]], [[How do you handle authentication exceptions in Spring Security]]).

**`CsrfConfigurer`** copies **`ExceptionHandlingConfigurer.getAccessDeniedHandler(http)`** onto **`CsrfFilter`**, which calls the handler **directly** (the filter sits **before** translation) ([[What is CsrfFilter in Spring Security]]). **`LogoutHandler`-style cleanup does not apply** — this is response mapping only.

```java
http.exceptionHandling((exceptions) -> exceptions
	.accessDeniedHandler((request, response, ex) -> {
		response.setStatus(HttpServletResponse.SC_FORBIDDEN);
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		response.getWriter().write("{\"error\":\"forbidden\"}");
	})
);
```

**Listing 1.** Custom **`AccessDeniedHandler`** (functional interface). Prefer this over an HTML **`accessDeniedPage`** for APIs.

```java
http.exceptionHandling((exceptions) -> exceptions
	.accessDeniedPage("/errors/access-denied")
);
```

**Listing 2.** Official shortcut: **`AccessDeniedHandlerImpl.setErrorPage`**. You still provide a view at that path.

```d2
direction: down
ade: "AccessDeniedException" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
etf: "ExceptionTranslationFilter" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
csrf: "CsrfFilter\ninvalid token" {
  width: 200
  height: 50
  style.fill: "#fce4ec"
}
branch: "anonymous or remember-me?" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
ep: "AuthenticationEntryPoint" {
  width: 220
  height: 50
  style.fill: "#f3e5f5"
}
adh: "AccessDeniedHandler.handle\n403 / forward" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

ade -> etf -> branch
branch -> ep: "yes"
branch -> adh: "no"
csrf -> adh
```

**Fig. 1.** **403 UI** is this handler. **Login / 401** is the entry point. CSRF skips the translation filter but still lands here.

> [!warning] Authenticated-only (and remember-me is not “full”)
> Dumps that say “authenticated user → AccessDeniedHandler” miss **remember-me**: **`AuthenticationTrustResolver.isRememberMe`** still starts the **entry point**. Setting **`accessDeniedPage`** does **not** replace **`loginPage`**. A handler that **redirects** starts a new GET that must be authorized; the stock impl **forwards**.

> [!warning] One handler, two callers
> Customizing the access-denied **page** also changes **invalid CSRF** responses. Pairing **`accessDeniedPage`** with **`defaultAccessDeniedHandlerFor`** does nothing useful — the explicit page **wins**.

> [!tip] Interview answer
> AccessDeniedHandler.handle is how Spring Security turns AccessDeniedException into HTTP for a fully authenticated user, defaulting to 403 via AccessDeniedHandlerImpl. Anonymous and remember-me users never reach it; they hit AuthenticationEntryPoint. CsrfFilter uses the same handler, which is why accessDeniedPage also covers InvalidCsrfTokenException.
