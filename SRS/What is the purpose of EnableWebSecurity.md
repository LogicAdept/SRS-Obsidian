<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS

# What is the purpose of `@EnableWebSecurity`?

> [!abstract] Short answer
> Put **`@EnableWebSecurity`** on a **`@Configuration`** class to turn on Spring Security’s **servlet Java config**: it publishes the **`springSecurityFilterChain`** `FilterChainProxy` and lets you expose **`SecurityFilterChain`** beans (`HttpSecurity`). It also wires **Spring MVC** integration (`@AuthenticationPrincipal`, and so on). It is **not** `@EnableMethodSecurity`. Spring Security **6** still uses this annotation; it does **not** use `WebSecurityConfigurerAdapter`.

## The switch for the servlet filter chain

```d2
direction: down
ann: "@EnableWebSecurity" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
wsc: "WebSecurityConfiguration\nspringSecurityFilterChain" {
  width: 280
  height: 50
}
fcp: "FilterChainProxy" {
  width: 180
  height: 40
  style.fill: "#e8f5e9"
}

ann -> wsc
wsc -> fcp
```

**Fig. 1.** Javadoc: add it to an `@Configuration` and define security by **exposing a `SecurityFilterChain` bean** (or a `WebSecurityCustomizer`). Java config: that filter is responsible for URL protection, login, logout, default headers. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]], [[What is FilterChainProxy and DelegatingFilterProxy]], and [[What is HttpSecurity in Spring Security]].

`debug = true` is a **separate** switch (`DebugFilter`); leave it **false** in production. See [[How do you enable Spring Security debug logging for the filter chain]].

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    SecurityFilterChain app(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated());
        return http.build();
    }
}
```

**Listing 1.** Spring Security 6 shape. With **no** `SecurityFilterChain` beans, `WebSecurityConfiguration` still **synthesizes** a default chain (authenticated + form login + HTTP Basic). See [[Can Spring Security run with zero SecurityFilterChain beans]] and [[What is the difference between EnableWebSecurity and EnableMethodSecurity]].

> [!warning] Boot already locked the app down
> `spring-boot-starter-security` on the classpath **secures** a web app **before** you write this annotation. `@EnableWebSecurity` is how you **customize** `HttpSecurity`, not how you “turn Security on from zero.” A `SecurityFilterChain` `@Bean` replaces Boot’s default chain. `UserDetailsService` / `PasswordEncoder` beans do **not** require this annotation by themselves.

> [!tip] Interview answer
> EnableWebSecurity is the annotation you put on a configuration class to turn on Spring Security’s web filter chain and MVC integration. You then expose a SecurityFilterChain bean from HttpSecurity. On Spring Boot the starter already secures URLs; this annotation is how you customize that. Spring Security 6 still uses it; WebSecurityConfigurerAdapter is gone.
