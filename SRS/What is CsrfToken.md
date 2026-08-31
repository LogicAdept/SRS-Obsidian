<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #SRS

# What is CsrfToken?

> [!abstract] Short answer
> **`CsrfToken`** is Spring Security's **synchronizer-token** object (since **3.2**): three non-null strings — **`getToken()`**, **`getParameterName()`** (default **`_csrf`**), **`getHeaderName()`**. The concrete type is **`DefaultCsrfToken`** (immutable). `CsrfFilter` compares the **actual** value from a header or parameter to the **expected** value loaded from a **`CsrfTokenRepository`**. Persistence is not the interface: default store is the **HTTP session**; a cookie is optional.

## The three fields

`CsrfToken` is `Serializable`. `DefaultCsrfToken`'s constructor rejects null or empty `headerName`, `parameterName`, or `token`. Repositories fill those fields when they `generateToken`:

| Repository | `getHeaderName()` | `getParameterName()` | Where `getToken()` is stored |
|---|---|---|---|
| `HttpSessionCsrfTokenRepository` (default) | **`X-CSRF-TOKEN`** | `_csrf` | `HttpSession` |
| `CookieCsrfTokenRepository` | **`X-XSRF-TOKEN`** | `_csrf` | cookie `XSRF-TOKEN` |

Both generate a `UUID` string as the raw token. See [[What is CookieCsrfTokenRepository]].

`CsrfTokenRequestHandler` (default **`XorCsrfTokenRequestAttributeHandler`** since Security **6**) exposes the token as request attribute **`_csrf`** (and as `CsrfToken.class.getName()`). Views and `@Controller` methods can read it; `CsrfTokenArgumentResolver` injects it as a method argument.

```d2
direction: right
repo: "CsrfTokenRepository\nexpected token" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
attr: "Request attribute _csrf\nCsrfToken (maybe XOR-masked)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
client: "Header or _csrf param\nactual token" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
filter: "CsrfFilter\ncompare" {
  width: 160
  height: 50
  style.fill: "#fce4ec"
}

repo -> attr: "handle()"
attr -> client: "form / AJAX copies"
client -> filter
repo -> filter: "loadToken()"
```

**Fig. 1.** The same `CsrfToken` idea appears three ways: persisted expected value, request-attribute copy for the page, actual value on the next unsafe request.

## How the client must send it

The actual token must be in a part of the request the **browser does not attach by itself**. Default resolution (header **`X-CSRF-TOKEN` or `X-XSRF-TOKEN`**, or parameter **`_csrf`**) is what `CsrfFilter` checks on every method **other than GET, HEAD, TRACE, OPTIONS**. See [[What is CsrfFilter in Spring Security]] and [[How do you handle CSRF tokens in AJAX requests in Spring Security]].

```html
<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
```

**Listing 1.** Form field from the `_csrf` request attribute. AJAX uses `headerName` instead of a JSON body field.

```java
@GetMapping("/csrf")
public CsrfToken csrf(CsrfToken csrfToken) {
    return csrfToken;
}
```

**Listing 2.** Conceptual — `CsrfTokenArgumentResolver` returns the request-attribute token so a client can copy `getHeaderName()` / `getToken()` onto later POSTs.

> [!warning] `getToken()` on the request is not always the raw cookie/session value
> From **5.8** / Security **6**, `XorCsrfTokenRequestAttributeHandler` **masks** the value on each request (BREACH). `${_csrf.token}` and a returned `CsrfToken` can **change every request** while the repository still holds the raw UUID. The filter **decodes** a header or `_csrf` parameter before comparing. A SPA that reads the **plain cookie** must use `csrf.spa()` (7.0) or a handler that resolves that header with the **plain** decoder — copying the XOR-masked form token is the other valid path.

> [!warning] Header name depends on the repository
> Session default is **`X-CSRF-TOKEN`**. Cookie default is **`X-XSRF-TOKEN`**. Sending the wrong name looks like a missing token (**403**). `HttpOnly` cookies cannot be read by JS; that is a [[What is CookieCsrfTokenRepository]] concern (`withHttpOnlyFalse()` / `csrf.spa()`), not a second `CsrfToken` type.

> [!tip] Interview answer
> CsrfToken is the synchronizer token: token value, parameter name `_csrf`, and header name. DefaultCsrfToken is immutable; the default store is the HTTP session, not the cookie. CsrfFilter checks the header or parameter on unsafe methods. Watch Security 6 XOR masking: the request-attribute token can differ from the persisted raw value.
