<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/FilterChain #Java/Annotations #SRS

# What is the difference between EnableWebSecurity and EnableMethodSecurity?

> [!abstract] Short answer
> **`@EnableWebSecurity` turns on the servlet filter chain. `@EnableMethodSecurity` turns on AOP method annotations.** One does **not** enable the other. URL `authorizeHttpRequests` never runs for a `@Scheduled` job, a listener, or an internal bean call. Method security does. Boot’s security starter typically gives you a `SecurityFilterChain`; it still does **not** enable `@PreAuthorize`.

## Filters vs method advisors

`@EnableWebSecurity` (since **3.2**) `@Import`s `WebSecurityConfiguration` and `HttpSecurityConfiguration` (plus MVC/OAuth2 selectors) and `@EnableGlobalAuthentication`. That publishes `springSecurityFilterChain` — a `FilterChainProxy` of `SecurityFilterChain`s. You customize with a `SecurityFilterChain` `@Bean` and `HttpSecurity` (login, CSRF, `authorizeHttpRequests`). It protects **HTTP requests** that enter the servlet filter chain.

`@EnableMethodSecurity` publishes Spring AOP advisors (`AuthorizationManagerBeforeMethodInterceptor` / `After`) for `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, `@PostFilter` (pre/post **on** by default). It does **not** register a servlet filter. It can run in a non-web context.

They are **complementary**. Putting both on one `@Configuration` is normal. That is **not** the illegal mix of `@EnableMethodSecurity` with deprecated `@EnableGlobalMethodSecurity` (two **method** stacks). `@EnableWebSecurity` plus leftover `@EnableGlobalMethodSecurity` is **not** `@EnableMethodSecurity` — old `prePostEnabled` defaults to **`false`**.

Reactive apps use `@EnableWebFluxSecurity` / `SecurityWebFilterChain`, still a different switch from method security.

```java
@Configuration
@EnableWebSecurity
public class WebSecurityConfig {

    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests((authorize) -> authorize
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated());
        return http.build();
    }
}
```

**Listing 1.** Conceptual Security **7.1** — HTTP only. A service method called from `@Scheduled` never hits this chain.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
}
```

**Listing 2.** Conceptual — method AOP. Boot does not add this when you add `spring-boot-starter-security`.

```d2
direction: down
http: "@EnableWebSecurity\nSecurityFilterChain" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
aop: "@EnableMethodSecurity\nmethod advisors" {
  width: 240
  height: 50
  style.fill: "#c8e6c9"
}
req: "HTTP request" {
  width: 160
  height: 40
  style.fill: "#fff3e0"
}
job: "@Scheduled / listener / self-call" {
  width: 240
  height: 45
  style.fill: "#ffcdd2"
}

req -> http
job -> aop
req -> aop: "if the controller method is annotated"
```

**Fig. 1.** URL rules stop at the filter. Method rules follow the bean. See [[What is EnableMethodSecurity]], [[Can method security run without a SecurityFilterChain]], [[Why does method security still matter if URL rules exist]], [[What is the difference between EnableMethodSecurity and EnableGlobalMethodSecurity]], [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]].

> [!warning] Boot 3: a filter chain is not method security
> `@EnableWebSecurity` (or Boot’s default `SecurityFilterChain`) does not honor `@PreAuthorize`. Keeping `@EnableGlobalMethodSecurity` next to web security is still the **old** method switch (`prePostEnabled` default **false**). Replace it with `@EnableMethodSecurity`. Do not expect URL `permitAll` / `authenticated` to cover internal calls.

> [!tip] Interview answer
> `@EnableWebSecurity` is the servlet filter chain — `SecurityFilterChain` and `HttpSecurity` for URLs. `@EnableMethodSecurity` is AOP for `@PreAuthorize` and friends. Neither turns the other on. Boot gives you web security by default and still leaves method security off, which is why a scheduled job or a skipped filter can bypass URL rules.
