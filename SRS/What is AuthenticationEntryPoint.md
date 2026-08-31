<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is AuthenticationEntryPoint?

> [!abstract] Short answer
> **`AuthenticationEntryPoint`** **commences** an authentication scheme when the caller is **not fully authenticated**. **`ExceptionTranslationFilter`** calls **`commence(request, response, AuthenticationException)`** after saving the request. Form login: **`LoginUrlAuthenticationEntryPoint`** **redirects** to **`/login`**. HTTP Basic: **`BasicAuthenticationEntryPoint`** sends **401** + **`WWW-Authenticate: Basic`**. With **no** form/Basic registered, the default is **`Http403ForbiddenEntryPoint`** (**403**, not 401). A failed **form POST** uses **`AuthenticationFailureHandler`**, not this type. Fully authenticated **403** uses **`AccessDeniedHandler`**.

## Commence, do not authenticate

Javadoc: *Used by ExceptionTranslationFilter to commence an authentication scheme.* Implementations **change the response** (redirect, challenge header, JSON body). They do **not** call **`AuthenticationManager`**. The translation filter records the original URL (**`RequestCache`**) before **`commence`** so success can replay it ([[What is ExceptionTranslationFilter in Spring Security]], [[How do you handle authentication exceptions in Spring Security]]).

Invoked when:

- **`AuthenticationException`** bubbles from the rest of the chain
- **`AccessDeniedException`** and the user is **anonymous or remember-me** (`InsufficientAuthenticationException`)

**Not** invoked for **`UsernamePasswordAuthenticationFilter`** / **`AbstractAuthenticationProcessingFilter`** failures — those go to **`AuthenticationFailureHandler`** (**`/login?error`**) ([[What is AuthenticationFailureHandler]], [[How do you create a custom login form in Spring Security]]). **Not** invoked for a **fully authenticated** missing role — **`AccessDeniedHandler`** (**403**) ([[What is AccessDeniedHandler]]).

Stock implementations:

| Type | Typical HTTP |
| --- | --- |
| **`LoginUrlAuthenticationEntryPoint`** | **302** to the login form |
| **`BasicAuthenticationEntryPoint`** | **401** + **`WWW-Authenticate`** ([[How do you configure HTTP Basic authentication in Spring Security]]) |
| **`HttpStatusEntryPoint`** | Bare status (JS clients; browser will not intercept like Basic) |
| **`Http403ForbiddenEntryPoint`** | Always **403** — **`ExceptionHandlingConfigurer`** default if nothing else is registered |

**`formLogin` / `httpBasic`** register their entry points via **`defaultAuthenticationEntryPointFor`**. Several matchers become **`DelegatingAuthenticationEntryPoint`**. A single **`authenticationEntryPoint(...)`** **replaces** form-login’s redirect. **`X-Requested-With: XMLHttpRequest`** suppresses Basic’s **`WWW-Authenticate`** so the browser dialog stays down.

```java
http.exceptionHandling((exceptions) -> exceptions
	.authenticationEntryPoint((request, response, ex) -> {
		response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		response.getWriter().write("{\"error\":\"unauthorized\"}");
	})
);
```

**Listing 1.** API **commence**: **401** JSON. On a browser app this **overrides** **`LoginUrlAuthenticationEntryPoint`** unless you also **`defaultAuthenticationEntryPointFor`**.

```java
http.httpBasic(Customizer.withDefaults());
```

**Listing 2.** Registers **`BasicAuthenticationEntryPoint`**. No extra `exceptionHandling` needed for the challenge.

```d2
direction: down
need: "no full Authentication\nor AuthenticationException" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
etf: "ExceptionTranslationFilter\nRequestCache then commence" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ep: "AuthenticationEntryPoint\nlogin 302 / 401 challenge / JSON" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
fail: "failed POST /login\nAuthenticationFailureHandler" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

need -> etf -> ep
fail -> fail
```

**Fig. 1.** Entry point **starts** login. Failure handler **reports** a rejected attempt. They are different strategies.

> [!warning] Default is not 401
> Without form or Basic, unauthenticated access is **`Http403ForbiddenEntryPoint`**. A JSON API that never sets an entry point looks like **authorization failed**. A JSON API that only sets **`formLogin`** **302s** to HTML **`/login`** — the dump trap is real.

> [!warning] One `authenticationEntryPoint` replaces the login redirect
> Use **`defaultAuthenticationEntryPointFor(entryPoint, RequestMatcher)`** when browsers and APIs share a chain. Remember-me denials **commence** again; they do not hit **`AccessDeniedHandler`**.

> [!tip] Interview answer
> AuthenticationEntryPoint.commence is the unauthenticated challenge: LoginUrlAuthenticationEntryPoint for form login, BasicAuthenticationEntryPoint for WWW-Authenticate. ExceptionTranslationFilter calls it for AuthenticationException and for anonymous or remember-me AccessDeniedException. Failed form POSTs use AuthenticationFailureHandler instead, and a missing role on a logged-in user uses AccessDeniedHandler.
