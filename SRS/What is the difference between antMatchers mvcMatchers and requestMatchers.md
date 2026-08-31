<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is the difference between `antMatchers`, `mvcMatchers`, and `requestMatchers`?

> [!abstract] Short answer
> **`antMatchers`** used **`AntPathRequestMatcher`** (raw servlet path, Ant `**`). **`mvcMatchers`** used **`MvcRequestMatcher`** so rules followed **Spring MVC** (servlet path, how controllers map). Both lived on **`authorizeRequests`**. **`requestMatchers`** (since **5.8**) is the **`authorizeHttpRequests`** API; current docs match **`PathPattern`** (`PathPatternRequestMatcher`) so Security and MVC share one parser. Spring Security **7 removed** `AntPathRequestMatcher` / `MvcRequestMatcher` and `authorizeRequests`. First-match still applies: specific patterns before `anyRequest()`.

## Three names, one job: build a `RequestMatcher`

```d2
direction: down
old: "authorizeRequests\nantMatchers | mvcMatchers" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
now: "authorizeHttpRequests\nrequestMatchers → PathPattern" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}

old -> now: "SS 5.8+ / gone in SS7"
```

**Fig. 1.** XML `request-matcher` was `ant` / `mvc` / `regex`; default is now **`PathPattern`**. MVC integration: publish `PathPatternRequestMatcherBuilderFactoryBean` so string `requestMatchers` / `securityMatcher` use the same parser as `@RequestMapping`. See [[How do you configure authorizeHttpRequests in Spring Security 6]], [[What is intercept-url in Spring Security]], and [[What is AuthorizationFilter in Spring Security]].

`mvcMatchers` existed so `/orders` and `/orders/` (and suffix patterns MVC served) were **one** resource — `antMatchers("/orders")` could miss a variant the controller still handled. `requestMatchers` is meant to close that gap via **`PathPattern`**. Non-MVC paths: `PathPatternRequestMatcher.withDefaults()`; a servlet prefix: `.basePath("/mvc")`. Regex: `RegexRequestMatcher`, not Ant.

```java
http.authorizeHttpRequests((authorize) -> authorize
        .requestMatchers("/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated());
```

**Listing 1.** SS6/7 spelling. `requestMatchers(HttpMethod, String…)` since 5.8. Do not write `antMatchers` / `mvcMatchers` — they will not compile on SS7. See [[Why does authorization matcher order matter in Spring Security]] and [[What is securityMatcher in Spring Security]] (`securityMatcher` picks the **chain**; these methods pick **rules inside** it).

> [!warning] Unmatched rule is deny, unmatched chain is open
> Omitting `anyRequest()` on `authorizeHttpRequests` **denies** leftover URLs; it does **not** leave them public. A lone `securityMatcher("/app/**")` with **no** catch-all chain **does** leave `/` unprotected. Defense in depth: still use method security if someone bypasses the web matcher.

> [!tip] Interview answer
> antMatchers was Ant-path on the servlet URL; mvcMatchers used Spring MVC matching so trailing-slash variants could not skip a rule. Both were authorizeRequests. Spring Security 6 uses authorizeHttpRequests and requestMatchers; 7 uses PathPatternRequestMatcher only. Put specific patterns first and end with anyRequest.
