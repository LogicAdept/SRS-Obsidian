<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS

# What happens if two `SecurityFilterChain` beans share the same `@Order`?

> [!abstract] Short answer
> **Undefined relative order.** Spring Security does **not** reject two `SecurityFilterChain` `@Bean`s with the same `@Order` (or the same `Ordered.getOrder()`). Both compare equal, so which one sits first in `FilterChainProxy` is **not guaranteed**. The proxy still runs **only the first match**. Use **distinct** integers: smaller number first. This is **not** a compile error.

## Same number, same bucket

Java config sorts chains by `@Order`. **Lower wins.** Docs’ examples use `@Order(1)`, `@Order(2)`, then a catch-all with **no** `@Order` (that last bean is `Ordered.LOWEST_PRECEDENCE`). Two beans that **share** a value are the same case as Customizer beans: **no `@Order`, or the same value → order undefined.**

```d2
direction: down
same: "@Order(1) + @Order(1)" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
undef: "equal sort keys\nrelative order undefined" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}
fcp: "FilterChainProxy\nfirst RequestMatcher wins" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}

same -> undef
undef -> fcp
```

**Fig. 1.** Duplicate `@Order` does not merge chains and does not fail startup. See [[What is FilterChainProxy and DelegatingFilterProxy]].

`WebSecurityConfiguration` injects `List<SecurityFilterChain>` and appends that list. The **unique-`@Order` `IllegalStateException`** applies to **`WebSecurityConfigurer` adapters**, not to chain beans. Missing `@Order` on **both** beans is the **same** equal-key problem, just in the **last** bucket — see [[What happens if two SecurityFilterChain beans have no Order]].

```java
@Bean
@Order(1)
SecurityFilterChain api(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        .authorizeHttpRequests((a) -> a.anyRequest().authenticated());
    return http.build();
}

@Bean
@Order(2) // not 1
SecurityFilterChain ui(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((a) -> a.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults());
    return http.build();
}
```

**Listing 1.** Distinct values. `@Order` on the `@Bean` method is enough. If both were `@Order(1)` and the UI chain has **no** `securityMatcher`, it can match `/api/**` first and the API chain never runs. See [[How do you configure JWT and form login as two SecurityFilterChain beans]].

Startup `DEBUG` on `DefaultSecurityFilterChain` prints **Will secure** in the list order that will actually be used. That is how you see the wrong chain “win” — at runtime, not at compile time.

> [!warning] Same `@Order` is not a compiler error
> The app starts. You get the wrong filter list, JWT vs form login swapped, or a catch-all stealing `/api/**`. Two old `WebSecurityConfigurer` classes with the same `@Order` **do** throw; do not assume chain beans behave that way.

> [!tip] Interview answer
> Two SecurityFilterChain beans with the same Order are both valid and their relative order is undefined. FilterChainProxy still takes the first match, so a catch-all can swallow the specific chain. Give them distinct Orders; adapters are the API that demands unique Order and throws.
