<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `ChannelProcessingFilter`?

> [!abstract] Short answer
> The **deprecated** early servlet filter that enforces **HTTP vs HTTPS** (the “channel”) **before** authentication. XML `requires-channel` / Java `http.requiresChannel(...)` add it. It looks up attributes (`REQUIRES_SECURE_CHANNEL`, `REQUIRES_INSECURE_CHANNEL`, `ANY_CHANNEL`) and delegates to a **`ChannelDecisionManager`**, which typically **redirects** and **commits** the response so the rest of the chain does not run. Spring Security **7** points you at **`HttpsRedirectFilter`** and **`http.redirectToHttps(...)`**. It does **not** terminate TLS.

## Very early, then stop or continue

```d2
direction: down
early: "DisableEncodeUrlFilter …\nChannelProcessingFilter" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
cdm: "ChannelDecisionManager\nSecure / Insecure processors" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
redir: "redirect + response committed" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}
rest: "SecurityContext, login, AuthorizationFilter" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}

early -> cdm
cdm -> redir: "wrong channel"
cdm -> rest: "ok / ANY_CHANNEL"
```

**Fig. 1.** `FilterOrderRegistration` places it near the **front** (just before **`HttpsRedirectFilter`**). Login never sees an HTTP request that was supposed to be HTTPS. See [[What is FilterChainProxy and DelegatingFilterProxy]].

XML: any `<intercept-url requires-channel="https|http|any">` installs this filter. Java: deprecated **`requiresChannel((c) -> c.anyRequest().requiresSecure())`**. Replacement:

```java
http.redirectToHttps(Customizer.withDefaults());
```

**Listing 1.** Current DSL on a `SecurityFilterChain`. `PortMapperImpl` default map: **80→443**, **8080→8443**. Prefer **all** requests HTTPS; mixing HTTP and HTTPS is supported on the old API and **not recommended**. See [[How do you require HTTPS with Spring Security]] and [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

`ChannelProcessingFilter` is a `GenericFilterBean` marked **`@Deprecated`**. Deprecated list: use **`HttpsRedirectFilter`** and its `PortMapper`. `HttpSecurity.requiresChannel` → **`redirectToHttps`**. Behind a reverse proxy, Security still only **sees** `HttpServletRequest.isSecure()` / forwarded headers — the **container or proxy** terminates TLS (`server.ssl.*` on Boot). This filter is the **redirect/enforce** layer on top, not the certificate.

> [!warning] Deprecated, and not your TLS terminator
> New code should not add `ChannelProcessingFilter` by hand. `redirectToHttps` / `HttpsRedirectFilter` is the supported path. If the decision manager **commits** the response, CSRF, form login, and `AuthorizationFilter` **do not run** on that request — by design.

> [!tip] Interview answer
> ChannelProcessingFilter is the old early filter for requires-channel: it redirects HTTP to HTTPS via ChannelDecisionManager before authentication. It is deprecated in favor of HttpsRedirectFilter and redirectToHttps. Boot SSL is the container; this filter only enforces the URL scheme.
