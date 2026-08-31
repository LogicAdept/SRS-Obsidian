<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `BasicAuthenticationFilter`?

> [!abstract] Short answer
> An **`OncePerRequestFilter`** that, on every request with **`Authorization: Basic`** plus **Base64(`username:password`)**, builds a **`UsernamePasswordAuthenticationToken`** and calls **`AuthenticationManager`**. **`http.httpBasic(Customizer.withDefaults())`** adds it (and a **`BasicAuthenticationEntryPoint`** that sends **`WWW-Authenticate`**). Success **continues the filter chain** — it is **not** `UsernamePasswordAuthenticationFilter` (form POST `/login`). Base64 is **encoding**, not encryption.

## Header on this request, then continue

```d2
direction: down
req: "request" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
hdr: "Authorization: Basic … ?" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
bam: "BasicAuthenticationFilter\nUsernamePasswordAuthenticationToken" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
etf: "ExceptionTranslationFilter\nBasicAuthenticationEntryPoint" {
  width: 300
  height: 50
  style.fill: "#fce4ec"
}
chain: "FilterChain.doFilter" {
  width: 200
  height: 36
  style.fill: "#e8f5e9"
}

req -> hdr
hdr -> bam: "yes"
hdr -> etf: "no / 401"
bam -> chain: "success"
bam -> etf: "failure"
```

**Fig. 1.** Challenge is `WWW-Authenticate`; credentials are on the **same** request class as Basic, not a login form. `RequestCache` is typically **`NullRequestCache`** (client retries). See [[How does Spring Security authenticate an HTTP request end to end]].

Default **Boot / synthesized** chain includes HTTP Basic. **Any** `SecurityFilterChain` you write must **opt in** with `httpBasic`. If **form login** is also on, that entry point **wins**; the Basic **filter** still reads the header. `X-Requested-With: XMLHttpRequest` **suppresses** `WWW-Authenticate` so the browser dialog does not steal an SPA. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]].

```java
http.httpBasic(Customizer.withDefaults());
```

**Listing 1.** DSL that installs `BasicAuthenticationFilter`. Prefer this over `new BasicAuthenticationFilter()` plus `addFilterAt` — **`httpBasic()` already adds one**, and a second `addFilterAt(..., BasicAuthenticationFilter.class)` **fails**. Landmark for **`addFilterAfter(custom, BasicAuthenticationFilter.class)`** is this class, **not** `UsernamePasswordAuthenticationFilter`. See [[What is addFilterAfter in Spring Security]] and [[What is AbstractAuthenticationProcessingFilter]].

Failure: clear `SecurityContextHolder`, `AuthenticationEntryPoint` (401 + `WWW-Authenticate`). Success: set `Authentication`, merge existing authorities, **`doFilter`** into `AuthorizationFilter`.

> [!warning] Base64 is not a password hash
> `Authorization: Basic …` is reversible `username:password`. It is **not** form login and **not** Bearer JWT. Use TLS in front (`redirectToHttps`); this filter does not encrypt the header. See [[How do you require HTTPS with Spring Security]].

> [!tip] Interview answer
> BasicAuthenticationFilter is OncePerRequestFilter: it decodes Authorization Basic, authenticates with AuthenticationManager, then continues the chain. httpBasic() adds it; form login is a different filter and usually a different entry point. Base64 is encoding, so put HTTPS in front.
