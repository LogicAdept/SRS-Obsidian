<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/SessionManagement #SRS

# What is RequestCache in Spring Security?

> [!abstract] Short answer
> **`RequestCache`** (**since 3.0**) saves the **protected request** you hit **before** login so it can be **replayed after** success. **`ExceptionTranslationFilter`** calls **`saveRequest`** then the **entry point**. After form login, **`SavedRequestAwareAuthenticationSuccessHandler`** redirects to that **`SavedRequest`**. **`RequestCacheAwareFilter`** then **`getMatchingRequest`** and wraps the current call so method, query, and body match. Default store: **`HttpSessionRequestCache`** (`SPRING_SECURITY_SAVED_REQUEST`). **`NullRequestCache`** stores nothing — use it for **Basic**, **Digest**, and **STATELESS** APIs so you do **not** create a session just to remember a URL.

## Save on 401-path, replay after authenticate

Interface: **`saveRequest`**, **`getRequest`** (leave cached), **`getMatchingRequest`** (wrapper + **remove**), **`removeRequest`**. Default **`HttpSessionRequestCache`** uses **`DefaultSavedRequest`**. **`createSessionAllowed`** defaults **true**; set **false** when the client will **retry the same URL** (Basic/Digest). **`CookieRequestCache`** is the session-less cookie variant.

**`getMatchingRequest`** (default **since 6**) only consults the session if the query contains **`continue`**. **`DefaultSavedRequest`** puts that parameter on the post-login redirect so the filter knows to unwrap. Architecture sample: **`setMatchingRequestParameterName("continue")`** is already the **7.1 default**.

Without a saved request, success goes to **`/`** (or **`defaultSuccessUrl`**). **`formLogin.successHandler(...)`** that ignores **`SavedRequest`** drops “return to the page I wanted” ([[What is AuthenticationSuccessHandler in Spring Security]], [[How does form login work internally in Spring Security]], [[What is ExceptionTranslationFilter in Spring Security]], [[What is AuthenticationEntryPoint]], [[What is loginPage in form login]], [[What is SavedRequest]]).

```java
http.requestCache((cache) -> cache.requestCache(new NullRequestCache()));
```

**Listing 1.** Official “do not save.” Pair with **STATELESS** token APIs or when you always send users **home** ([[How do you implement custom token-based authentication in Spring Security]], [[How do you configure HTTP Basic authentication in Spring Security]]).

```java
HttpSessionRequestCache cache = new HttpSessionRequestCache();
cache.setMatchingRequestParameterName("continue"); // default in 7.1
http.requestCache((c) -> c.requestCache(cache));
```

**Listing 2.** Session cache. **`setCreateSessionAllowed(false)`** avoids a session on Basic/Digest challenges.

```d2
direction: down
etf: "ExceptionTranslationFilter\nsaveRequest" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
login: "form login success\nredirect to SavedRequest" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
replay: "RequestCacheAwareFilter\ngetMatchingRequest" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

etf -> login -> replay
```

**Fig. 1.** Cache is **not** the login form. It is the **original** resource.

> [!warning] Sessions and APIs
> **`HttpSessionRequestCache`** **creates a session** by default (`createSessionAllowed`). That fights **`SessionCreationPolicy.STATELESS`**. Use **`NullRequestCache`**. HTTP Basic already expects the client to **repeat the request** with **`Authorization`** — saving a form POST in the session is the wrong model.

> [!warning] `continue` and custom success handlers
> **`RequestCacheAwareFilter`** ignores the session unless **`continue`** is on the URL. A success handler that **302s to `/dashboard`** never replays a **POST /checkout**. **`getRequest`** (success handler) and **`getMatchingRequest`** (filter) are different methods — removing the cache in one path leaves the other empty.

> [!tip] Interview answer
> RequestCache remembers the request that triggered login so Spring can send the user back there. ExceptionTranslationFilter saves it; after form login the success handler redirects to that SavedRequest; RequestCacheAwareFilter replays it when the continue parameter is present. The default is HttpSessionRequestCache. For Basic or a stateless API I use NullRequestCache so we do not create a session just to store a URL.
