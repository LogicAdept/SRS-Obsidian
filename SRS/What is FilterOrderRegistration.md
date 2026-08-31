<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `FilterOrderRegistration`?

> [!abstract] Short answer
> Spring Security’s **internal order table** (`final`, package-private, since **3.2**) that maps known `Filter` **classes** to integers: start **`100`**, step **`100`**. `HttpSecurity.addFilterAfter` / `Before` / `At` / `addFilter` look this map up so a custom filter sits next to `CsrfFilter` or `UsernamePasswordAuthenticationFilter` **inside** `FilterChainProxy`, not at a servlet-container `web.xml` order. Unknown landmark → **`IllegalArgumentException`**: `does not have a registered order`.

## Map of class → slot, then sort

```d2
direction: down
map: "FilterOrderRegistration\nDisableEncodeUrlFilter=100\nCsrfFilter=1100\n… SwitchUserFilter last" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
http: "HttpSecurity\naddFilterAfter → order+1" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
sort: "performBuild\nOrderComparator" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}

map -> http
http -> sort
```

**Fig. 1.** Architecture: you usually do not memorize the list; when you must, this class **is** the list. First slot is [[What is DisableEncodeUrlFilter]]; URI authorization is [[What is AuthorizationFilter in Spring Security]] (after the legacy `FilterSecurityInterceptor` slot). See [[What is FilterChainProxy and DelegatingFilterProxy]].

`getOrder` walks **superclasses** (an `X509AuthenticationFilter` can hit `AbstractPreAuthenticatedProcessingFilter`). `put` is **`putIfAbsent`** — a second registration of the same class does **not** move it. Optional modules (OAuth2, SAML, CAS, Bearer) are keyed by **class name String** so they need not be on the classpath.

```java
http.addFilterAfter(new TenantFilter(), AnonymousAuthenticationFilter.class);
// TenantFilter order = registered(Anonymous) + 1; then filterOrders.put(TenantFilter.class, that order)
```

**Listing 1.** Architecture tenant example. `addFilterBefore` is **−1**; `addFilterAt` is **0** (same slot, **not** a replace). `addFilter(new MyFilter())` works only if `MyFilter` (or a superclass) is **already** in the table. See [[What is addFilterAfter in Spring Security]] and [[How do you implement a custom security filter in Spring Security]].

> [!warning] Not the servlet Filter chain
> Tomcat / `web.xml` / `FilterRegistrationBean` order is a **different** list. Security filters run **inside** one `DelegatingFilterProxy` (`springSecurityFilterChain`). A Boot `@Component` `Filter` can run **twice** unless you `setEnabled(false)` on its registration. `addFilterAt` does **not** remove `CsrfFilter`.

> [!tip] Interview answer
> FilterOrderRegistration is the integer map HttpSecurity uses to place filters: 100, 200, 300, and so on, DisableEncodeUrlFilter first. addFilterAfter is plus one from a known class. If the class is not in that map, build throws. It is not web.xml filter order — everything still sits inside FilterChainProxy.
