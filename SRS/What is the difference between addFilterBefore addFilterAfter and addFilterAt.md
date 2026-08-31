<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is the difference between `addFilterBefore`, `addFilterAfter`, and `addFilterAt`?

> [!abstract] Short answer
> All three register **your** `Filter` relative to a **known** class in [[What is FilterOrderRegistration]] (`HttpSecurity.addFilterAtOffsetOf`). **`addFilterBefore`** → order **−1** (yours runs first). **`addFilterAfter`** → **+1**. **`addFilterAt`** → **0** (same slot). Same-slot order is **not deterministic** and **does not replace** the landmark — disable the DSL (`formLogin.disable()`) if you do not want [[What is UsernamePasswordAuthenticationFilter]]. Unknown landmark → **`IllegalArgumentException`**: `does not have a registered order`.

## Three offsets, one sort

```d2
direction: right
before: "Before\norder − 1" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
at: "At\norder + 0\nboth keep running" {
  width: 180
  height: 55
  style.fill: "#fff3e0"
}
after: "After\norder + 1" {
  width: 140
  height: 40
  style.fill: "#e8f5e9"
}

before -> at -> after
```

**Fig. 1.** `performBuild` sorts `OrderedFilter`s. The landmark class need **not** be present in **this** chain — only in the order table (or already added with before/after). See [[What is addFilterAfter in Spring Security]] and [[How do you implement a custom security filter in Spring Security]].

Architecture rule of thumb: custom **authentication** **after `LogoutFilter`** (`addFilterBefore`/`After` relative to that). JWT dumps often `addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)` — that slot is **before** [[What is AnonymousAuthenticationFilter]], so the token can still win. **`addFilter(new MyFilter())`** only works for a **Security** type that already has an order.

```java
http.addFilterBefore(jwt, UsernamePasswordAuthenticationFilter.class); // −1
http.addFilterAfter(tenant, AnonymousAuthenticationFilter.class);       // +1
http.addFilterAt(custom, UsernamePasswordAuthenticationFilter.class);   // 0, both run
```

**Listing 1.** TRACE `Invoking … (n/m)` shows the real order — [[How do you enable Spring Security debug logging for the filter chain]]. Boot `@Component` filters also need `FilterRegistrationBean.setEnabled(false)`.

> [!warning] At is not a swap; after Anonymous is too late for JWT
> `addFilterAt` **does not** remove `UsernamePasswordAuthenticationFilter`. Architecture’s “replaces” wording is the wrong model. A JWT filter **after** Anonymous sees `anonymousUser` already set — [[Why must a JWT filter run before AnonymousAuthenticationFilter]]. Wrong landmark still **compiles**; you just run in the wrong phase.

> [!tip] Interview answer
> addFilterBefore is minus one from a known filter’s order, addFilterAfter is plus one, addFilterAt is the same integer. At does not replace — you get two filters in that slot in undefined order. The landmark must be in FilterOrderRegistration. Put JWT before AnonymousAuthenticationFilter, not after.
