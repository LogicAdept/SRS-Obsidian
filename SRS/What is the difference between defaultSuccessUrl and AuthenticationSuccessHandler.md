<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is the difference between defaultSuccessUrl and AuthenticationSuccessHandler?

> [!abstract] Short answer
> **`defaultSuccessUrl`** is a **DSL shortcut** (**since 3.2**, on **`AbstractAuthenticationFilterConfigurer`**: **`formLogin`**, **`oauth2Login`**, …). It **builds** a **`SavedRequestAwareAuthenticationSuccessHandler`**, sets **`defaultTargetUrl`**, optionally **`alwaysUseDefaultTargetUrl`**, and **installs** it via **`successHandler(...)`**. **`AuthenticationSuccessHandler`** (**since 3.0**) is the **strategy** the filter **actually calls** after **`Authentication`** is already in **`SecurityContext`**. A custom **`successHandler`** **replaces** that SavedRequest-aware redirect unless you **delegate**. Both write the **same** field — **last call wins**.

## Shortcut versus strategy

Form login success runs **after** credentials already matched ([[How does form login work internally in Spring Security]]). **`AbstractAuthenticationProcessingFilter.successfulAuthentication`** stores the context, **`RememberMeServices.loginSuccess`**, **`InteractiveAuthenticationSuccessEvent`**, then the **3-arg** **`onAuthenticationSuccess(request, response, authentication)`** — the **chain stops**. The default 4-arg method (**since 5.2**) calls **3-arg then `chain.doFilter`**; **`AuthenticationFilter`** (tokens) uses that path, form login does **not**.

**`successHandler(h)`** — Javadoc: the default is **`SavedRequestAwareAuthenticationSuccessHandler`** with **no extra properties** (fallback URL **`/`**). **`defaultSuccessUrl("/home")`** is **`defaultSuccessUrl("/home", false)`**: new SavedRequest-aware handler, **`setDefaultTargetUrl("/home")`**, **`alwaysUseDefaultTargetUrl = false`**, then **`successHandler(handler)`**. **`defaultSuccessUrl("/home", true)`** forces **`/home`** and **drops** the saved request.

SavedRequest-aware order ([[What is AuthenticationSuccessHandler in Spring Security]], [[What is SavedRequest]], [[What is RequestCache in Spring Security]]):

1. **`alwaysUseDefaultTargetUrl`** → **`defaultTargetUrl`**, remove cache
2. Else **`targetUrlParameter`** on the request (open-redirect risk)
3. Else **`RequestCache`** URL from **`ExceptionTranslationFilter`**
4. Else parent default (**`/`**, or the URL **`defaultSuccessUrl`** set)

There is **no** `successUrlByRole` DSL. ADMIN vs USER landing pages are a **custom** handler that reads **`authentication.getAuthorities()`**. **`successForwardUrl`** is a **different** shortcut: **forward**, still **`successHandler`**. Sibling: [[What is AuthenticationFailureHandler]].

**`AbstractAuthenticationFilterConfigurer.configure`** copies the **shared** **`RequestCache`** onto the **`defaultSuccessHandler`** field only. A **custom** **`SavedRequestAwareAuthenticationSuccessHandler`** passed to **`successHandler(...)`** keeps its **own** **`HttpSessionRequestCache`** unless you **`setRequestCache`**.

```java
http.formLogin((form) -> form
	.defaultSuccessUrl("/home", false)
);
```

**Listing 1.** Fallback **`/home`** when the user opened **`/login` directly**. A prior hit on a **protected** page still redirects to that **SavedRequest**. Pass **`true`** to **always** use **`/home`**.

```java
http.formLogin((form) -> form
	.successHandler((request, response, authentication) -> {
		boolean admin = authentication.getAuthorities().stream()
			.anyMatch((a) -> "ROLE_ADMIN".equals(a.getAuthority()));
		response.sendRedirect(request.getContextPath() + (admin ? "/admin" : "/home"));
	})
);
```

**Listing 2.** Role-based landing. This **replaces** SavedRequest-aware redirect. To keep deep links, **subclass** **`SavedRequestAwareAuthenticationSuccessHandler`** and override **`determineTargetUrl(..., Authentication)`** (fallback only).

```d2
direction: down
dsl: "defaultSuccessUrl(\"/home\")" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
saved: "SavedRequestAware handler\ndefaultTargetUrl=/home" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
iface: "AuthenticationSuccessHandler\nonAuthenticationSuccess" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
custom: "successHandler(custom)\nreplaces the shortcut" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}

dsl -> saved -> iface
custom -> iface
```

**Fig. 1.** The shortcut **is** a success handler. **`successHandler(...)`** swaps the strategy the filter invokes.

> [!warning] Last call wins; SavedRequest is easy to drop
> **`defaultSuccessUrl` then `successHandler`** (or the reverse) share **one** field. The **later** call **discards** the earlier. A **lambda** that **`sendRedirect`s** does **not** consult **`RequestCache`**. **`defaultSuccessUrl("/home")` does not mean “always `/home`”** — a SavedRequest still wins unless the second argument is **`true`**.

> [!warning] Redirect is the wrong success contract for JSON
> **`defaultSuccessUrl`** always installs a **redirect** handler. A browser login wants **302**; a JSON client typically wants **200** (or a JSON body). Wire **`successHandler`**: write the status/body yourself, or **`HttpMessageConverterAuthenticationSuccessHandler`** (**since 6.4**) which writes **`redirectUrl` + `authenticated`**. **`targetUrlParameter`** on the URL-based handlers is an **open redirect** if an attacker can set the parameter.

> [!tip] Interview answer
> defaultSuccessUrl is only a shortcut that builds SavedRequestAwareAuthenticationSuccessHandler with a fallback URL and alwaysUse flag, then calls successHandler. AuthenticationSuccessHandler is the strategy the filter runs after SecurityContext is already set. If I register my own handler I replace that SavedRequest redirect unless I delegate, and if I set both DSL methods the last one wins. I do not use defaultSuccessUrl for a JSON login; I write 200 in a custom handler instead.
