<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #Security/Authorization #SRS

# How do you implement ABAC with PermissionEvaluator in Spring Security?

> [!abstract] Short answer
> **Implement `PermissionEvaluator` and wire it into method-security SpEL.** `hasPermission(...)` on `@PreAuthorize` / `@PostAuthorize` / `@PreFilter` / `@PostFilter` delegates to that bean. You decide from **who** (`Authentication`), **what** (domain object or id + type), and **which permission** — attributes, not only roles. Register it with `DefaultMethodSecurityExpressionHandler.setPermissionEvaluator`. Until you do, the default is **`DenyAllPermissionEvaluator`** (always `false`).

## Two `hasPermission` shapes, one strategy

`SecurityExpressionRoot` (the SpEL root) exposes:

| SpEL | Evaluator method |
|---|---|
| `hasPermission(target, permission)` | `hasPermission(Authentication, Object target, Object permission)` |
| `hasPermission(targetId, targetType, permission)` | `hasPermission(Authentication, Serializable targetId, String targetType, Object permission)` |

The three-argument form is for when the instance is **not** loaded yet. `targetType` is usually a Java class name; any string is fine if it matches how you load permissions. A `null` target **must** return `false` (check `target == null` in the expression if you need a different answer). The `permission` argument is whatever the expression passed — typically a `String` such as `"READ"` / `"write"`. Unquoted `read` / `write` / `create` / `delete` / `admin` are fields on the root object (the ACL samples use `hasPermission(filterObject, read)`).

This is **not** the ACL module. `PermissionEvaluator` lives in core and has **no** ACL dependency. `AclPermissionEvaluator` is one implementation if you store ACLs; a custom class is the usual ABAC path (owner, tenant, clearance, time, …). A `@Bean` method in SpEL (`@authz.check(authentication, #root)`) is the other official hook if you would rather not implement the interface.

```java
public class EmployeePermissionEvaluator implements PermissionEvaluator {

    @Override
    public boolean hasPermission(Authentication authentication,
            Object target, Object permission) {
        if (target == null) {
            return false;
        }
        return decide(authentication, (Employee) target, permission);
    }

    @Override
    public boolean hasPermission(Authentication authentication,
            Serializable targetId, String targetType, Object permission) {
        return decideById(authentication, targetId, targetType, permission);
    }
}
```

**Listing 1.** Conceptual — inspect principal, resource attributes, and the permission token. Always-`true` is not ABAC; default `DenyAllPermissionEvaluator` is always-`false`.

```java
@Configuration
@EnableMethodSecurity
class MethodSecurityConfig {

    @Bean
    static MethodSecurityExpressionHandler expressionHandler(
            PermissionEvaluator employeePermissionEvaluator) {
        DefaultMethodSecurityExpressionHandler handler =
                new DefaultMethodSecurityExpressionHandler();
        handler.setPermissionEvaluator(employeePermissionEvaluator);
        return handler;
    }
}

@Service
class EmployeeService {

    @PreAuthorize("hasPermission(#id, 'com.example.Employee', 'READ')")
    Employee read(Long id) {
        return load(id);
    }

    @PreAuthorize("hasPermission(#employee, 'WRITE')")
    void update(Employee employee) {
        save(employee);
    }
}
```

**Listing 2.** Conceptual Security **7.1** — `static` `MethodSecurityExpressionHandler` so the bean exists before method-security `@Configuration` initializes. `#id` / `#employee` need parameter-name discovery — [[Can PreAuthorize use method parameters]].

```d2
direction: down
spel: "@PreAuthorize\nhasPermission(#id, type, 'READ')" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
root: "MethodSecurityExpressionRoot\nhasPermission(...)" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
eval: "PermissionEvaluator\nAuthentication + target + permission" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

spel -> root -> eval
```

**Fig. 1.** SpEL does not know your attributes. The evaluator is where ABAC lives.

Publish the handler as a **`static` `@Bean` `MethodSecurityExpressionHandler`**, the same pattern used for `RoleHierarchy`. `@EnableMethodSecurity` is still required; Boot’s security starter does not turn method security on. See [[What is hasPermission in Spring Security method expressions]], [[What is PreAuthorize]], [[Why does method security still matter if URL rules exist]].

> [!warning] Default evaluator denies everything
> If you write `hasPermission(...)` and never call `setPermissionEvaluator`, you are on **`DenyAllPermissionEvaluator`**. Every check is `false` → `AccessDeniedException`. The documented wiring is a **`static` `MethodSecurityExpressionHandler` `@Bean`** that calls `setPermissionEvaluator`. `authorizeHttpRequests` / `hasRole` on the filter chain cannot read domain-object fields; that is why ABAC sits on the **method**.

> [!tip] Interview answer
> ABAC with Spring Security is a `PermissionEvaluator` plus `hasPermission` in `@PreAuthorize`. Implement both overloads, register the evaluator on a static `MethodSecurityExpressionHandler` bean, and decide from `Authentication`, the object or id+type, and the permission. The default evaluator always denies; URL role rules cannot see object attributes.
