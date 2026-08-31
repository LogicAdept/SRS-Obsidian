<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Annotations #SRS

# What is `HttpSecurity` in Spring Security?

> [!abstract] Short answer
> The **Java DSL** for one servlet **`SecurityFilterChain`** — Spring Security’s `<http>` in code (since **3.2**). You inject it into a `@Bean SecurityFilterChain`, call `authorizeHttpRequests`, `formLogin`, `httpBasic`, `csrf`, `cors`, `logout`, `headers`, `sessionManagement`, `addFilterAfter`, … then **`return http.build()`**. That build is a `DefaultSecurityFilterChain`. Spring Security **6** does **not** use `WebSecurityConfigurerAdapter.configure(HttpSecurity)`.

## Builder for one chain

```d2
direction: down
inj: "@Bean SecurityFilterChain(HttpSecurity http)" {
  width: 320
  height: 40
  style.fill: "#e3f2fd"
}
dsl: "lambda Customizer methods\nsecurityMatcher · authorizeHttpRequests" {
  width: 340
  height: 50
  style.fill: "#fff3e0"
}
chain: "http.build()\nDefaultSecurityFilterChain" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
fcp: "FilterChainProxy\nfirst matching chain" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}

inj -> dsl
dsl -> chain
chain -> fcp
```

**Fig. 1.** Javadoc: similar to XML `<http>`; **default matches every request**. `securityMatcher(...)` / `securityMatchers(...)` choose **which requests enter this chain**. `authorizeHttpRequests` chooses **authorization inside** it. See [[What is securityMatcher in Spring Security]], [[What is SecurityFilterChain]], and [[What is FilterChainProxy and DelegatingFilterProxy]].

`HttpSecurity` is a **prototype** builder (`HttpSecurityConfiguration`). Each chain bean gets a **fresh** instance — CSRF off on `/api/**` does not turn CSRF off on the form-login chain. `@EnableWebSecurity` still required so the DSL and `FilterChainProxy` exist.

```java
@Configuration
@EnableWebSecurity
public class FormLoginSecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests((authorize) -> authorize
                .requestMatchers("/**").hasRole("USER"))
            .formLogin(Customizer.withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Class-level javadoc example. Use **`authorizeHttpRequests` + `requestMatchers`**, not `authorizeRequests` / `antMatchers`. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]], [[How do you configure authorizeHttpRequests in Spring Security 6]], and [[Why was WebSecurityConfigurerAdapter removed]].

> [!warning] Adapter is gone; matcher ≠ authorize
> SS6 **removed** `WebSecurityConfigurerAdapter`. A `@Bean` chain **replaces** Boot’s default web security (form login is **opt-in** on that bean). Mixing `securityMatcher("/api/**")` with `anyRequest()` only authorizes **inside** `/api/**` — other URLs need **another** chain or they are **unprotected**.

> [!tip] Interview answer
> HttpSecurity is the Java <http> builder: you configure one SecurityFilterChain and call build(). In Spring Security 6 that is a @Bean, not WebSecurityConfigurerAdapter. securityMatcher picks which requests hit this chain; authorizeHttpRequests sets the rules inside it. Default is all requests until you add a matcher.
