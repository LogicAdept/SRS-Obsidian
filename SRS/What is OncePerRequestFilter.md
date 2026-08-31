<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# What is `OncePerRequestFilter`?

> [!abstract] Short answer
> A **Spring Framework** abstract `Filter` (`org.springframework.web.filter.OncePerRequestFilter`) that extends [[What is GenericFilterBean in Spring Security]]. You override **`doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain)`**. `doFilter` sets a request attribute (`filterName + ".FILTERED"`) and **skips** if it is already there — **once per request thread / dispatch**, not “once per user click.” Architecture’s recommended base for a **custom Security filter**. Most Security filters use it; [[What is ExceptionTranslationFilter in Spring Security]] does **not**.

## Wrapper, then `doFilterInternal` once

```d2
direction: down
df: "doFilter\nalready .FILTERED?" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
skip: "chain.doFilter\nno work" {
  width: 200
  height: 40
  style.fill: "#eceff1"
}
work: "doFilterInternal(Http…)" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}

df -> skip: "yes"
df -> work: "no"
```

**Fig. 1.** Javadoc: also **ASYNC** / **ERROR** flags. Defaults: **`shouldNotFilterAsyncDispatch()` = true**, **`shouldNotFilterErrorDispatch()` = true** (since 3.2) — a later ERROR dispatch often **does not** re-run your JWT logic. Override those if you need thread-locals on every dispatch. See [[How do you implement a custom security filter in Spring Security]].

```java
public class TenantFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response,
            FilterChain chain) throws ServletException, IOException {
        chain.doFilter(request, response);
    }
}

http.addFilterBefore(new TenantFilter(), UsernamePasswordAuthenticationFilter.class);
```

**Listing 1.** Typed `Http*` args; no cast. JWT dumps: parse `Authorization`, `SecurityContextHolder.getContext().setAuthentication(...)`, then `chain.doFilter`. Authentication filters belong **after `LogoutFilter`** (dumps often landmark `UsernamePasswordAuthenticationFilter` because it is in [[What is FilterOrderRegistration]]). [[What is BearerTokenAuthenticationFilter]] is this pattern. See [[What is addFilterAfter in Spring Security]].

> [!warning] “Once” is not “one click”
> The same user click can be **REQUEST** then **FORWARD** / **ERROR** / **ASYNC**. The request attribute stops a second pass on the **same** request; ERROR/ASYNC are **off** by default. A Boot `@Component` filter still runs on the **container** chain unless `FilterRegistrationBean.setEnabled(false)`.

> [!tip] Interview answer
> OncePerRequestFilter is Spring’s Filter adapter that calls doFilterInternal once per request thread and passes HttpServletRequest. Spring Security tells you to extend it for custom filters, then addFilterBefore or After on HttpSecurity. It is not ExceptionTranslationFilter’s parent. Once does not mean once per browser click — check ERROR and ASYNC dispatcher defaults.
