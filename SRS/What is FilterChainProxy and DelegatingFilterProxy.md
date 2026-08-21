<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `FilterChainProxy` and `DelegatingFilterProxy`?

> [!abstract] Short answer
> **`DelegatingFilterProxy`** is a Servlet container `Filter` that looks up a Spring bean and forwards every request to it. For Spring Security that bean is named **`springSecurityFilterChain`** and is a **`FilterChainProxy`**: one `Filter` that owns one or more [[What is SecurityFilterChain]] instances and runs only the first matching chain’s security filters.

The servlet container registers filters by its own rules and does **not** know Spring beans. Spring Framework’s `DelegatingFilterProxy` bridges that gap: register the proxy with the container; it lazily resolves a bean that implements `jakarta.servlet.Filter` and calls `doFilter` on it. By default the target bean name is the proxy’s `filter-name` (or an explicit `targetBeanName`). Servlet `init`/`destroy` on the target are **not** delegated unless `targetFilterLifecycle=true` — Spring usually owns that bean’s lifecycle.

Spring Security puts almost all Servlet support behind one such bean. `WebSecurityConfiguration` (imported by [[What is the purpose of EnableWebSecurity]]) exposes `@Bean(name = "springSecurityFilterChain")`. `WebSecurity` builds that bean as a `FilterChainProxy`. So the name you see in `web.xml`, `AbstractSecurityWebApplicationInitializer`, or Boot’s filter registration is the **bean id of the proxy target**, not a separate “magic” type.

```d2
direction: down
container: "Servlet container\nFilter registration" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
dfp: "DelegatingFilterProxy\n(container Filter)" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
fcp: "Bean springSecurityFilterChain\n= FilterChainProxy" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
pick: "Pick first matching\nSecurityFilterChain" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
filters: "Run that chain's\nordered security Filters" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
app: "Original FilterChain\n(e.g. DispatcherServlet)" {
  width: 280
  height: 80
  style.fill: "#f3e5f5"
}

container -> dfp
dfp -> fcp
fcp -> pick
pick -> filters
filters -> app
```

**Fig. 1.** Container → `DelegatingFilterProxy` → `FilterChainProxy` → one matching `SecurityFilterChain` → the rest of the application.

## What `FilterChainProxy` does

`FilterChainProxy` is itself a `Filter`. It holds a list of `SecurityFilterChain` objects. On each request it chooses the **first** chain whose `RequestMatcher` matches, then runs **that** chain’s filters (via an internal virtual chain) and finally continues the original servlet `FilterChain`. It does **not** merge filters from later chains.

That central role also lets it do cross-cutting work that individual security filters should not own alone: apply Spring Security’s `HttpFirewall`, and clear the `SecurityContext` to avoid leaks. Security filters are usually Spring beans, but they are wired into `FilterChainProxy` through `SecurityFilterChain`, **not** each registered as its own `DelegatingFilterProxy`.

```java
@Configuration
@EnableWebSecurity
public class MultiHttpSecurityConfig {

    @Bean
    @Order(1)
    SecurityFilterChain api(HttpSecurity http) throws Exception {
        http
            .securityMatcher("/api/**")
            .authorizeHttpRequests(auth -> auth.anyRequest().hasRole("ADMIN"))
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }

    @Bean
    SecurityFilterChain ui(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Conceptual Spring Security 6+ shape: multiple `SecurityFilterChain` beans; `@Order` decides which matcher is tried first; `securityMatcher` scopes a chain (see [[What is securityMatcher in Spring Security]]).

`FilterChainProxy` walks the ordered chains; the first match wins. A broader catch-all chain must sit **after** more specific ones, or the catch-all will swallow `/api/**` before the API chain runs. Within a chosen chain, filter order still matters for authentication before authorization — that is a separate concern from chain selection.

> [!warning] `FilterChainProxy` is not one `SecurityFilterChain`
> `springSecurityFilterChain` is the **orchestrator** (`FilterChainProxy`). Your `@Bean SecurityFilterChain …` methods are **entries** inside it. Confusing the two leads to wrong mental models of “where” a custom filter or matcher lives.

> [!warning] Bean name vs your method name
> The container/`DelegatingFilterProxy` looks up **`springSecurityFilterChain`**. Renaming your `SecurityFilterChain` `@Bean` method does not rename that proxy target; `WebSecurityConfiguration` still publishes the `FilterChainProxy` under that fixed name.

## How registration usually happens

| Setup | Who registers `DelegatingFilterProxy` |
| --- | --- |
| Classic WAR | `web.xml` filter named `springSecurityFilterChain` |
| Servlet 3+ | `AbstractSecurityWebApplicationInitializer` |
| Spring Boot | Auto-configuration registers the same named filter |

In all cases the proxy still resolves the Spring bean [[What is the springSecurityFilterChain bean name]] and hands the request to `FilterChainProxy`.

> [!tip] Interview answer
> **`DelegatingFilterProxy` is the servlet-container hook; it delegates to the Spring bean `springSecurityFilterChain`.** That bean is a **`FilterChainProxy`**, which picks the first matching **`SecurityFilterChain`** and runs only that chain’s security filters before the rest of the app. Multiple chains use `@Order` plus `securityMatcher`; first match wins.
