<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# Why does addFilterBefore target filter choice matter?

> [!abstract] Short answer
> **`addFilterBefore(yourFilter, Landmark.class)` only positions your filter relative to that landmark class** in the **Spring Security** chain — not relative to servlet-container filters. Pick the **wrong landmark** and your filter runs in the **wrong phase**: before **`SecurityContextHolder`** is ready, **after** form-login filters consumed the body, or **after** **`AnonymousAuthenticationFilter`** already set anonymous auth.

## Relative placement, not absolute order

`HttpSecurity.addFilterBefore(Filter, Class<?>)` inserts **`yourFilter` immediately before the first filter instance of the given class** inside the **`SecurityFilterChain`**. It does **not** assign a servlet `@Order` or replace the landmark — the landmark still runs right after yours.

Spring Security registers dozens of built-in filters at fixed **`FilterOrderRegistration`** slots. Custom filters are almost always anchored to a **well-known neighbor** because memorizing every slot number is impractical.

```java
// common JWT / bearer anchor — early in the auth block
http.addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);

// authorization-style check — after authentication completes
http.addFilterAfter(tenantFilter, AnonymousAuthenticationFilter.class);
```

**Listing 1.** The landmark class is the coordinate system; changing it moves your filter to a different chain segment.

## Default chain landmarks (simplified)

At startup, **`DefaultSecurityFilterChain`** logs the resolved filter list (DEBUG). Per-request, **`FilterChainProxy`** at TRACE logs each invocation — the architecture guide recommends both when debugging placement.

Typical servlet chain segment (abbreviated):

```d2
direction: right
ctx: "SecurityContextHolderFilter" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
exploit: "HeaderWriter / Csrf / Logout" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
form: "UsernamePasswordAuthenticationFilter" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
basic: "BasicAuthenticationFilter" {
  width: 200
  height: 50
  style.fill: "#fce4ec"
}
anon: "AnonymousAuthenticationFilter" {
  width: 220
  height: 50
  style.fill: "#ffcdd2"
}
authz: "AuthorizationFilter" {
  width: 180
  height: 50
  style.fill: "#f3e5f5"
}

ctx -> exploit -> form -> basic -> anon -> authz
```

**Fig. 1.** Landmarks sit in different phases; anchoring on the wrong class skips or repeats prerequisite work.

Official placement guidance:

| Filter purpose | Place after | Because … |
|---|---|---|
| Exploit protection | `SecurityContextHolderFilter` | Context loaded from session/repository |
| **Authentication** | `LogoutFilter` | Context + CSRF/CORS/headers applied |
| **Authorization** | `AnonymousAuthenticationFilter` | Auth mechanisms finished |

## Wrong landmark → wrong phase

**Authentication filter before `LogoutFilter`.** CSRF, CORS, and secure-header handling may not have run yet; logout/exploit protection is out of order.

**JWT anchored on `BasicAuthenticationFilter` instead of `UsernamePasswordAuthenticationFilter`.** Your bearer filter runs **after** form-login filters and page generators. Symptoms include **`SecurityContext`** still empty or already **`anonymousUser`**, valid **`Authorization: Bearer`** headers ignored, or request-body readers conflicting with login parsing — even though you called `addFilterBefore`.

**Authentication filter after `AnonymousAuthenticationFilter`.** Anonymous auth fills an empty context first; your token filter never replaces it. See [[Why must a JWT filter run before AnonymousAuthenticationFilter]].

**`securityMatcher` mismatch.** `FilterChainProxy` picks the **first** matching **`SecurityFilterChain`**. If your custom filter lives on a chain whose **`securityMatcher("/api/**")`** does not match the request, **the entire chain — including your filter — is skipped**, regardless of landmark choice. See [[What is securityMatcher in Spring Security]].

> [!warning] Servlet `FilterRegistrationBean` order is a different domain
> Registering a filter as a Spring **`@Component`** also adds it to the **embedded servlet container**, which can invoke it **twice** and in a **different order** than `HttpSecurity`. Disable container registration with **`FilterRegistrationBean.setEnabled(false)`** and add the filter only through **`SecurityFilterChain`**. Container `@Order` does **not** reorder filters inside **`FilterChainProxy`**. See [[What is the difference between addFilterBefore addFilterAfter and addFilterAt]] and [[What is FilterOrderRegistration]].

> [!tip] Interview answer
> addFilterBefore positions your filter relative to a landmark class inside the SecurityFilterChain. Wrong landmark means wrong phase — context not loaded, CSRF not applied, or anonymous auth already set. Use UsernamePasswordAuthenticationFilter or AnonymousAuthenticationFilter as common auth anchors, log FilterChainProxy at TRACE to verify, and remember securityMatcher decides whether the chain runs at all.
