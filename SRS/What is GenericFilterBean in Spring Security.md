<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `GenericFilterBean` in Spring Security?

> [!abstract] Short answer
> A **Spring Framework** `Filter` adapter (`org.springframework.web.filter.GenericFilterBean`), **not** a Security class. It maps `web.xml` init-params onto bean properties, implements `BeanNameAware` / `ServletContextAware` / `InitializingBean`, and leaves **`doFilter`** to subclasses. Spring Security filters sit on it: **`OncePerRequestFilter`** (most Security filters) or **directly** ([[What is ExceptionTranslationFilter in Spring Security]]). Architecture’s custom-filter tip is **`OncePerRequestFilter`**, then [[What is addFilterAfter in Spring Security]] on `HttpSecurity`.

## Spring-aware Filter, then Security’s chain

```d2
direction: down
gfb: "GenericFilterBean\ninit-param → setters, doFilter" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
opr: "OncePerRequestFilter\ndoFilterInternal(Http…)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ss: "CsrfFilter, Basic, DisableEncodeUrl…" {
  width: 300
  height: 40
  style.fill: "#fff3e0"
}
etf: "ExceptionTranslationFilter" {
  width: 260
  height: 40
  style.fill: "#fce4ec"
}

gfb -> opr
opr -> ss
gfb -> etf: "extends directly"
```

**Fig. 1.** Javadoc: “handy superclass for any type of filter”; filtering is still `Filter.doFilter`. No `ApplicationContext` load — beans come from the root context. See [[How do you implement a custom security filter in Spring Security]].

```java
public class AuditFilter extends GenericFilterBean {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        chain.doFilter(request, response);
    }
}

http.addFilterAfter(new AuditFilter(), AnonymousAuthenticationFilter.class);
```

**Listing 1.** Valid, but you cast to `HttpServletRequest` yourself. Architecture prefers `OncePerRequestFilter` + `doFilterInternal` so the filter runs **once per request**. Register on **`HttpSecurity`**, not only as a container filter. See [[What is FilterChainProxy and DelegatingFilterProxy]].

> [!warning] Bean ≠ Security order
> A `@Component` `Filter` is registered with the **embedded container** as well. It can run **twice** and **outside** `FilterOrderRegistration`. `FilterRegistrationBean.setEnabled(false)` so only `HttpSecurity` adds it. `GenericFilterBean` does **not** place you in the Security chain by itself.

> [!tip] Interview answer
> GenericFilterBean is Spring’s Filter adapter: init-params become properties and you implement doFilter. Spring Security uses it as the parent of OncePerRequestFilter, and ExceptionTranslationFilter extends it directly. For a custom security filter, Spring Security’s docs tell you to extend OncePerRequestFilter and addFilterAfter on HttpSecurity, not to rely on a servlet FilterRegistrationBean.
