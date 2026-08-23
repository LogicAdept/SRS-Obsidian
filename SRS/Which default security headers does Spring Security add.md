<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/AppSec #SRS

# Which default security headers does Spring Security add?

> [!abstract] Short answer
> With defaults enabled, Spring Security writes this response-header set: **Cache-Control** / **Pragma** / **Expires** (no caching), **X-Content-Type-Options: nosniff**, **Strict-Transport-Security** (HSTS), **X-Frame-Options: DENY**, and **X-XSS-Protection: 0**. Customize or replace them via **`http.headers(...)`** on the `SecurityFilterChain`.

## The default set (official list)

| Header | Default value | Purpose |
|---|---|---|
| **Cache-Control** | `no-cache, no-store, max-age=0, must-revalidate` | Stop caching of authenticated / sensitive pages |
| **Pragma** | `no-cache` | HTTP/1.0 cache compatibility |
| **Expires** | `0` | Immediate expiry |
| **X-Content-Type-Options** | `nosniff` | Block MIME sniffing |
| **Strict-Transport-Security** | `max-age=31536000 ; includeSubDomains` | Force HTTPS for ~1 year (HSTS) |
| **X-Frame-Options** | `DENY` | Block clickjacking via iframes |
| **X-XSS-Protection** | `0` | Explicitly **disable** the legacy XSS auditor |

`HeaderWriterFilter` applies these writers early in the filter chain — [[What is HeaderWriterFilter]].

## Customize on the filter chain

Keep defaults but change one policy (e.g. allow same-origin frames):

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.headers(headers -> headers
            .frameOptions(frame -> frame.sameOrigin()));
    return http.build();
}
```

**Listing 1.** Override only `X-Frame-Options` to `SAMEORIGIN`; other defaults stay.

To drop the whole default suite and opt in selectively:

```java
http.headers(headers -> headers
        .defaultsDisabled()
        .cacheControl(withDefaults()));
```

**Listing 2.** `defaultsDisabled()` clears the suite; then enable only what you want.

```d2
direction: right
chain: "SecurityFilterChain" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
hwf: "HeaderWriterFilter" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
resp: "HTTP response\ndefault headers" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}

chain -> hwf -> resp
```

**Fig. 1.** Default header writers run as part of the security filter chain unless `web.ignoring()` removes that path entirely.

> [!warning] X-XSS-Protection is not “on”
> Modern Spring Security defaults send **`X-XSS-Protection: 0`** (filter **off**). Older dumps that list it as an active XSS shield are outdated. Prefer CSP when you need XSS hardening beyond escaping — [[How does Spring Security mitigate XSS CSRF and clickjacking]].

> [!warning] DENY vs real iframes
> **`X-Frame-Options: DENY`** blocks **all** framing. Legitimate same-app embeds need **`sameOrigin()`** (or CSP `frame-ancestors`).

> [!tip] Interview answer
> Defaults: no-cache trio (Cache-Control, Pragma, Expires), nosniff, HSTS with includeSubDomains, X-Frame-Options DENY, and X-XSS-Protection 0. Tune with http.headers(); use defaultsDisabled() when you want an explicit subset.
