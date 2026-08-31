<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #SRS

# What is CookieCsrfTokenRepository?

> [!abstract] Short answer
> **`CookieCsrfTokenRepository`** is a **`CsrfTokenRepository`** (since **4.1**) that stores the **expected** CSRF token in cookie **`XSRF-TOKEN`** and expects the **actual** token on header **`X-XSRF-TOKEN`** (or parameter **`_csrf`**) — Angular's double-submit convention. The **default** store is still **`HttpSessionCsrfTokenRepository`**. Use **`withHttpOnlyFalse()`** only when JavaScript must **read** the cookie; the no-arg constructor keeps **`HttpOnly=true`**.

## What it stores versus what the filter checks

`CsrfTokenRepository` is the persistence SPI: `generateToken`, `saveToken` (null means **delete**), `loadToken`. `CsrfConfigurer` defaults that SPI to **`HttpSessionCsrfTokenRepository`**. The cookie implementation exists so a JavaScript app can **see** the expected token without a server-rendered page. See [[What is CsrfToken]] and [[What is CsrfFilter in Spring Security]].

The cookie is **not** the CSRF check. Browsers attach cookies automatically, so a value that lives **only** in a cookie is forgeable. The client must **copy** `XSRF-TOKEN` into **`X-XSRF-TOKEN`** (or `_csrf`). `CsrfFilter` compares that header/parameter to the loaded cookie. See [[How do you handle CSRF tokens in AJAX requests in Spring Security]].

```d2
direction: right
repo: "CsrfTokenRepository" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
session: "HttpSessionCsrfTokenRepository\n(default)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
cookie: "CookieCsrfTokenRepository\ncookie XSRF-TOKEN" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
header: "Actual token\nX-XSRF-TOKEN" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}

repo -> session
repo -> cookie
cookie -> header: "JS copies"
```

**Fig. 1.** Session is the default store. The cookie repository only holds the **expected** token; the SPA still sends a header.

## Defaults (Spring Security 7.1)

| Piece | Default |
|---|---|
| Cookie name | `XSRF-TOKEN` |
| Header name | `X-XSRF-TOKEN` |
| Parameter name | `_csrf` |
| `HttpOnly` | **`true`** (`new CookieCsrfTokenRepository()`) |
| Path | request context path, or `/` if empty |
| `Secure` | `request.isSecure()` unless overridden |
| Max-Age | `-1` (session cookie); **`saveToken(null)`** writes empty value and **maxAge 0** (delete) |
| Token value | `UUID.randomUUID()` via `generateToken` |

`withHttpOnlyFalse()` is a factory that sets `cookieHttpOnly = false` so `document.cookie` (and Angular) can read `XSRF-TOKEN`. `setCookieCustomizer` (since **6.1**) can adjust the `ResponseCookie` before it is written. Names are overridable (`setCookieName` / `setHeaderName` / `setParameterName`).

```java
http.csrf(csrf -> csrf
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()));
```

**Listing 1.** Conceptual — SPA that reads the cookie. If JavaScript never needs it, use `new CookieCsrfTokenRepository()` so the cookie stays `HttpOnly`.

From Spring Security **7.0**, `csrf.spa()` does that factory **and** installs a request handler that resolves a **plain** header value (the cookie is not XOR/BREACH-encoded; form `_csrf` still is):

```java
http.csrf(csrf -> csrf.spa());
```

**Listing 2.** Conceptual — `spa()` is `CookieCsrfTokenRepository.withHttpOnlyFalse()` plus `SpaCsrfTokenRequestHandler`. On 6.x you configure those two pieces yourself.

> [!warning] HttpOnly false is for JavaScript, not “more CSRF”
> Official guidance: set `HttpOnly` false **only** so a JS framework can read the cookie; if you do not need that, **keep** the default constructor **to improve security**. A non-`HttpOnly` `XSRF-TOKEN` is readable by **any script on the origin** (`document.cookie`). Prefer meta tags or a `/csrf` endpoint when the page is server-rendered.

> [!warning] Client-writable cookie is why session is preferred
> `CsrfFilter` documents session storage as **preferred** because a cookie **can be modified by the client**. Cookie persistence is a JS integration choice, not a stronger token. Never treat “the cookie was sent” as passing CSRF — the **header or parameter** is the actual token.

> [!tip] Interview answer
> CookieCsrfTokenRepository puts the expected CSRF token in an XSRF-TOKEN cookie and expects X-XSRF-TOKEN, Angular's convention. The default store is still the HTTP session. Use withHttpOnlyFalse or csrf.spa() only when JavaScript must read the cookie; keep HttpOnly otherwise, and always copy the value into a header on state-changing requests.
