<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/FilterChain #SRS

# What is AuthorizationManager in method security?

> [!abstract] Short answer
> **`AuthorizationManager<T>` is the Security 5.6+ decision API.** It **supersedes** `AccessDecisionManager` and `AccessDecisionVoter`. A method interceptor calls **one** manager: `authorize(Supplier<Authentication>, T)` returns an `AuthorizationResult`; `verify(...)` throws `AccessDeniedException` on deny. For `@PreAuthorize`, `T` is `MethodInvocation`; for `@PostAuthorize`, `MethodInvocationResult`.

## One manager per interceptor

`@EnableMethodSecurity` publishes advisors that each wrap a manager:

| Annotation | Interceptor | Manager |
|---|---|---|
| `@PreAuthorize` | `AuthorizationManagerBeforeMethodInterceptor` | `PreAuthorizeAuthorizationManager` |
| `@PostAuthorize` | `AuthorizationManagerAfterMethodInterceptor` | `PostAuthorizeAuthorizationManager` |
| `@Secured` | before interceptor | `SecuredAuthorizationManager` |
| JSR-250 | before interceptor | `Jsr250AuthorizationManager` |

The same `AuthorizationManager` type is what **`authorizeHttpRequests`** uses on the filter chain — one interface for request, method, and message authorization. The `Supplier<Authentication>` lets the lookup stay lazy (the `@EnableMethodSecurity` arrangement). Grant, deny, or **`null` (abstain)**.

`hasPermission` SpEL is **not** an `AuthorizationManager`. It still goes through `MethodSecurityExpressionHandler` → `PermissionEvaluator`. `@EnableMethodSecurity` **does not** autowire a `PermissionEvaluator` `@Bean`; set it on a `MethodSecurityExpressionHandler` — [[How do you implement ABAC with PermissionEvaluator in Spring Security]].

```java
@Component
public class MyPreAuthorizeAuthorizationManager
        implements AuthorizationManager<MethodInvocation> {

    @Override
    public AuthorizationResult authorize(Supplier<Authentication> authentication,
            MethodInvocation invocation) {
        // inspect authentication.get() and invocation arguments
        return new AuthorizationDecision(/* granted */);
    }
}

@Configuration
@EnableMethodSecurity(prePostEnabled = false)
class MethodSecurityConfig {

    @Bean
    @Role(BeanDefinition.ROLE_INFRASTRUCTURE)
    Advisor preAuthorize(MyPreAuthorizeAuthorizationManager manager) {
        return AuthorizationManagerBeforeMethodInterceptor.preAuthorize(manager);
    }
}
```

**Listing 1.** Conceptual Security **7.1** — replace the default pre/post managers. Leave `prePostEnabled` **true** and add a second advisor and `@PreAuthorize` runs **twice**.

```d2
direction: down
aop: "AuthorizationManagerBeforeMethodInterceptor" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
am: "AuthorizationManager\nauthorize(Supplier, MethodInvocation)" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
res: "AuthorizationResult\ngrant / deny / abstain" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

aop -> am -> res
```

**Fig. 1.** Voters and `AccessDecisionManager` are the old stack (`MethodSecurityInterceptor`). See [[How does method security work in Spring]], [[What is EnableMethodSecurity]], [[What is MethodSecurityInterceptor]], [[At what levels can Spring Security enforce access control]].

> [!warning] Do not stack a second pre-authorize advisor
> `@EnableMethodSecurity` already publishes `AuthorizationManagerBeforeMethodInterceptor.preAuthorize()`. A manual extra interceptor with defaults left **on** double-invokes the join point. Turn **`prePostEnabled = false`** and publish **your** advisors, or customize with `ObjectPostProcessor` / `AuthorizationManagerFactory`. `PermissionEvaluator` auto-detect is **not** how the new config works.

> [!tip] Interview answer
> `AuthorizationManager` replaced `AccessDecisionManager` and voters for methods and URLs. Each method interceptor asks one manager with a lazy `Authentication` supplier and the `MethodInvocation`. Deny is `AccessDeniedException`. `PermissionEvaluator` is still wired on the expression handler, not auto-detected as a second manager.
