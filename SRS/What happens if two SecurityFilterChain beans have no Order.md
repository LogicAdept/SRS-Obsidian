<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS

# What happens if two `SecurityFilterChain` beans have no `@Order`?

> [!abstract] Short answer
> Both sit at **`Ordered.LOWEST_PRECEDENCE`**. Their **relative** order is **undefined** — not an API you can rely on. `FilterChainProxy` still runs **only the first chain that matches**. A bean **without** `securityMatcher` matches **every** URL, so if that catch-all is tried first, a more specific `/api/**` chain **never runs**. Put **`@Order` on every extra chain**: smallest number first, catch-all **last** (omit `@Order` on **that one only**).

## `@Order` is the sort key, not declaration order

Docs: **no `@Order` defaults to last** *relative to a chain that has a higher `@Order`*. Two beans with **no** `@Order` (or the **same** value) are like `Customizer` beans with the same order: **undefined**. `WebSecurityConfiguration` injects `List<SecurityFilterChain>` and adds them in that list order. It does **not** fail if two **chain beans** share an order. (Two `WebSecurityConfigurer` adapters **do** throw: `@Order` must be unique.)

```d2
direction: down
beans: "two @Bean SecurityFilterChain\nno @Order" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
sort: "both LOWEST_PRECEDENCE\nrelative order undefined" {
  width: 280
  height: 50
  style.fill: "#fce4ec"
}
fcp: "FilterChainProxy first match" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
steal: "catch-all may win /api/**" {
  width: 260
  height: 40
  style.fill: "#ffebee"
}

beans -> sort
sort -> fcp
fcp -> steal
```

**Fig. 1.** Missing `@Order` on **both** chains is not “declaration order.” First-match then decides which DSL actually runs. See [[What is FilterChainProxy and DelegatingFilterProxy]].

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((a) -> a.anyRequest().authenticated());
    return http.build();
}

@Bean
SecurityFilterChain ui(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((a) -> a.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build(); // no securityMatcher, no @Order → last
}
```

**Listing 1.** Specific matcher **and** `@Order(1)` on the API chain; UI catch-all last. Omit `@Order` on **one** catch-all, not on two peers. See [[How do you configure JWT and form login as two SecurityFilterChain beans]].

Symptoms of two unordered chains: JWT vs form-login swapping, intermittent 401s if the list order changes, debug logs showing the **wrong** filter list for `/api/**`. `DEBUG` on `DefaultSecurityFilterChain` prints **Will secure** in list order at startup — that order **is** what `FilterChainProxy` will use.

> [!warning] Catch-all without matcher steals the request
> Default `HttpSecurity` matches **any** request. If that bean is first in the undefined sort, `/api/**` never reaches the API chain. Only **one** chain runs. This is not “both apply.” Unmatched URLs are a different hole — see [[What happens if no SecurityFilterChain matches a request]].

> [!tip] Interview answer
> No Order on two SecurityFilterChain beans means both are last precedence and their relative order is undefined. FilterChainProxy still takes the first match, so a catch-all with no securityMatcher can swallow /api if it sorts first. Give the specific chain @Order(1) and leave the catch-all unordered last.
