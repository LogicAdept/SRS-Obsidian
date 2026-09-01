<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/FilterChain #Java/Spring/Core/IoC/SpEL #SRS

# What is `SecurityExpressionHandler` in Spring Security?

> [!abstract] Short answer
> The **3.1+ facade** that builds a SpEL **`EvaluationContext`** for a secure object `T`. **`createEvaluationContext(Authentication, T)`** (eager) and, since **5.8**, **`createEvaluationContext(Supplier<Authentication>, T)`** (lazy). The **root** is a **`SecurityExpressionOperations`** (`hasRole`, `hasAuthority`, …). **Web and method are different types.** Method: **`MethodSecurityExpressionHandler`** / **`DefaultMethodSecurityExpressionHandler`** (`MethodInvocation`; **`setReturnObject`**, **`filter`**). Web today: **`DefaultHttpSecurityExpressionHandler`** (`RequestAuthorizationContext`). A handler on **`HttpSecurity`** does **not** change **`@PreAuthorize`**.

## Parser + context, not the expression strings

**`getExpressionParser()`** parses `"hasRole('ADMIN') && #id == authentication.name"`. The handler supplies **variables** (`#root`, method args) and the **root object**. **`AbstractSecurityExpressionHandler`** is the usual base; override **`createSecurityExpressionRoot`**.

| Bean | `T` | Used by |
| --- | --- | --- |
| **`DefaultMethodSecurityExpressionHandler`** | **`MethodInvocation`** | **`@PreAuthorize` / `@PostAuthorize` / `@PreFilter` / `@PostFilter`** |
| **`DefaultHttpSecurityExpressionHandler`** (5.8+) | **`RequestAuthorizationContext`** | **`WebExpressionAuthorizationManager`** |
| **`DefaultWebSecurityExpressionHandler`** | **`FilterInvocation`** | Legacy **`authorizeRequests` / `FilterSecurityInterceptor`** |
| **`DefaultMessageSecurityExpressionHandler`** | messaging | WebSocket |

**`@EnableMethodSecurity`** publishes interceptors that call **`createEvaluationContext(Supplier, MethodInvocation)`**. Expose the method handler as a **`static @Bean`** so it exists **before** method-security `@Configuration` initializes. Prefer a **custom `@Bean`** (`@PreAuthorize("@authz.isAdmin(#root)")`) over subclassing. If you subclass, override the **`Supplier`** overload — the old **`createSecurityExpressionRoot(Authentication, …)`** path is **not** what `@EnableMethodSecurity` calls.

```java
@Bean
static MethodSecurityExpressionHandler methodSecurityExpressionHandler(RoleHierarchy roleHierarchy) {
	DefaultMethodSecurityExpressionHandler handler = new DefaultMethodSecurityExpressionHandler();
	handler.setRoleHierarchy(roleHierarchy);
	return handler;
}
```

**Listing 1.** Official customization. **`setReturnObject` / `filter`** live on **`MethodSecurityExpressionHandler`**, not the base interface — that is **`returnObject`** / collection filtering in SpEL ([[What are Spring Security expressions]], [[What is EnableMethodSecurity]], [[What is AuthorizationManager in method security]]).

Web SpEL on Security 6+ is **`.access(new WebExpressionAuthorizationManager("hasRole('ADMIN')"))`**, not **`http.authorizeRequests().expressionHandler(...)`**.

```d2
direction: down
ann: "@PreAuthorize SpEL" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
h: "SecurityExpressionHandler\ncreateEvaluationContext" {
  width: 250
  height: 48
  style.fill: "#fff3e0"
}
r: "SecurityExpressionRoot\nhasRole / authentication" {
  width: 250
  height: 48
  style.fill: "#c8e6c9"
}

ann -> h
h -> r
```

**Fig. 1.** Two handler beans if you use **both** URL SpEL and method SpEL. Customizing only HTTP leaves **`@PreAuthorize`** on the method default ([[What is the difference between EnableMethodSecurity and EnableGlobalMethodSecurity]], [[How do you configure authorizeHttpRequests in Spring Security 6]]).

> [!warning] Web handler ≠ method handler
> **`HttpSecurity` expression config** never reaches **`@PreAuthorize`**. Register **`MethodSecurityExpressionHandler`**. **`authorizeRequests().expressionHandler`** is the **old** interceptor DSL.

> [!warning] `@EnableMethodSecurity` uses the `Supplier` overload
> Overriding only **`createSecurityExpressionRoot(Authentication, MethodInvocation)`** is a no-op. Override **`createEvaluationContext(Supplier, MethodInvocation)`** or use an **`@authz` bean**. **`ROLE_`** prefix still comes from the root / **`GrantedAuthorityDefaults`**, not from “adding a handler.”

> [!tip] Interview answer
> SecurityExpressionHandler builds the SpEL EvaluationContext and root object for a given invocation type. DefaultMethodSecurityExpressionHandler serves @PreAuthorize; DefaultHttpSecurityExpressionHandler serves web WebExpressionAuthorizationManager. They are separate beans. EnableMethodSecurity needs a static MethodSecurityExpressionHandler bean and the lazy Supplier createEvaluationContext method.
