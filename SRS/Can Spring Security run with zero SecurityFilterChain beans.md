<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Boot/AutoConfiguration #SRS

# Can Spring Security run with zero `SecurityFilterChain` beans?

> [!abstract] Short answer
> **Yes.** Servlet Spring Security does not require you to declare a `SecurityFilterChain` `@Bean`. `@EnableWebSecurity` still publishes the `springSecurityFilterChain` `FilterChainProxy`. When that bean list is empty, `WebSecurityConfiguration` **builds the default chain internally** (every request authenticated, form login, HTTP Basic). That chain lives inside `FilterChainProxy`; it is not a bean you can inject. **Omitting the bean does not turn HTTP security off.**

## Zero beans is not an empty `FilterChainProxy`

`@EnableWebSecurity` imports `WebSecurityConfiguration`, which creates the filter named `springSecurityFilterChain`. It autowires `List<SecurityFilterChain>` (optional). If that list is empty, it adds a builder equivalent to:

```java
@Configuration
@EnableWebSecurity
public class NoChainBeanConfig {
    // no SecurityFilterChain @Bean — Spring Security still starts
}
```

**Listing 1.** Valid Spring Security 6+ setup: enable web security and declare no chain beans. The default chain is still assembled.

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
        .formLogin(Customizer.withDefaults())
        .httpBasic(Customizer.withDefaults());
    return http.build();
}
```

**Listing 2.** The chain `WebSecurityConfiguration` synthesizes when `securityFilterChains` is empty.

A Boot application with `spring-boot-starter-security` usually **does** have a bean: `SpringBootWebSecurityConfiguration` (`@ConditionalOnDefaultWebSecurity`) publishes `defaultSecurityFilterChain` with the same authenticated / form-login / HTTP Basic shape, and a nested `WebSecurityEnablerConfiguration` adds `@EnableWebSecurity` if the `springSecurityFilterChain` bean is missing. Publishing your own `SecurityFilterChain` makes that Boot default **back off completely** — you then own every matcher and filter.

```d2
direction: down
enable: "@EnableWebSecurity\nzero chain beans" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
boot: "Boot @ConditionalOnDefaultWebSecurity\ndefaultSecurityFilterChain @Bean" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
wsc: "WebSecurityConfiguration\nspringSecurityFilterChain()" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
fcp: "FilterChainProxy has ≥1 chain" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}

enable -> wsc: "synthesize Listing 2"
boot -> wsc: "bean list not empty"
wsc -> fcp
```

**Fig. 1.** Either core Security synthesizes the default chain off-bean, or Boot registers that same shape as a bean. `FilterChainProxy` is not left empty.

Three different “nothing configured” situations:

| Situation | What `FilterChainProxy` does |
|---|---|
| **Zero `SecurityFilterChain` beans** + `@EnableWebSecurity` | Synthesizes the default **full** chain (Listing 2) |
| **No matching chain**, or a matching chain whose `getFilters()` is empty (`WebSecurity.ignoring()`, XML `filters="none"`, `new DefaultSecurityFilterChain(matcher)`) | Logs “No security”, resets the firewalled request, continues the servlet chain |
| **`permitAll()` on `authorizeHttpRequests`** | Still runs that chain’s filters (headers, CSRF, …); only authorization is a no-op |

`FilterChainProxy`’s no-arg constructor starts with `Collections.emptyList()`. On each request it still wraps with `HttpFirewall`, then `getFilters()` returns `null` when nothing matches. Empty or null filter lists skip security filters — see [[What happens if no SecurityFilterChain matches a request]] and [[What is FilterChainProxy and DelegatingFilterProxy]]. That empty-list state is **not** what `@EnableWebSecurity` produces when you simply omit beans.

A chain with **zero filters** is also allowed: Spring Security uses that when the application wants certain requests ignored. That is still a `SecurityFilterChain` instance (often not your `@Bean`), not “zero beans.” See [[What is SecurityFilterChain]].

> [!warning] Omitting the bean does not mean permitAll
> Zero chain **beans** still give you the default **authenticated** chain (or Boot’s equivalent bean). `permitAll()` is the opposite idea: a **real** chain keeps running `HeaderWriterFilter`, `CsrfFilter`, and the rest; only the authorization rule is public. `WebSecurity.ignoring()` (or an unmatched request) is what skips those filters — and then Spring Security **cannot** write security headers. Prefer `permitAll` for static resources; see [[What is the difference between permitAll and web ignoring]].

> [!warning] Firewall and `SecurityContext` still run
> Even when no security filters run, `FilterChainProxy` still applies `HttpFirewall` and, after the request, **clears** `SecurityContextHolder`. An empty filter list is not “Spring Security is absent from this request.”

> [!tip] Interview answer
> Yes — you can start servlet Spring Security with no SecurityFilterChain bean. EnableWebSecurity still builds FilterChainProxy, and if the bean list is empty it installs the default chain: any request authenticated, form login, HTTP Basic. Boot usually registers that same chain as a bean and backs off when you declare your own. That is not the same as permitAll or as ignoring requests; those either keep the default filters or skip them entirely.
