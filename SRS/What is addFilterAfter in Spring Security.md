<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `addFilterAfter` in Spring Security?

> [!abstract] Short answer
> **`http.addFilterAfter(filter, SomeFilter.class)`** puts your `Filter` in this `SecurityFilterChain` **one slot after** a **known** Spring Security filter type. “Known” means it has a **registered order** (`FilterOrderRegistration`: `UsernamePasswordAuthenticationFilter`, `BasicAuthenticationFilter`, `AnonymousAuthenticationFilter`, …) **or** you already added it with `addFilterBefore` / `addFilterAfter`. It does **not** mean that landmark must be enabled on this chain.

## After a landmark, not “somewhere later”

```d2
direction: right
anon: "AnonymousAuthenticationFilter" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
you: "your Filter\norder + 1" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}
etf: "ExceptionTranslationFilter …" {
  width: 240
  height: 40
  style.fill: "#eceff1"
}

anon -> you
you -> etf
```

**Fig. 1.** Architecture rule of thumb: authorization-style work **after** `AnonymousAuthenticationFilter` (last authentication filter). Custom **authentication** is usually **`addFilterBefore(..., LogoutFilter.class)`** so logout still runs first.

```java
@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http
        .authorizeHttpRequests((a) -> a.anyRequest().authenticated())
        .addFilterAfter(new TenantFilter(), AnonymousAuthenticationFilter.class);
    return http.build();
}
```

**Listing 1.** Documented tenant example: after authentication filters, before `ExceptionTranslationFilter` can translate `AccessDeniedException`. `addFilterBefore` is the same API with offset **−1** (JWT dumps often use `UsernamePasswordAuthenticationFilter.class`). `addFilter(Filter)` only accepts a **Security** filter type that already has an order — custom types must use before/after. See [[How do you implement a custom security filter in Spring Security]].

If the landmark class has **no** registered order: **`IllegalArgumentException`**: `The Filter class … does not have a registered order`. A random `OncePerRequestFilter` subclass is not a landmark until you add it relative to a known type. `UsernamePasswordAuthenticationFilter` stays in the order table even if you never called `formLogin()`.

`addFilterAt` uses offset **0**. Multiple filters at the **same** order are **not deterministic**; it does **not** remove the original filter. Architecture’s “replaces” wording is the wrong mental model — disable the DSL (`httpBasic((b) -> b.disable())`) if you do not want `BasicAuthenticationFilter`.

If the `Filter` is a Boot `@Component`, the container may run it **and** the chain. `FilterRegistrationBean.setEnabled(false)` so only `HttpSecurity` adds it. TRACE `Invoking … (n/m)` shows the real position. See [[How do you enable Spring Security debug logging for the filter chain]].

> [!warning] Landmark must be known, not necessarily present
> `addFilterAfter(new F(), MyFilter.class)` fails at **`http.build()`** if `MyFilter` was never given an order. It does **not** fail merely because `httpBasic` is off and `BasicAuthenticationFilter` is absent from the built list. Wrong landmark still compiles — you just run in the wrong phase (before `SecurityContext` is loaded, after `AuthorizationFilter`, and so on).

> [!tip] Interview answer
> addFilterAfter places your filter one order after a known Spring Security filter class. The class must be in FilterOrderRegistration or already added with before/after, or build throws. addFilterAt is the same slot and does not replace; use before LogoutFilter for custom authentication and after AnonymousAuthenticationFilter when you need the user already set.
