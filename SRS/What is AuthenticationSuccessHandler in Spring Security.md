<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is AuthenticationSuccessHandler in Spring Security?

> [!abstract] Short answer
> **`AuthenticationSuccessHandler`** runs **after** credentials already succeeded. **`AbstractAuthenticationProcessingFilter`** (form **`POST /login`**) sets **`SecurityContext`**, saves it, **`RememberMeServices.loginSuccess`**, publishes **`InteractiveAuthenticationSuccessEvent`**, then **`onAuthenticationSuccess(request, response, authentication)`** (**3-arg** — the chain **stops**). Default **`SavedRequestAwareAuthenticationSuccessHandler`** redirects to the **cached original URL**, else **`/`**. **`formLogin.successHandler(...)` replaces** that redirect. A JSON API should **write 200**, not **302**. **`AuthenticationFilter`** (tokens) calls the **4-arg** method (**since 5.2**), which **continues** the chain after the 3-arg method.

## Destination after a successful attempt

Javadoc (**since 3.0**): typical behaviour is **navigate** (redirect or forward). The filter has **already authenticated**; the handler does **not** call **`AuthenticationManager`** ([[How does form login work internally in Spring Security]], [[How do you create a custom login form in Spring Security]]).

**`SavedRequestAwareAuthenticationSuccessHandler`** (default on the processing filter):

1. **`alwaysUseDefaultTargetUrl`** → **`defaultTargetUrl`**, drop saved request
2. Else **`targetUrlParameter`** on the request
3. Else **`RequestCache`** URL saved by **`ExceptionTranslationFilter`**
4. Else the parent default (**`/`**)

**`defaultSuccessUrl("/app")`** sets that default; **`defaultSuccessUrl("/app", true)`** always uses it. **`successHandler(h)`** **replaces** SavedRequest (a lambda does **not** call super). **`successForwardUrl`** forwards instead of redirect. Role-based landing pages are a **custom** handler inspecting **`authentication.getAuthorities()`** — there is no `successUrlByRole` DSL.

Form login uses **3-arg** success, so the **controller is not invoked** on **`POST /login`**. **`AuthenticationFilter`** uses **4-arg**; the default 4-arg implementation calls **3-arg then `chain.doFilter`**. Leaving **SavedRequestAware** on a bearer filter **redirects** instead of hitting the API — use a **no-op 3-arg** handler ([[How do you implement custom token-based authentication in Spring Security]]). Sibling: **`AuthenticationFailureHandler`** ([[What is AuthenticationFailureHandler]]). This is **not** **`AuthenticationEntryPoint`** ([[What is AuthenticationEntryPoint]]).

```java
http.formLogin((form) -> form
	.defaultSuccessUrl("/home", false)
);
```

**Listing 1.** Saved-request redirect when the user hit a protected page first; otherwise **`/home`**. **`true`** as the second argument **always** goes to **`/home`**.

```java
http.formLogin((form) -> form
	.successHandler((request, response, authentication) -> {
		response.setStatus(HttpServletResponse.SC_OK);
		response.setContentType(MediaType.APPLICATION_JSON_VALUE);
		response.getWriter().write("{\"status\":\"ok\"}");
	})
);
```

**Listing 2.** REST login: **200** JSON. This **drops** SavedRequest unless you wrap **`SavedRequestAwareAuthenticationSuccessHandler`**.

```d2
direction: down
ok: "AuthenticationManager success" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
ctx: "SecurityContext + session\nremember-me, event" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
sh: "AuthenticationSuccessHandler\nSavedRequest / default URL / JSON" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}

ok -> ctx -> sh
```

**Fig. 1.** Context is stored **before** the handler. The handler only **chooses the next HTTP step**.

> [!warning] `successHandler` replaces SavedRequest
> If you implement a custom handler and **do not** delegate to **`SavedRequestAwareAuthenticationSuccessHandler`**, the user **loses** the original URL (deep link after login). **`continueChainBeforeSuccessfulAuthentication`** defaults **false** — do not expect **`POST /login`** to reach an MVC `@PostMapping("/login")`.

> [!warning] 3-arg vs 4-arg
> Form login **must not** continue the chain after a **302**. Token **`AuthenticationFilter`** **must** continue after setting the context. Copying **SavedRequestAware** onto a stateless API yields a **redirect to `/`**, not the resource. **`AuthenticationEntryPoint`** is the wrong type for “where to go after password matched.”

> [!tip] Interview answer
> AuthenticationSuccessHandler runs after UsernamePasswordAuthenticationFilter has already put Authentication in the SecurityContext. The default SavedRequestAwareAuthenticationSuccessHandler sends the browser back to the page that triggered login, or to defaultSuccessUrl. I replace it for JSON 200 responses, knowing that drops SavedRequest, and I use a no-op 3-arg handler on AuthenticationFilter so the 4-arg method continues the chain.
