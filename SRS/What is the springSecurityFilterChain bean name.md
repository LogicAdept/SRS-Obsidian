<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is the `springSecurityFilterChain` bean name?

> [!abstract] Short answer
> **`springSecurityFilterChain`** is the Spring bean name of the **`FilterChainProxy`** that **`DelegatingFilterProxy`** looks up from the servlet container. `@EnableWebSecurity` / XML `<http>` / `WebSecurityConfiguration` publish that **one** proxy. Your **`SecurityFilterChain`** beans are **not** that name — they sit **behind** the proxy. Do **not** register a second bean called `springSecurityFilterChain`.

## One proxy name, many chains inside

```d2
direction: down
dfp: "DelegatingFilterProxy\nfilter-name = springSecurityFilterChain" {
  width: 340
  height: 50
}
fcp: "FilterChainProxy bean\nspringSecurityFilterChain" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
c1: "SecurityFilterChain beans" {
  width: 240
  height: 40
}

dfp -> fcp: "look up by name"
fcp -> c1: "first matching chain"
```

**Fig. 1.** Namespace: a `FilterChainProxy` bean named `"springSecurityFilterChain"` is created. Java config: that servlet `Filter` is responsible for URL security, login, logout. `AbstractSecurityWebApplicationInitializer` registers the same name with the container. See [[What is FilterChainProxy and DelegatingFilterProxy]], [[What is SecurityFilterChain]], and [[What is the purpose of EnableWebSecurity]].

The servlet **`filter-name` must match** that bean name. `DelegatingFilterProxy` lazily loads the Spring `Filter` bean; it is **not** the class that holds your `HttpSecurity` rules.

```xml
<filter>
    <filter-name>springSecurityFilterChain</filter-name>
    <filter-class>org.springframework.web.filter.DelegatingFilterProxy</filter-class>
</filter>
<filter-mapping>
    <filter-name>springSecurityFilterChain</filter-name>
    <url-pattern>/*</url-pattern>
</filter-mapping>
```

**Listing 1.** Classic `web.xml`. Boot / `AbstractSecurityWebApplicationInitializer` do this for you. A `@Bean SecurityFilterChain app(...)` is **another** bean (`app`); it is assembled **into** the proxy. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]] and [[Can Spring Security run with zero SecurityFilterChain beans]].

> [!warning] Rename the servlet filter, break the lookup
> If the container filter is not named `springSecurityFilterChain`, `DelegatingFilterProxy` will not find the proxy bean (unless you point it at that bean name explicitly). Do not `@Bean("springSecurityFilterChain")` your own `SecurityFilterChain` — that name is **infrastructure**.

> [!tip] Interview answer
> The bean name is springSecurityFilterChain. That is the FilterChainProxy DelegatingFilterProxy looks up from the servlet container. Individual SecurityFilterChain beans have their own names and live behind that one proxy. You should not reuse springSecurityFilterChain for an application bean.
