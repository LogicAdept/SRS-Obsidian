<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is EnableMethodSecurity?

> [!abstract] Short answer
> **`@EnableMethodSecurity`** is the Spring Security configuration annotation that **activates method-level authorization** on Spring-managed beans. It superseded deprecated **`@EnableGlobalMethodSecurity`** and, by default, enables **`@PreAuthorize`**, **`@PostAuthorize`**, **`@PreFilter`**, and **`@PostFilter`**.

## What it turns on

Add **`@EnableMethodSecurity`** to any **`@Configuration`** class (or use **`<sec:method-security/>`** in XML). Spring Security then publishes AOP advisors that enforce annotations on bean method invocations — including checks on parameters and return values.

Default attribute values on the annotation:

| Attribute | Default | Enables |
|---|---|---|
| **`prePostEnabled`** | **`true`** | `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, `@PostFilter` |
| **`securedEnabled`** | **`false`** | `@Secured` |
| **`jsr250Enabled`** | **`false`** | JSR-250 (`@RolesAllowed`, …) |

Set **`securedEnabled = true`** or **`jsr250Enabled = true`** when you need those annotation styles in addition to (or instead of) pre/post annotations.

```java
@Configuration
@EnableMethodSecurity
public class SecurityConfig {
}
```

**Listing 1.** Minimal activation — pre/post method security is on without extra flags.

```d2
direction: right
cfg: "@Configuration\n@EnableMethodSecurity" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
aop: "Spring AOP advisors\n(method interceptors)" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
bean: "@Service method\n@PreAuthorize(...)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

cfg -> aop -> bean: "authorize\ninvocation"
```

**Fig. 1.** Configuration registers advisors; annotated service methods are checked at runtime.

## Migration from `@EnableGlobalMethodSecurity`

**`@EnableGlobalMethodSecurity`** is **deprecated**. **`@EnableMethodSecurity`** replaces it with an **`AuthorizationManager`**-based model, native Spring AOP, and clearer defaults.

The critical default flip: **`@EnableGlobalMethodSecurity`** had **`prePostEnabled = false`** by default, so **`@PreAuthorize` did nothing** unless you explicitly enabled pre/post. **`@EnableMethodSecurity`** defaults **`prePostEnabled` to `true`**, matching what most applications expect after a Boot 3 / Security 6 migration.

> [!warning] Not on by default with Boot starter alone
> **`spring-boot-starter-security`** secures HTTP requests but **does not activate method security automatically**. Without **`@EnableMethodSecurity`**, **`@PreAuthorize`** on a service method is a no-op. URL rules from **`SecurityFilterChain`** also do not replace method-level checks — see [[What is the difference between EnableWebSecurity and EnableMethodSecurity]] and [[Why does method security still matter if URL rules exist]].

> [!tip] Interview answer
> @EnableMethodSecurity switches on method-level authorization via Spring AOP. It replaces @EnableGlobalMethodSecurity and defaults prePostEnabled to true, so @PreAuthorize works out of the box. @Secured and JSR-250 stay off unless you enable them; Boot’s security starter still requires this annotation for method security.
