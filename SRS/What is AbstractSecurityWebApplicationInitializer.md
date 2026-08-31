<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Boot/AutoConfiguration #SRS

# What is `AbstractSecurityWebApplicationInitializer`?

> [!abstract] Short answer
> A Servlet 3 `WebApplicationInitializer` that **registers `DelegatingFilterProxy`** named **`springSecurityFilterChain`** (`DEFAULT_FILTER_NAME`) on the container **before other filters**, mapped to every URL. It does **not** create the `FilterChainProxy` bean — `@EnableWebSecurity` / `WebSecurityConfiguration` does that. **Spring Boot** registers the same proxy via **`SecurityFilterAutoConfiguration`**, so you **do not** subclass this in a typical Boot app.

## Two constructors

```d2
direction: down
war: "WAR / Servlet 3+" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
init: "AbstractSecurityWebApplicationInitializer" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
dfp: "DelegatingFilterProxy\nspringSecurityFilterChain" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
fcp: "FilterChainProxy bean\n@EnableWebSecurity" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}

war -> init
init -> dfp
dfp -> fcp: "looks up bean"
```

**Fig. 1.** Container hook vs Spring bean. See [[What is FilterChainProxy and DelegatingFilterProxy]].

**Security-only WAR:** pass `@EnableWebSecurity` config into `super(...)`. That also adds a `ContextLoaderListener`.

**Already using Spring MVC:** **empty** subclass. Passing config classes **again** errors (second root context). Load `WebSecurityConfig` from the **existing** initializer — docs put it in `getServletConfigClasses()` next to MVC so request matchers see `PathPatternParser`. Root/parent context may not.

```java
public class SecurityWebApplicationInitializer
        extends AbstractSecurityWebApplicationInitializer {
    public SecurityWebApplicationInitializer() {
        super(WebSecurityConfig.class); // Security-only app
    }
}

public class SecurityWebApplicationInitializer
        extends AbstractSecurityWebApplicationInitializer {
} // MVC: empty; load WebSecurityConfig elsewhere
```

**Listing 1.** Both shapes from Java configuration. Empty initializer **still needs** a `@EnableWebSecurity` class on the context. See [[How do you configure a SecurityFilterChain bean in Spring Security 6]] and [[Can Spring Security run with zero SecurityFilterChain beans]].

Overrides: `beforeSpringSecurityFilterChain` / `insertFilters` (e.g. `MultipartFilter` **before** CSRF), `enableHttpSessionEventPublisher()`, async + dispatcher types. Default session tracking is **cookie only** (URL tracking omitted against session fixation).

Boot: `SecurityFilterAutoConfiguration` publishes a `DelegatingFilterProxyRegistrationBean` when a bean named `springSecurityFilterChain` exists. Do not also register the initializer (double proxy).

> [!warning] DispatcherServlet initializer order
> `AbstractDispatcherServletInitializer` registers **its** filters first. Give that initializer a **higher** `Ordered` priority than the Security one, or Security’s `DelegatingFilterProxy` may sit in the wrong place.

> [!tip] Interview answer
> AbstractSecurityWebApplicationInitializer is the Servlet 3 replacement for web.xml: it registers DelegatingFilterProxy for springSecurityFilterChain. You still need @EnableWebSecurity to create the FilterChainProxy bean. Boot already does that registration, so you skip this class there.
