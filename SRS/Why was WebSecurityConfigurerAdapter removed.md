<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# Why was WebSecurityConfigurerAdapter removed?

> [!abstract] Short answer
> **`WebSecurityConfigurerAdapter`** was **deprecated in Spring Security 5.7** and **removed in Spring Security 6** so applications would move to **component-based configuration**: register a **`SecurityFilterChain` `@Bean`** for `HttpSecurity` (and a **`WebSecurityCustomizer` `@Bean`** when customizing `WebSecurity`) instead of extending an abstract adapter.

## Timeline and replacement

| Version | Status |
|---|---|
| Spring Security **5.4+** | `SecurityFilterChain` bean style available |
| Spring Security **5.7** | `WebSecurityConfigurerAdapter` **deprecated** |
| Spring Security **6** (Spring Boot **3**) | Adapter **removed** — extending it does not compile |

The deprecation Javadoc and Spring’s migration guide point to the same replacement:

```java
@Configuration
public class SecurityConfiguration {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(authz -> authz.anyRequest().authenticated())
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }
}
```

**Listing 1.** Component-based `HttpSecurity` setup — no subclass of `WebSecurityConfigurerAdapter`.

For ignoring paths at the `WebSecurity` level, register a **`WebSecurityCustomizer`** bean instead of overriding `configure(WebSecurity)`. Authentication stores (`UserDetailsService`, LDAP factories, and so on) are likewise published as beans rather than configured only inside `configure(AuthenticationManagerBuilder)`.

## Why the team pushed beans

Spring Security encouraged this model so security configuration is ordinary Spring **components**, not inheritance from a framework base class. That style:

- Composes with the rest of the application context like any other `@Bean`
- Makes **multiple `SecurityFilterChain` beans** (with `@Order`) a natural pattern for distinct URL spaces
- Aligns with the lambda DSL and `authorizeHttpRequests` configuration shown throughout current docs

```d2
direction: right
old: "extends\nWebSecurityConfigurerAdapter" {
  width: 240
  height: 80
  style.fill: "#fce4ec"
}
neu: "@Bean SecurityFilterChain\n(+ optional WebSecurityCustomizer)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

old -> neu: "Security 5.7 deprecate\nSecurity 6 remove"
```

**Fig. 1.** Inheritance-based adapter configuration → bean-based `SecurityFilterChain`.

> [!warning] Boot 3 interview / migration trap
> On **Spring Boot 3**, the classpath is Spring Security **6**: **`WebSecurityConfigurerAdapter` is gone**. Copy-pasting an old `extends WebSecurityConfigurerAdapter` + `configure(HttpSecurity)` class fails at compile time. Migrate to a **`SecurityFilterChain` bean** (and separate beans for users / password encoding). See [[What is SecurityFilterChain]] and [[What happens if two SecurityFilterChain beans have no Order]].

> [!tip] Interview answer
> WebSecurityConfigurerAdapter was removed in Spring Security 6 after a 5.7 deprecation so teams would use component-based security: a SecurityFilterChain bean configures HttpSecurity instead of subclassing the adapter. Boot 3 apps that still extend the adapter simply will not compile.
