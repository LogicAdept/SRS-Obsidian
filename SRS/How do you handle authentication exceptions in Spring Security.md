<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you handle authentication exceptions in Spring Security?

> [!abstract] Short answer
> **`AuthenticationException`** has **two** servlet paths. An **unauthenticated** call to a protected resource is translated by **`ExceptionTranslationFilter`** into **`AuthenticationEntryPoint.commence`** (form: redirect to login; Basic: **401** + **`WWW-Authenticate`**; APIs: write **401** JSON). A **failed login POST** is caught by **`AbstractAuthenticationProcessingFilter`**, which clears the context and calls **`AuthenticationFailureHandler`** (form default: redirect **`/login?error`**). Do not wire only **`exceptionHandling.authenticationEntryPoint`** and assume every auth failure hits it. **Authenticated** missing-authority is **`AccessDeniedHandler`** (**403**), not an entry point.

## Commence vs failed attempt

**`AuthenticationException`** is the abstract type for an invalid authentication. **`ExceptionTranslationFilter`** does **not** enforce rules; it maps exceptions to HTTP ([[What is ExceptionTranslationFilter in Spring Security]], [[What is AuthenticationEntryPoint]], [[What is AuthenticationFailureHandler]]):

| Situation | Who handles it | Typical HTTP |
| --- | --- | --- |
| No (or anonymous) authentication on a protected resource | **`AuthenticationEntryPoint`** | **302** to login, or **401** |
| Remember-me / anonymous **`AccessDeniedException`** | Same entry point (`InsufficientAuthenticationException`) | Same |
| Form (or other `AbstractAuthenticationProcessingFilter`) **attempt fails** | **`AuthenticationFailureHandler`** | **302** `/login?error`, or **401** |
| HTTP Basic **bad credentials** | **`BasicAuthenticationEntryPoint`** again | **401** + challenge |
| Fully authenticated, missing authority | **`AccessDeniedHandler`** | **403** |

With **no** `formLogin` / `httpBasic` entry point registered, **`ExceptionHandlingConfigurer`** defaults to **`Http403ForbiddenEntryPoint`**, which always **`sendError(403)`** — not 401. **`formLogin`** registers **`LoginUrlAuthenticationEntryPoint`**. **`httpBasic`** registers **`BasicAuthenticationEntryPoint`**. Several matchers use **`defaultAuthenticationEntryPointFor`** (**`DelegatingAuthenticationEntryPoint`**). An explicit **`authenticationEntryPoint(...)`** **replaces** those defaults.

Failed **form** attempts never reach the translation filter: **`unsuccessfulAuthentication`** clears **`SecurityContextHolder`**, stores the exception for the view (**`WebAttributes`** / session), calls **`RememberMeServices.loginFail`**, then **`AuthenticationFailureHandler`**. Default is **`SimpleUrlAuthenticationFailureHandler`** → **`/login?error`**. With **no** failure URL it sends **401**. **`ExceptionMappingAuthenticationFailureHandler`** maps exception **class names** to URLs (for example credentials expired). **`getAuthenticationRequest()`** on the exception is since **6.5**.

**`HttpSecurity.exceptionHandling`** takes a **`Customizer`** in **7.x**. **`formLogin.failureUrl` / `failureHandler` / `failureForwardUrl`** configure the other path ([[How do you create a custom login form in Spring Security]], [[How do you configure HTTP Basic authentication in Spring Security]], [[How do you customize the access denied page in Spring Security]], [[What is the difference between AuthenticationException and AccessDeniedException]]).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.exceptionHandling((exceptions) -> exceptions
			.authenticationEntryPoint((request, response, ex) -> {
				response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
				response.setContentType(MediaType.APPLICATION_JSON_VALUE);
				response.getWriter().write("{\"error\":\"unauthorized\"}");
			})
		);
	return http.build();
}
```

**Listing 1.** JSON **commence** path. Use **`defaultAuthenticationEntryPointFor`** if the same app still needs a login redirect for browsers — a single **`authenticationEntryPoint`** **overrides** form-login’s **`LoginUrlAuthenticationEntryPoint`**.

```java
http
	.formLogin((form) -> form
		.failureUrl("/login?error")
		.failureHandler((request, response, ex) -> {
			response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
			response.setContentType(MediaType.APPLICATION_JSON_VALUE);
			response.getWriter().write("{\"error\":\"bad_credentials\"}");
		})
	);
```

**Listing 2.** Failed **POST /login**. **`failureHandler`** replaces the default **`SimpleUrlAuthenticationFailureHandler`**. **`failureUrl`** is a shortcut for that handler with a redirect; calling **both** as here, the **handler wins**. Pick one.

```d2
direction: down
deny: "protected resource\nno Authentication" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
post: "POST /login\nBadCredentialsException" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
etf: "ExceptionTranslationFilter" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
filter: "AbstractAuthenticationProcessingFilter\nunsuccessfulAuthentication" {
  width: 300
  height: 70
  style.fill: "#fce4ec"
}
ep: "AuthenticationEntryPoint.commence\nlogin / 401 JSON / WWW-Authenticate" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
fh: "AuthenticationFailureHandler\n/login?error or 401" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}
adh: "AccessDeniedHandler\n403 (already authenticated)" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}

deny -> etf -> ep
post -> filter -> fh
etf -> adh: "authenticated + AccessDeniedException"
```

**Fig. 1.** Entry point **starts** authentication. Failure handler **reports** a rejected attempt. **403** is authorization, not a failed login.

> [!warning] 401 is not “any security exception”
> A logged-in user missing a role is **`AccessDeniedException`** → **403**. Returning **401** there makes clients retry credentials they already sent. Conversely, with neither form nor Basic configured, the **default entry point is 403**, so “unauthenticated always 401” is also false unless you set one.

> [!warning] One `authenticationEntryPoint` replaces form login’s redirect
> Setting a JSON entry point on **`exceptionHandling`** is the right API commence path and the **wrong** default for a browser **`formLogin`** app unless you **`defaultAuthenticationEntryPointFor`** by **`RequestMatcher`**. Failed form POSTs still need **`failureHandler`** (or **`failureUrl`**) or they keep redirecting to **`/login?error`**.

> [!tip] Interview answer
> I split commence from failed attempt. ExceptionTranslationFilter calls AuthenticationEntryPoint when the caller is not fully authenticated; form login’s UsernamePasswordAuthenticationFilter calls AuthenticationFailureHandler on a bad POST. I set exceptionHandling.authenticationEntryPoint for 401 JSON APIs, and formLogin.failureHandler for login failures. Authenticated authorization failures go to AccessDeniedHandler as 403, not 401.
