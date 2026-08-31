<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #SRS

# How do you handle CSRF tokens in AJAX requests in Spring Security?

> [!abstract] Short answer
> **Put the CSRF token in an HTTP header** the browser will **not** attach by itself. JSON bodies are **not** form parameters, so a `_csrf` field inside JSON is ignored. For a **multi-page** app, render `CsrfToken` into `_csrf` / `_csrf_header` meta tags and copy them onto every AJAX call (`X-CSRF-TOKEN` by default). For an **SPA**, persist the expected token in a cookie (`CookieCsrfTokenRepository` / `csrf.spa()` from Spring Security **7.0**) and send **`X-XSRF-TOKEN`**. A missing token on POST/PUT/PATCH/DELETE is **403**, not 401.

## Why AJAX cannot use a hidden form field

`CsrfFilter` is on by default for **unsafe** methods. The default matcher **ignores GET, HEAD, TRACE, and OPTIONS** and validates every other request. The actual token must live in a **header or request parameter** — never in a cookie alone, because cookies are auto-sent.

A `Content-Type: application/json` body is not parsed as `application/x-www-form-urlencoded`, so `_csrf` inside JSON never reaches the resolver. The request handler looks for a header (**`X-CSRF-TOKEN` or `X-XSRF-TOKEN`** by default) or the **`_csrf`** parameter. See [[What is CsrfToken]] and [[What is CsrfFilter in Spring Security]].

```d2
direction: right
ajax: "AJAX POST / PUT /\nPATCH / DELETE" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
header: "Header\nX-CSRF-TOKEN or\nX-XSRF-TOKEN" {
  width: 180
  height: 80
  style.fill: "#fff3e0"
}
filter: "CsrfFilter" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
ok: "Filter chain\ncontinues" {
  width: 140
  height: 60
  style.fill: "#e8f5e9"
}
deny: "AccessDeniedHandler\n403 Forbidden" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}

ajax -> header
header -> filter
filter -> ok: "matches"
filter -> deny: "missing / invalid"
```

**Fig. 1.** AJAX must copy the token into a header; `CsrfFilter` then compares it to the persisted `CsrfToken` and fails closed with `AccessDeniedException`.

## Multi-page apps: meta tags plus `ajaxSend`

`CsrfToken` is a request attribute named **`_csrf`**. Expose `token` and `headerName` in meta tags from JSP or any other view that can read that attribute:

```html
<meta name="_csrf" content="${_csrf.token}"/>
<meta name="_csrf_header" content="${_csrf.headerName}"/>
```

**Listing 1.** Default session header name is **`X-CSRF-TOKEN`**. The meta names `_csrf` / `_csrf_header` are **not** the HTTP header names.

jQuery (or equivalent) reads those tags and sets the header on every AJAX send:

```javascript
$(function () {
	var token = $("meta[name='_csrf']").attr("content");
	var header = $("meta[name='_csrf_header']").attr("content");
	$(document).ajaxSend(function(e, xhr, options) {
		xhr.setRequestHeader(header, token);
	});
});
```

**Listing 2.** Copy meta values onto `XMLHttpRequest`. Extra CSRF headers on GET are harmless; GET is not CSRF-checked by default.

## SPAs: cookie plus `X-XSRF-TOKEN`

`CookieCsrfTokenRepository` writes cookie **`XSRF-TOKEN`** and expects header **`X-XSRF-TOKEN`** (Angular convention). JavaScript can read that cookie **only** if it is not `HttpOnly`. See [[What is CookieCsrfTokenRepository]].

```java
http.csrf(csrf -> csrf
    .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse()));
```

**Listing 3.** Conceptual — `withHttpOnlyFalse()` is required when the SPA reads the cookie itself. Prefer `new CookieCsrfTokenRepository()` if JavaScript never needs the cookie.

From Spring Security **7.0**, `csrf.spa()` is the bundled SPA setup: cookie repository **plus** a request handler that resolves the **plain** cookie value (JS never sees the XOR/BREACH-encoded form token):

```java
http.csrf(csrf -> csrf.spa());
```

**Listing 4.** Conceptual — Spring Security 7.0+. On 6.x, you still need `withHttpOnlyFalse()` **and** a custom `CsrfTokenRequestHandler` that uses the plain resolver when the `X-XSRF-TOKEN` header is present.

Angular can copy `XSRF-TOKEN` into `X-XSRF-TOKEN` automatically once the cookie is readable. Other SPAs must do that copy themselves.

A third official option is a `@ControllerAdvice` (or a `GET /csrf` endpoint) that writes `csrfToken.getHeaderName()` / `getToken()` on the **response**; the next AJAX call sends the same name as a **request** header.

> [!warning] HttpOnly cookie is invisible to JavaScript
> `Cookie.isHttpOnly() == true` (the safer default of `new CookieCsrfTokenRepository()`) **blocks** `document.cookie`. An SPA that must read `XSRF-TOKEN` needs `withHttpOnlyFalse()` or `csrf.spa()`. The cookie still only stores the **expected** token; the **actual** token must go in **`X-XSRF-TOKEN`**. Sending the cookie alone is not CSRF proof.

> [!warning] Missing AJAX CSRF header is 403, not 401
> Invalid or absent token → `InvalidCsrfTokenException` (`AccessDeniedException`) → default `AccessDeniedHandlerImpl` sends **403 Forbidden**. That is not `AuthenticationEntryPoint` (**401**). Authenticated JSON POSTs fail CSRF **before** the controller if the header is omitted. Do not treat this as a login or JWT failure; keep CSRF on cookie-session apps, and see [[Why do you disable CSRF for a JWT REST API]] only for header-only Bearer APIs.

> [!warning] Safe methods must stay read-only
> CSRF is skipped for **GET, HEAD, TRACE, OPTIONS**. A state-changing GET is forgeable with a cross-site navigation and **no** token check. PUT/PATCH/DELETE are protected like POST. Do not “fix” AJAX 403s by moving mutations onto GET.

> [!tip] Interview answer
> JSON AJAX cannot put `_csrf` in the body; send the token as a header. Server-rendered pages expose `CsrfToken` in meta tags and jQuery `ajaxSend` copies `X-CSRF-TOKEN`. SPAs use a readable `XSRF-TOKEN` cookie and `X-XSRF-TOKEN`, which is `withHttpOnlyFalse()` or `csrf.spa()` on Security 7. A missing header on POST is 403 from `CsrfFilter`, not 401.
