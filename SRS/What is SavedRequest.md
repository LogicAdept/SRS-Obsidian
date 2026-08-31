<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/SessionManagement #Java/Spring/Security/CSRF #SRS

# What is SavedRequest?

> [!abstract] Short answer
> **`SavedRequest`** (**since 3.0**) is the **serializable snapshot** of the **protected request** that triggered login: **redirect URL**, **HTTP method**, **query/form parameters**, **headers**, **cookies**, **locales**. **`RequestCache`** stores it (default: **`HttpSessionRequestCache`** as **`DefaultSavedRequest`**). After success, **`SavedRequestAwareAuthenticationSuccessHandler`** **redirects** to **`getRedirectUrl()`** (includes the **`continue`** query param in **7.1**). **`RequestCacheAwareFilter`** then wraps the current request so it **looks like** the original. It is **not** a raw body dump — **`getParameterMap()`** is form/query data. **`NullRequestCache`** means there is **no** `SavedRequest`.

## Snapshot for redirect, then a wrapper

Javadoc: used so an authentication mechanism can **redirect to the original URL** and so **`RequestCache`** can **reproduce** the request. **`ExceptionTranslationFilter`** creates **`DefaultSavedRequest`** at the **`AuthenticationException`**. **`SavedRequestAwareWrapper`** rebuilds it after login ([[What is RequestCache in Spring Security]], [[What is ExceptionTranslationFilter in Spring Security]], [[How does form login work internally in Spring Security]], [[What is AuthenticationSuccessHandler in Spring Security]]).

**`getRedirectUrl()`** is the full URL the browser should **GET** next. **`DefaultSavedRequest`** appends **`matchingRequestParameterName`** (default **`continue`**) so the filter will **`getMatchingRequest`**. **`If-Modified-Since` / `If-None-Match` are omitted** (**SEC-1412**, **SEC-1624**). **`SimpleSavedRequest`** is a thinner implementation (cookie cache).

Without a snapshot, success lands on **`/`** (or **`defaultSuccessUrl`**). A custom success handler that always **`/dashboard`** **throws this object away** ([[What is loginPage in form login]]).

```java
SavedRequest saved = requestCache.getRequest(request, response);
if (saved != null) {
	String url = saved.getRedirectUrl(); // original URL + continue
	String method = saved.getMethod();
}
```

**Listing 1.** Success handler reads **`getRedirectUrl()`**. The filter uses **method + parameters + headers**, then **removes** the cache.

```java
http.requestCache((cache) -> cache.requestCache(new NullRequestCache()));
```

**Listing 2.** No **`SavedRequest`** — correct for **STATELESS** APIs and when you always send users **home** ([[How do you implement custom token-based authentication in Spring Security]]).

```d2
direction: down
hit: "GET/POST /checkout\nunauthenticated" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
snap: "DefaultSavedRequest\nin HttpSession" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
back: "302 getRedirectUrl\nthen RequestCacheAwareFilter" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

hit -> snap -> back
```

**Fig. 1.** The object is the **memory** of `/checkout`. Login is a **detour**.

> [!warning] POST + CSRF
> A saved **form POST** still has the **old `_csrf`** in **`getParameterMap()`**. After login (often a **new session**), **`CsrfFilter`** expects the **new** token — replay can **403**. Prefer saving **GETs**, or complete checkout **after** login with a **fresh** POST. JSON bodies are **not** in the parameter map.

> [!warning] Not for token APIs
> **`HttpSessionRequestCache`** **creates a session** to hold this object. **Bearer / STATELESS** chains should not. **`continue`** must be on the post-login URL or **`RequestCacheAwareFilter`** will **not** unwrap.

> [!tip] Interview answer
> SavedRequest is the cached original request: URL, method, and form parameters, held by RequestCache in the session. After form login, Spring redirects to getRedirectUrl() so the user returns to /checkout instead of /. RequestCacheAwareFilter then wraps the request to replay method and params. I use NullRequestCache on APIs, and I do not expect a saved POST with an old CSRF token to succeed.
