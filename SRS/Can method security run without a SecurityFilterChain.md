<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/FilterChain #SRS

# Can method security run without a SecurityFilterChain?

> [!abstract] Short answer
> **Yes.** Method security is **Spring AOP on bean methods**, not a servlet filter. `@EnableMethodSecurity` registers interceptors that authorize `@PreAuthorize` / `@Secured` (and related) invocations. That check does **not** go through `FilterChainProxy` or a `SecurityFilterChain`. A scheduler, message listener, or test that calls the service is a non-HTTP entry — there is **no** filter chain on that path.

## Two stacks, one `Authentication`

Spring Security models authorization at the **request** level (`authorizeHttpRequests` on a `SecurityFilterChain`) **and** at the **method** level. The latter is native Spring AOP: `AuthorizationManagerBeforeMethodInterceptor` / `AuthorizationManagerAfterMethodInterceptor` wrap the join point. `@EnableMethodSecurity` on any `@Configuration` is what turns that on. `spring-boot-starter-security` **does not**.

Denial is `AccessDeniedException`. An unauthenticated direct call (empty `SecurityContextHolder`) is `AuthenticationCredentialsNotFoundException`. The interceptor reads `Authentication` from `SecurityContextHolder` — in a web request the filter chain usually filled that; without HTTP, **you** (or `@WithMockUser`) must.

Official method-security tests call the bean with `@WithMockUser`. They do not perform an HTTP request and do not replace (or even use) a `SecurityFilterChain`. HTTP tests that keep the production chain are a different exercise — [[How do you test method security without replacing SecurityFilterChain]].

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
}

@Service
public class BankService {

    @PreAuthorize("hasRole('ADMIN')")
    public Account readAccount(String id) {
        return load(id);
    }
}
```

**Listing 1.** Conceptual Security **7.1** enablement — advisors on the service proxy. No `SecurityFilterChain` `@Bean` is required for this check to run.

```java
@Autowired BankService bankService;

@WithMockUser(roles = "ADMIN")
@Test
void readAccountWithAdminRoleThenInvokes() {
    this.bankService.readAccount("12345678");
}

@WithMockUser(roles = "WRONG")
@Test
void readAccountWithWrongRoleThenAccessDenied() {
    assertThatExceptionOfType(AccessDeniedException.class)
            .isThrownBy(() -> this.bankService.readAccount("12345678"));
}
```

**Listing 2.** Conceptual official sample — invoke the proxy; `roles = "ADMIN"` is `ROLE_ADMIN`. No MockMvc, no filter chain.

```d2
direction: down
http: "HTTP request" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
chain: "SecurityFilterChain\nExceptionTranslationFilter" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
job: "Scheduler / listener / test\n(no servlet)" {
  width: 240
  height: 55
  style.fill: "#ffebee"
}
aop: "@EnableMethodSecurity proxy\n@PreAuthorize" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
svc: "Target @Service method" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}

http -> chain -> aop -> svc
job -> aop
```

**Fig. 1.** The filter chain is an HTTP on-ramp. Method security sits on the bean whether that on-ramp exists.

A Boot **servlet** app with Security on the classpath still **auto-configures** a default `SecurityFilterChain` (`SecurityAutoConfiguration` / `SpringBootWebSecurityConfiguration`). Method security does **not** replace or disable that. You **also** add `@EnableMethodSecurity`. Non-web apps and tests that never start a servlet have **no** chain at all — see [[What is EnableMethodSecurity]], [[How does method security work in Spring]], [[At what levels can Spring Security enforce access control]].

> [!warning] No chain means no HTTP 403 translation
> `ExceptionTranslationFilter` lives **inside** `FilterChainProxy`. It is the bridge from `AccessDeniedException` / `AuthenticationException` to an HTTP status (typically **403**, or the authentication entry point). A job, listener, or `@WithMockUser` service test is **not** in that `doFilter` try/catch — the exception stays an exception unless **you** handle it.

> [!warning] A default Boot chain is not method security
> `@EnableMethodSecurity` without a custom `HttpSecurity` bean does **not** turn off Boot’s default web lock-down. URL rules and method annotations are separate. Missing `@EnableMethodSecurity` makes `@PreAuthorize` a silent no-op even when HTTP is locked down — [[Why does method security still matter if URL rules exist]].

> [!tip] Interview answer
> Yes — method security is AOP on the service proxy via `@EnableMethodSecurity`, so it does not need a `SecurityFilterChain`. Jobs, listeners, and direct tests still hit the interceptors. Without the servlet chain there is no `ExceptionTranslationFilter`, so denial is a raw `AccessDeniedException`, not HTTP 403. Boot web apps still get a default filter chain; that is extra HTTP security, not a requirement for `@PreAuthorize`.
