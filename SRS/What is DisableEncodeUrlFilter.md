<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `DisableEncodeUrlFilter`?

> [!abstract] Short answer
> The **first** filter in a default `SecurityFilterChain` (`OncePerRequestFilter`, since **5.7**). It wraps `HttpServletResponse` so **`encodeURL` / `encodeRedirectURL` return the URL unchanged** — the container never appends **`;jsessionid=`**. That stops the session id leaking in **HTTP access logs** (and in any URL the app encodes). It is **not** CSRF. XML: `http@disable-url-rewriting` defaults to **`true`**; **`false`** omits this filter and cookie-less clients can track sessions in the URL.

## First filter, response wrapper

```d2
direction: down
fcp: "FilterChainProxy\nmatched chain" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
deuf: "DisableEncodeUrlFilter (1/N)\nwrap encodeURL → identity" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
rest: "rest of the chain +\nJSP / sendRedirect" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

fcp -> deuf
deuf -> rest
```

**Fig. 1.** Architecture TRACE: `Invoking DisableEncodeUrlFilter (1/15)` before `WebAsyncManagerIntegrationFilter`. `FilterOrderRegistration` puts it **first**. See [[What is FilterChainProxy and DelegatingFilterProxy]] and [[What does an empty Security filter chain debug log mean]].

Servlet containers rewrite URLs when cookies are off (`response.encodeURL("/home")` → `/home;jsessionid=…`). The wrapper’s `encodeURL` / `encodeRedirectURL` just **return `url`**. Downstream filters and views never see the encoding methods of the real response. Incoming `jsessionid` in a request URL is **not** stripped.

XML namespace maps **`DISABLE_ENCODE_URL_FILTER`** → `http@disable-url-rewriting`. Default **`true`**: clients **must use cookies**. Set **`false`** only if you still need URL session tracking.

```xml
<http disable-url-rewriting="false">
    <!-- omits DisableEncodeUrlFilter; jsessionid may appear in encoded URLs -->
</http>
```

**Listing 1.** Namespace: default is `true` (filter present). Java `HttpSecurity` default chains include the same first filter; there is no `csrf.disable()`-style switch on this class.

> [!warning] Not CSRF, not a cookie killer
> This only **blocks `encodeURL` rewriting**. It does **not** replace [[What is CsrfFilter in Spring Security]], and it does **not** delete `JSESSIONID` cookies. `web.ignoring()` / empty chains **skip** it, so ignored static paths can still emit encoded URLs. Turning rewriting **on** (`disable-url-rewriting="false"`) puts the session id in logs and bookmarks.

> [!tip] Interview answer
> DisableEncodeUrlFilter is first in the default chain. It wraps the response so encodeURL never adds jsessionid, because session ids in URLs leak in access logs. It is not CSRF. XML disable-url-rewriting is true by default; false restores container URL rewriting for cookie-less clients.
