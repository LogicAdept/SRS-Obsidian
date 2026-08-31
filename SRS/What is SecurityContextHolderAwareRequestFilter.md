<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `SecurityContextHolderAwareRequestFilter`?

> [!abstract] Short answer
> A **`GenericFilterBean`** that wraps `HttpServletRequest` with **`SecurityContextHolderAwareRequestWrapper`** so **servlet API** methods read Spring’s **`Authentication`**: `getRemoteUser()`, `getUserPrincipal()`, `isUserInRole(String)`. On with `@EnableWebSecurity` (`http.servletApi`); XML **`servlet-api-provision`** defaults **`true`**. Default TRACE: after [[What is RequestCacheAwareFilter]], before [[What is AnonymousAuthenticationFilter]]. Dump “~1200” is **wrong** (`FilterOrderRegistration` **3400**).

## Wrap the request, not the context store

```d2
direction: down
f: "SecurityContextHolderAwareRequestFilter" {
  width: 320
  height: 40
  style.fill: "#e3f2fd"
}
w: "SecurityContextHolderAwareRequestWrapper" {
  width: 320
  height: 40
  style.fill: "#e8f5e9"
}
api: "getRemoteUser / isUserInRole\nServlet 3 login logout authenticate" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}

f -> w
w -> api
```

**Fig. 1.** Javadoc: wrapper implements the servlet security methods from `SecurityContextHolder`. `HttpServletRequest.login` / `logout` / `authenticate` and `AsyncContext.start` (copy `SecurityContext` to the async thread) are extra Servlet 3 hooks. See [[What is FilterOrderRegistration]] and [[What is HttpSecurity in Spring Security]].

`isUserInRole` is an **exact** `GrantedAuthority` match. Default **`rolePrefix` is `ROLE_`** (same idea as `hasRole`): `request.isUserInRole("ADMIN")` looks for **`ROLE_ADMIN`**. Pass `null`/empty prefix only if you turned that off. `getUserPrincipal()` is the **`Authentication`**. See [[How do you restrict URL access by role in Spring Security]].

```java
http.servletApi((servletApi) -> servletApi.disable());
```

**Listing 1.** `HttpSecurity.servletApi` is auto-applied. Disable if you must use the **container** principal instead. JSP/`HttpServletRequest` in MVC still sees Security’s user **after** authentication filters (including anonymous) have run — the wrapper reads the **current** `SecurityContext` when the method is called.

> [!warning] Prefix and not HolderFilter
> This is **not** `SecurityContextHolderFilter` (load/save context). `isUserInRole("ROLE_ADMIN")` with a `ROLE_` prefix looks for **`ROLE_ROLE_ADMIN`**. Servlet `login`/`logout` no-ops unless you wired `AuthenticationManager` / `LogoutHandler`s (defaults keep **container** behavior).

> [!tip] Interview answer
> SecurityContextHolderAwareRequestFilter wraps the request so getRemoteUser and isUserInRole use Spring Security’s Authentication. isUserInRole("ADMIN") means ROLE_ADMIN, like hasRole. It is on by default as servletApi. It does not load the SecurityContext — it only exposes it through the servlet API.
