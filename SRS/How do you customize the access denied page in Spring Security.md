<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# How do you customize the access denied page in Spring Security?

> [!abstract] Short answer
> On **`HttpSecurity.exceptionHandling(Customizer)`**, call **`accessDeniedPage("/errors/access-denied")`**. That is a shortcut for **`AccessDeniedHandlerImpl`** with that **error page**. **`ExceptionTranslationFilter`** invokes it only when an **already authenticated** request hits **`AccessDeniedException`** (not anonymous, not remember-me). With no page set, the default handler sends **HTTP 403**. For JSON or extra logic, set **`accessDeniedHandler(...)`**. The same handler is what **`CsrfFilter`** uses for a missing or invalid CSRF token.

## ExceptionTranslationFilter decides; the handler renders

Authorization denials from **`AuthorizationFilter`** or method security throw **`AccessDeniedException`**. **`ExceptionTranslationFilter`** (UI only — it does not enforce rules) catches it ([[What is ExceptionTranslationFilter in Spring Security]], [[What is AccessDeniedHandler]], [[What is the difference between AuthenticationException and AccessDeniedException]]):

- **`AuthenticationException`**, **anonymous**, or **remember-me** → **`AuthenticationEntryPoint`** (login / `WWW-Authenticate`). Remember-me is wrapped as **`InsufficientAuthenticationException`** (“full authentication is required”).
- Otherwise → **`AccessDeniedHandler.handle`**.

**`accessDeniedPage(url)`** builds **`AccessDeniedHandlerImpl`**, calls **`setErrorPage`**, and registers it. The path **must start with `/`** (context-relative). The handler **forwards** (not redirects) with status **403**, leaves **`SecurityContextHolder`** populated, and stores the exception under **`WebAttributes.ACCESS_DENIED_403`**. With no `errorPage`, it **`sendError(403)`**. You still provide a controller or view at that path.

**`HttpSecurity.exceptionHandling`** in **7.x** takes only a **`Customizer`**. The old **`http.exceptionHandling().accessDeniedPage(...)`** chain is gone.

**`defaultAccessDeniedHandlerFor(handler, RequestMatcher)`** (since **5.1**) selects a handler by request (for example HTML vs JSON). Several mappings become **`RequestMatcherDelegatingAccessDeniedHandler`**. An explicit **`accessDeniedPage` / `accessDeniedHandler`** **wins** and those defaults are unused.

**`CsrfConfigurer`** reads **`ExceptionHandlingConfigurer.getAccessDeniedHandler(http)`**, so this page also handles **`InvalidCsrfTokenException`**. **`CsrfFilter`** calls the handler **directly** (it sits **before** `ExceptionTranslationFilter`).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize
			.requestMatchers("/**").hasRole("USER")
		)
		.exceptionHandling((exceptionHandling) -> exceptionHandling
			.accessDeniedPage("/errors/access-denied")
		);
	return http.build();
}
```

**Listing 1.** Official **`HttpSecurity.exceptionHandling`** sample: denied users are **forwarded** to **`/errors/access-denied`**. Map that path in MVC (or a static resource).

```java
http.exceptionHandling((exceptions) -> exceptions
	.accessDeniedHandler((request, response, ex) -> {
		response.setStatus(HttpServletResponse.SC_FORBIDDEN);
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		response.getWriter().write("{\"error\":\"forbidden\"}");
	})
);
```

**Listing 2.** Custom **`AccessDeniedHandler`** when a browser error page is the wrong body (APIs). Prefer **`defaultAccessDeniedHandlerFor`** when HTML and JSON must differ — do not pair that with **`accessDeniedPage`**, which replaces the defaults.

```d2
direction: down
app: "AuthorizationFilter / method security\nAccessDeniedException" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
etf: "ExceptionTranslationFilter" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
csrf: "CsrfFilter\ninvalid / missing token" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
branch: "anonymous or remember-me?" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
ep: "AuthenticationEntryPoint\nlogin / 401" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}
adh: "AccessDeniedHandler\naccessDeniedPage → forward 403" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

app -> etf -> branch
branch -> ep: "yes"
branch -> adh: "no (fully authenticated)"
csrf -> adh
```

**Fig. 1.** Access-denied **page** runs only after a **fully authenticated** denial (or CSRF). Unauthenticated clients never see it ([[What is AuthenticationEntryPoint]], [[What is CsrfFilter in Spring Security]]).

> [!warning] Not the login page
> Unauthenticated (and **remember-me**) users hit **`AuthenticationEntryPoint`**, not **`accessDeniedPage`**. Setting a 403 view does not replace **`loginPage`**. A handler that **`sendRedirect`s** starts a **new** GET — that URL must be authorized; the stock page **forwards**, so **`FilterChainProxy`** (REQUEST dispatchers) does not re-check the error path.

> [!warning] CSRF lands on the same handler
> A missing or invalid CSRF token is an **`AccessDeniedException`** handled by this **`AccessDeniedHandler`**, not by the login entry point. An HTML access-denied page on a JSON API is usually the wrong 403 body — use a custom handler or **`defaultAccessDeniedHandlerFor`**.

> [!tip] Interview answer
> I call exceptionHandling with accessDeniedPage so AccessDeniedHandlerImpl forwards a 403 to my view, keeping the SecurityContext and the exception in WebAttributes.ACCESS_DENIED_403. That runs only for a fully authenticated AccessDeniedException; anonymous and remember-me users go to AuthenticationEntryPoint. CsrfFilter uses the same handler, so I do not assume the page is only for missing roles.
