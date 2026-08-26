<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is PreAuthorize?

> [!abstract] Short answer
> **`@PreAuthorize`** is a Spring Security annotation whose **SpEL `value` is evaluated before** a bean method runs. If the expression is false, `AuthorizationManagerBeforeMethodInterceptor` throws `AccessDeniedException` and **the target never executes**. It needs `@EnableMethodSecurity` (`prePostEnabled` defaults to `true`). `@Secured` and `@RolesAllowed` cannot take SpEL.

## When it runs

`@Target({METHOD, TYPE})`, `@Retention(RUNTIME)`, since Security **3.0**. Place it on a method, class, interface, or as a **meta-annotation**. With `@EnableMethodSecurity`, Spring publishes `AuthorizationManagerBeforeMethodInterceptor.preAuthorize()`, which uses `PreAuthorizeAuthorizationManager`. Advisor order for `@PreAuthorize` is **200** (after `@PreFilter` at 100).

The interceptor builds a SpEL `EvaluationContext` from `MethodSecurityExpressionHandler` / `MethodSecurityExpressionRoot` (extends `SecurityExpressionRoot`). Common expression pieces:

| Piece | Meaning |
|---|---|
| `hasRole('ADMIN')` | `hasAuthority` with default `ROLE_` prefix → looks for `ROLE_ADMIN` |
| `hasAuthority('permission:read')` | Exact `GrantedAuthority` string, no prefix |
| `authentication` / `principal` | Current `Authentication` and its principal |
| `#param` | Method argument named by `DefaultSecurityParameterNameDiscoverer` |
| `permitAll` / `denyAll` | Always true / false; **does not** load `Authentication` |
| `hasPermission(#obj, 'write')` | Delegates to `PermissionEvaluator` |
| `@bean.method(...)` | Call another Spring bean from SpEL |

`returnObject` belongs to **`@PostAuthorize`**. It is not the return of the method you are about to call.

```java
@Component
public class BankService {

    @PreAuthorize("hasRole('ADMIN')")
    public Account readAccount(Long id) {
        return load(id);
    }

    @PreAuthorize("#userId == authentication.name")
    public Account readOwn(String userId) {
        return loadFor(userId);
    }
}
```

**Listing 1.** Conceptual — `hasRole('ADMIN')` requires `ROLE_ADMIN`; `#userId` is the method parameter, not a request header.

Parameter names come from `DefaultSecurityParameterNameDiscoverer`, in order: `@P("c")`, Spring Data `@Param`, **`-parameters`** compile flag, then debug symbols (debug symbols **do not** work on interfaces).

```d2
direction: down
proxy: "AOP proxy" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}
pre: "@PreAuthorize SpEL\nAuthorizationManagerBeforeMethodInterceptor" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
body: "Target method" {
  width: 160
  height: 50
  style.fill: "#fff3e0"
}
deny: "AccessDeniedException\nmethod skipped" {
  width: 200
  height: 50
  style.fill: "#ffcdd2"
}

proxy -> pre
pre -> body: "true"
pre -> deny: "false"
```

**Fig. 1.** A failed pre-check never enters the method body.

Compared with `@Secured` / `@RolesAllowed`: those take **role/authority names**, not SpEL, and need `securedEnabled` / `jsr250Enabled` on `@EnableMethodSecurity`. See [[How does method security work in Spring]], [[What is EnableMethodSecurity]], and [[What is the difference between Secured RolesAllowed and PreAuthorize]].

> [!warning] Proxy + parameter names
> `this.readAccount(id)` and **private** methods skip the proxy, so `@PreAuthorize` never runs — [[Why does method security skip self-invocation]]. `#userId` is also a no-op (or a SpEL error) if the compiler did not keep parameter names and you did not use `@P` / `@Param`. Boot’s security starter still does not enable method security — [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]].

> [!tip] Interview answer
> `@PreAuthorize` is a SpEL gate on the AOP proxy, evaluated before the method. Denial is `AccessDeniedException` and the body never runs. It needs `@EnableMethodSecurity`; `@Secured` cannot express argument or ownership checks.
