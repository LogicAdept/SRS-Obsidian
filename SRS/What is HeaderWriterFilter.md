<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/AppSec #SRS

# What is `HeaderWriterFilter`?

> [!abstract] Short answer
> An **`OncePerRequestFilter`** (since **3.2**) that runs a list of **`HeaderWriter`s** on the **response**. Default `http.headers(...)` (on with `@EnableWebSecurity`) writes cache-control, **`X-Content-Type-Options: nosniff`**, **HSTS** (HTTPS only), **`X-Frame-Options`**, and **`X-XSS-Protection`**. Architecture TRACE: **`(4/15)`** after `SecurityContextHolderFilter`, before [[What is CsrfFilter in Spring Security]] (and [[What is CorsFilter in Spring Security]] when CORS is on). It does **not** authorize.

## Early exploit headers, not authorization

```d2
direction: down
ctx: "SecurityContextHolderFilter" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
hw: "HeaderWriterFilter\nHeaderWriter list" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
csrf: "CorsFilter? → CsrfFilter" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}

ctx -> hw
hw -> csrf
```

**Fig. 1.** Dump “~200” is **wrong** — `FilterOrderRegistration` places this **after** context filters (order **900**), TRACE **`Invoking HeaderWriterFilter (4/15)`**. HSTS TRACE: *Not injecting HSTS header since it did not match request to [Is Secure]*. See [[What is FilterOrderRegistration]].

`http.headers(Customizer.withDefaults())` equals `contentTypeOptions` + `xssProtection` + `cacheControl` + `httpStrictTransportSecurity` + `frameOptions`. **CSP is opt-in**. `headers.disable()` removes the filter’s writers. Static files: Spring MVC can **override** cache headers; or `cacheControl.disable()`.

```java
http.headers((headers) -> headers
        .frameOptions((fo) -> fo.sameOrigin())); // keep other defaults

http.headers((headers) -> headers.disable()); // no security headers from this filter
```

**Listing 1.** Servlet headers chapter. `permitAll` **still runs** this filter. `web.ignoring()` does **not**. See [[How do you ignore static resources in Spring Security]] and [[What does an empty Security filter chain debug log mean]].

> [!warning] Ignoring skips headers
> Empty / `security="none"` chains never hit `HeaderWriterFilter` — CSS/JS get **no** `X-Content-Type-Options` / frame options. That is why SS6 prefers `permitAll` for static paths. Default **cache-control** is also **no-store**; cache assets by overriding the header or disabling cache-control, not by ignoring the chain unless you accept zero Security headers.

> [!tip] Interview answer
> HeaderWriterFilter writes the default security response headers: nosniff, HSTS on HTTPS, frame options, cache-control, XSS-Protection. It sits early, after the security context is loaded, before CSRF. permitAll still gets those headers; web.ignoring() does not. Customize with http.headers, or disable the whole set with headers.disable().
