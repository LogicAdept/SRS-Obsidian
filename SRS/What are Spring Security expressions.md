<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Core/IoC/SpEL #SRS

# What are Spring Security expressions?

> [!abstract] Short answer
> They are **SpEL** strings evaluated against a **`SecurityExpressionRoot`** (`SecurityExpressionOperations`): **`hasRole` / `hasAuthority` / `hasAnyRole` / `permitAll` / `denyAll` / `isAuthenticated` / `isAnonymous` / `isRememberMe` / `isFullyAuthenticated` / `hasPermission`**, plus **`authentication`**. Use them in **`@PreAuthorize`** (and post/filter annotations) and, on the web, in XML **`access=`** or **`WebExpressionAuthorizationManager`**. **`@Secured` is not SpEL.**

## One root object, two call sites

The methods live on **`SecurityExpressionOperations`**. **`hasRole("ADMIN")`** is **`hasAuthority`** with a **`ROLE_`** prefix (configurable). **`hasAnyRole` / `hasAnyAuthority`** are **OR** across the given names. **`permitAll()`** is always true; **`denyAll()`** always false. **`getAuthentication()`** is exposed in SpEL as **`authentication`** (for example **`authentication.name`**).

**Method security** (needs **`@EnableMethodSecurity`**; **`prePostEnabled` defaults to true**):

```java
@PreAuthorize("hasAuthority('permission:read') || hasRole('ADMIN')")
@PostAuthorize("returnObject.owner == authentication.name")
Customer read(String id) { /* ... */ }

@PreAuthorize("@authz.decide(#root)")
void write(Order order) { /* ... */ }
```

**Listing 1.** **`@PreAuthorize` / `@PostAuthorize` / `@PreFilter` / `@PostFilter`** are the SpEL annotations. **`#root`** is the **`MethodSecurityExpressionOperations`**. Custom logic: a bean method, e.g. **`@authz.decide(#root)`**. Method parameters are **`#id`**, **`#order`**. **`filterObject` / `returnObject`** are for filter/post annotations.

**`@Secured`** is a **legacy attribute list** (`{"ROLE_USER", "ROLE_ADMIN"}`), **off** until **`securedEnabled = true`**. It cannot take **`and`**, **`#param`**, or **`@bean`**. Prefer **`@PreAuthorize`**.

**HTTP** prefers type-safe managers (`hasRole("ADMIN")` on the DSL). SpEL on URLs is **`WebExpressionAuthorizationManager`** (or XML **`access="hasRole('ADMIN') and hasAuthority('db')"`**):

```java
http.authorizeHttpRequests(authorize -> authorize
	.requestMatchers("/admin/**").hasRole("ADMIN")
	.requestMatchers("/test/**")
		.access(new WebExpressionAuthorizationManager(
			"hasRole('ADMIN') && hasRole('USER')")));
```

**Listing 2.** Same vocabulary; the Java DSL **`hasRole`** is an **`AuthorizationManager`**, not a string, unless you wrap it.

```d2
direction: down
spel: "SpEL string" {
  width: 140
  height: 40
  style.fill: "#e3f2fd"
}
root: "SecurityExpressionRoot\nhasRole hasAuthority …" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
sites: "@PreAuthorize  |  WebExpressionAuthorizationManager" {
  width: 340
  height: 45
  style.fill: "#c8e6c9"
}

spel -> root
root -> sites
```

**Fig. 1.** Expressions are **not** a separate language — they are SpEL plus this root ([[What is PreAuthorize]], [[What is the difference between Secured RolesAllowed and PreAuthorize]], [[What is hasRole versus hasAuthority in Spring Security]], [[What is hasPermission in Spring Security method expressions]], [[What is Spring Expression Language]]).

**`hasPermission(#obj, 'write')`** delegates to a **`PermissionEvaluator`**. Until you set one on a **static** **`MethodSecurityExpressionHandler`**, it is **`DenyAllPermissionEvaluator`**. **`@EnableGlobalMethodSecurity`** is deprecated in favor of **`@EnableMethodSecurity`**.

> [!warning] Annotations without `@EnableMethodSecurity` do nothing
> **`prePostEnabled`** is true **only after** that annotation (or XML **`<method-security>`**). **`@Secured` / `@RolesAllowed`** stay off until **`securedEnabled` / `jsr250Enabled`**. A missing enable is the usual “it never fired” bug.

> [!warning] `@Secured` is not an expression
> You cannot write **`hasRole('A') and hasRole('B')`** on **`@Secured`**. Multiple string attributes are **names**, not SpEL. For **AND**, method parameters, or beans, use **`@PreAuthorize`**. **`hasRole('ROLE_ADMIN')`** doubles the prefix if the default is already **`ROLE_`**.

> [!tip] Interview answer
> Spring Security expressions are SpEL on SecurityExpressionRoot: hasRole, hasAuthority, permitAll, isAuthenticated, authentication, hasPermission. They power @PreAuthorize and related annotations after @EnableMethodSecurity, and web XML or WebExpressionAuthorizationManager. @Secured is a non-SpEL role list. hasRole adds ROLE_; hasPermission needs a PermissionEvaluator or it always denies.
