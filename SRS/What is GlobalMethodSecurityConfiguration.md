<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS

# What is GlobalMethodSecurityConfiguration?

> [!abstract] Short answer
> **The deprecated `@Configuration` base class behind `@EnableGlobalMethodSecurity`.** It published `MethodSecurityInterceptor`, a `DelegatingMethodSecurityMetadataSource`, and the voter / `AccessDecisionManager` stack. You **subclassed** it to override protected hooks (`createExpressionHandler()`, `accessDecisionManager()`, …) and still had to put **`@EnableGlobalMethodSecurity` on the subclass**. `@EnableMethodSecurity` replaced that with **bean-based** `AuthorizationManager` interceptors — do not extend a replacement base class.

## What the class actually registered

`@EnableGlobalMethodSecurity` `@Import`s `GlobalMethodSecuritySelector`, which brings in `GlobalMethodSecurityConfiguration` (since **3.2**). That class is itself `@Configuration`. Its main beans:

| Bean | Role |
|---|---|
| `methodSecurityInterceptor` | `MethodSecurityInterceptor` (or `AspectJMethodSecurityInterceptor` if `mode = ASPECTJ`) |
| `methodSecurityMetadataSource` | `DelegatingMethodSecurityMetadataSource` from the enable flags plus optional `customMethodSecurityMetadataSource()` |
| `preInvocationAuthorizationAdvice` | `ExpressionBasedPreInvocationAdvice` when pre/post is on |

The interceptor is built from overridable collaborators: `accessDecisionManager()` (default `AffirmativeBased` with `PreInvocationAuthorizationAdviceVoter` / `Jsr250Voter` as flags allow, plus `RoleVoter` and `AuthenticatedVoter`), `afterInvocationManager()` (post-invocation / filter path when pre/post is on), `authenticationManager()`, `runAsManager()` (default `null`).

If **none** of `prePostEnabled` / `securedEnabled` / `jsr250Enabled` is true and there is no custom metadata source, startup fails: no annotation support was activated. On Security **6+** this whole type lives in optional **`spring-security-access`**; **7.1** fails fast without that module. Prefer migrating.

```java
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class OldMethodSecurityConfig extends GlobalMethodSecurityConfiguration {

    @Override
    protected MethodSecurityExpressionHandler createExpressionHandler() {
        DefaultMethodSecurityExpressionHandler handler =
                new DefaultMethodSecurityExpressionHandler();
        handler.setPermissionEvaluator(new EmployeePermissionEvaluator());
        return handler;
    }
}
```

**Listing 1.** Conceptual legacy customization. The annotation on the subclass is mandatory — `setImportMetadata` / a class-level lookup both require `@EnableGlobalMethodSecurity`. A subclass with neither import nor annotation fails: the annotation is required.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {

    @Bean
    static MethodSecurityExpressionHandler methodSecurityExpressionHandler() {
        DefaultMethodSecurityExpressionHandler handler =
                new DefaultMethodSecurityExpressionHandler();
        handler.setPermissionEvaluator(new EmployeePermissionEvaluator());
        return handler;
    }
}
```

**Listing 2.** Conceptual Security **7.1** replacement. Official migration: **direct beans**, not a `GlobalMethodSecurityConfiguration` subclass. The framework’s `PrePostMethodSecurityConfiguration` / `SecuredMethodSecurityConfiguration` / `Jsr250MethodSecurityConfiguration` are the imported replacements — you do not extend them.

```d2
direction: down
ann: "@EnableGlobalMethodSecurity\non the subclass" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
gmsc: "GlobalMethodSecurityConfiguration" {
  width: 260
  height: 50
  style.fill: "#ffcdd2"
}
msi: "MethodSecurityInterceptor\nvoters / metadata" {
  width: 260
  height: 50
  style.fill: "#ffcdd2"
}
ems: "@EnableMethodSecurity" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
beans: "MethodSecurityExpressionHandler\nAuthorizationManager beans" {
  width: 280
  height: 50
  style.fill: "#c8e6c9"
}

ann -> gmsc
gmsc -> msi
ems -> beans
```

**Fig. 1.** Old path: subclass the global config. New path: publish beans. See [[What is EnableGlobalMethodSecurity]], [[What is MethodSecurityInterceptor]], [[What is AuthorizationManager in method security]], [[What happens if you mix EnableMethodSecurity and EnableGlobalMethodSecurity]].

> [!warning] Do not mix a subclass with `@EnableMethodSecurity`
> Extending `GlobalMethodSecurityConfiguration` **and** adding `@EnableMethodSecurity` is two interceptor families. Official docs do not support stacking them. Also: this **old** class **does** pick up a unique `PermissionEvaluator` bean in `afterSingletonsInstantiated`. `@EnableMethodSecurity` does **not** — wire `setPermissionEvaluator` on a **static** `MethodSecurityExpressionHandler` bean, or `hasPermission` stays `DenyAllPermissionEvaluator`. See [[How do you implement ABAC with PermissionEvaluator in Spring Security]].

> [!tip] Interview answer
> `GlobalMethodSecurityConfiguration` is the old, deprecated configuration class that `@EnableGlobalMethodSecurity` imported. You subclassed it to swap the expression handler or access-decision manager, and you still had to put the annotation on the subclass. `@EnableMethodSecurity` dropped that base class in favor of ordinary beans and `AuthorizationManager` interceptors. Do not keep the subclass next to the new annotation.
