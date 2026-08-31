<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #Security/Authorization #SRS

# What is hasPermission in Spring Security method expressions?

> [!abstract] Short answer
> **`hasPermission` is the method-security SpEL hook for object-level checks.** `@PreAuthorize("hasPermission(#c, 'write')")` does **not** look at roles by itself. `MethodSecurityExpressionRoot` forwards to a **`PermissionEvaluator`**. Until you call `setPermissionEvaluator` on a **static** `MethodSecurityExpressionHandler` bean, that evaluator is **`DenyAllPermissionEvaluator`** (always `false`). `@EnableMethodSecurity` does **not** auto-detect a `PermissionEvaluator` bean.

## Two call shapes

The 7.1 reference lists `hasPermission` as a hook into your `PermissionEvaluator` for object-level authorization. Official sample: `@PreAuthorize("hasPermission(#c, 'write')")` — current `Authentication` must have `write` on that `Contact`. Parameter names use `#c` / `@P` / `-parameters` the same way as other method SpEL.

| SpEL | Evaluator method |
|---|---|
| `hasPermission(target, permission)` | `hasPermission(Authentication, Object target, Object permission)` |
| `hasPermission(targetId, targetType, permission)` | `hasPermission(Authentication, Serializable targetId, String targetType, Object permission)` |

The three-argument form is for when the instance is **not** loaded yet. `permission` is whatever you passed — usually a `String` (`'WRITE'`). Unquoted `read` / `write` / `create` / `delete` / `admin` are fields on the SpEL root (ACL samples use `hasPermission(filterObject, read)`). A `null` target **must** evaluate to `false`.

On `@PreAuthorize` / `@PostAuthorize`, `false` is `AccessDeniedException`. On `@PreFilter` / `@PostFilter`, `false` **drops** that element; it does not deny the call. `hasRole` / `hasAuthority` stay authority-string checks; they cannot see domain attributes. A `@authz.check(authentication, #root)` bean is the other official programmatic hook if you do not want `PermissionEvaluator`.

```java
@PreAuthorize("hasPermission(#c, 'write')")
public void updateContact(@P("c") Contact contact) { /* ... */ }

@PreAuthorize("hasPermission(#id, 'com.example.Contact', 'READ')")
public Contact loadContact(Long id) { /* ... */ }
```

**Listing 1.** Conceptual Security **7.1** — two-arg instance check vs id+type. `#c` is the method argument, not HTTP.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {

    @Bean
    static MethodSecurityExpressionHandler methodSecurityExpressionHandler(
            PermissionEvaluator permissionEvaluator) {
        DefaultMethodSecurityExpressionHandler handler =
                new DefaultMethodSecurityExpressionHandler();
        handler.setPermissionEvaluator(permissionEvaluator);
        return handler;
    }
}
```

**Listing 2.** Conceptual wiring. This is **not** a second interceptor. Do **not** rely on a `PermissionEvaluator` `@Bean` being picked up by `@EnableMethodSecurity`.

```d2
direction: down
spel: "@PreAuthorize\nhasPermission(#c, 'write')" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
root: "MethodSecurityExpressionRoot" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
pe: "PermissionEvaluator" {
  width: 220
  height: 45
  style.fill: "#c8e6c9"
}
deny: "DenyAllPermissionEvaluator\n(default)" {
  width: 240
  height: 50
  style.fill: "#ffcdd2"
}

spel -> root
root -> pe
root -> deny: "if unset"
```

**Fig. 1.** Expression method, then evaluator. See [[How do you implement ABAC with PermissionEvaluator in Spring Security]], [[What is PreAuthorize]], [[Can PreAuthorize use method parameters]], [[What is authentication in method-security SpEL]].

> [!warning] Not auto-detected, not a second interceptor
> Dumps that `@EnableMethodSecurity` auto-wires `PermissionEvaluator` are **wrong**. `PrePostMethodSecurityConfiguration` does not inject it. Leaving the default evaluator makes every `hasPermission(...)` fail closed. Registering the evaluator on the expression handler does **not** double-invoke the join point. Two interceptors come from mixing enable annotations, not from this bean. Deprecated `GlobalMethodSecurityConfiguration` **did** pick up a unique `PermissionEvaluator` — that is the old stack only. See [[What is GlobalMethodSecurityConfiguration]], [[What is denyAll in a method-security expression]].

> [!tip] Interview answer
> `hasPermission` is method-security SpEL for object-level ABAC. It delegates to a `PermissionEvaluator` you install on a static `MethodSecurityExpressionHandler`. The default evaluator always returns false, and `@EnableMethodSecurity` does not auto-detect your bean. Use `hasPermission(#entity, 'WRITE')` or the id-plus-type form when the instance is not loaded yet.
