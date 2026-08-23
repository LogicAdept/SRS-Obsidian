<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# Why must a JWT filter run before AnonymousAuthenticationFilter?

> [!abstract] Short answer
> **`AnonymousAuthenticationFilter` is the last authentication filter.** It installs an **`AnonymousAuthenticationToken`** whenever **`SecurityContextHolder` has no `Authentication`**. A JWT / Bearer filter placed **after** it leaves **anonymous** in the context, so the bearer token is **never applied** and **`AuthorizationFilter`** sees **`ROLE_ANONYMOUS`** instead of the JWT principal.

## Filter-chain order

Spring Security runs authentication filters **before** authorization. Built-in order (from **`HttpSecurity` filter registration**) includes **`BearerTokenAuthenticationFilter`** among authentication filters and places **`AnonymousAuthenticationFilter` afterward** — anonymous is explicitly **“chained after the normal authentication mechanisms.”**

The architecture guide calls **`AnonymousAuthenticationFilter` the last authentication filter** in the chain. Custom **authentication** filters belong **after `LogoutFilter`** (exploit protection and logout have already run) and **before anonymous**.

```d2
direction: right
logout: "LogoutFilter" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}
jwt: "JWT / Bearer\nauth filter" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
anon: "AnonymousAuthenticationFilter\n(if no Authentication)" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
authz: "AuthorizationFilter" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}

logout -> jwt -> anon -> authz
```

**Fig. 1.** Bearer/JWT authentication must run while the context is still unset; anonymous fills the gap only after real auth filters finish.

## What goes wrong when order is reversed

**`AnonymousAuthenticationFilter`** checks whether an **`Authentication`** already exists; if not, it creates **`anonymousUser` / `ROLE_ANONYMOUS`**.

If your JWT filter runs **after** that:

1. Anonymous is already in **`SecurityContextHolder`**
2. The JWT filter may **skip** (context non-empty) or fail to **replace** anonymous with the decoded JWT **`Authentication`**
3. **`AuthorizationFilter`** evaluates rules against **anonymous**, so a valid **`Authorization: Bearer`** header still yields **401 / 403**

With **`oauth2ResourceServer().jwt()`**, Spring registers **`BearerTokenAuthenticationFilter`** in the correct slot automatically. Custom **`OncePerRequestFilter`** JWT parsers must be inserted explicitly — typically **`addFilterBefore(filter, AnonymousAuthenticationFilter.class)`** or among authentication filters after **`LogoutFilter`**.

```java
http.oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
// registers BearerTokenAuthenticationFilter before AnonymousAuthenticationFilter

// custom filter equivalent:
http.addFilterBefore(jwtAuthFilter, AnonymousAuthenticationFilter.class);
```

**Listing 1.** Conceptual placement — authentication before anonymous, not after.

> [!warning] Symptom looks like a bad token
> Mis-ordered filters produce **silent anonymous auth** with a valid Bearer header — easy to misdiagnose as signature or issuer problems. Log **`SecurityContextHolder.getContext().getAuthentication()`** after the JWT filter runs. See [[What is AnonymousAuthenticationToken]] and [[What is SecurityFilterChain]].

> [!tip] Interview answer
> AnonymousAuthenticationFilter runs last among auth filters and only runs when no Authentication exists. A JWT filter after it leaves anonymous in the context, so the token is ignored and authorization fails. Place JWT/Bearer authentication before AnonymousAuthenticationFilter — oauth2ResourceServer().jwt() does this for you.
