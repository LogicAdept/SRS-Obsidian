<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS

# How do you implement a custom security filter in Spring Security?

> [!abstract] Short answer
> Implement `jakarta.servlet.Filter` (or extend `OncePerRequestFilter` and override `doFilterInternal`). Register it on **`HttpSecurity`** with **`addFilterBefore` / `addFilterAfter` / `addFilterAt`** relative to a **known Spring Security filter class**. Custom **authentication** goes **after `LogoutFilter`**. Do **not** rely on a servlet-container-only registration if you care about Security’s order.

## Write the filter, then place it

Rule of thumb from the servlet architecture:

| Kind of filter | Place it after | So that already happened |
|---|---|---|
| Exploit protection | `SecurityContextHolderFilter` | SecurityContext loaded |
| Authentication | `LogoutFilter` | Context + headers/CORS/CSRF |
| Authorization | `AnonymousAuthenticationFilter` | Authentication filters finished |

```java
public class TenantFilter implements Filter {
    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        if (isUserAllowed(request.getHeader("X-Tenant-Id"))) {
            chain.doFilter(req, res);
            return;
        }
        throw new AccessDeniedException("Access denied");
    }

    private boolean isUserAllowed(String tenantId) {
        return tenantId != null;
    }
}
```

**Listing 1.** Official shape: continue the chain on success; on failure throw `AccessDeniedException` so `ExceptionTranslationFilter` can map it. `OncePerRequestFilter` is the same idea with `doFilterInternal(HttpServletRequest, HttpServletResponse, FilterChain)`. A JWT-style filter that `SecurityContextHolder.getContext().setAuthentication(...)` then `chain.doFilter` is still an **authentication** filter — park it **after `LogoutFilter`** (and usually **before** `AnonymousAuthenticationFilter`). See [[Why must a JWT filter run before AnonymousAuthenticationFilter]].

```java
@Bean
SecurityFilterChain app(HttpSecurity http) throws Exception {
    http.addFilterAfter(new TenantFilter(), AnonymousAuthenticationFilter.class);
    return http.build();
}
```

**Listing 2.** `addFilterAfter` / `addFilterBefore(filter, LogoutFilter.class)` insert; `addFilterAt(filter, SomeFilter.class)` is the **replacement slot**. If the DSL already added that class (`formLogin()`, `httpBasic()`), `addFilterAt` **does not** silently drop it — disable the DSL first. See [[What is the difference between addFilterBefore addFilterAfter and addFilterAt]] and [[How do you disable form login on a SecurityFilterChain]].

```d2
direction: down
http: "HttpSecurity" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
before: "addFilterBefore\nrelative to Class" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
after: "addFilterAfter" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
at: "addFilterAt\nreplace that Class" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

http -> before
http -> after
http -> at
```

**Fig. 1.** Custom filters join [[What is FilterChainProxy and DelegatingFilterProxy]] only through these three methods (plus a DSL that already knows the filter).

> [!warning] A `@Component` `Filter` often runs twice
> Spring Boot registers servlet `Filter` beans with the container **and** `HttpSecurity` may run them again, in a **different order**. Prefer a non-bean filter, or a `FilterRegistrationBean` with `setEnabled(false)` so **only** `HttpSecurity` adds it.

> [!warning] Do not swallow the request
> If you neither call `chain.doFilter` nor complete the response (or throw `AccessDeniedException` / `AuthenticationException`), the client waits. Listing 1’s throw path is the documented deny.

> [!tip] Interview answer
> Implement Filter or OncePerRequestFilter, then HttpSecurity addFilterBefore or After a concrete Security filter class — custom auth after LogoutFilter. Registering only as a servlet Filter skips Security’s order and can run twice under Boot. addFilterAt is a replace slot; turn off formLogin or httpBasic if that filter is already in the DSL.
