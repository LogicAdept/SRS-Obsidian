<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS

# What is EnableGlobalMethodSecurity?

> [!abstract] Short answer
> **The deprecated annotation that used to turn on method security.** `@EnableGlobalMethodSecurity` (since **3.2**) registers the legacy `MethodSecurityInterceptor` stack. **`prePostEnabled` defaults to `false`**, so `@PreAuthorize` is a no-op unless you set it. Replace with **`@EnableMethodSecurity`**, where pre/post defaults to **`true`**.

## What it switched on

Put it on a `@Configuration` class (or on a subclass of `GlobalMethodSecurityConfiguration` — the annotation is still required there). Attributes:

| Attribute | Default | Enables |
|---|---|---|
| `prePostEnabled` | **`false`** | `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, `@PostFilter` |
| `securedEnabled` | `false` | `@Secured` |
| `jsr250Enabled` | `false` | `@RolesAllowed`, `@PermitAll`, `@DenyAll` |
| `mode` | `AdviceMode.PROXY` | Spring AOP proxies vs AspectJ |

It `@Import`s `GlobalMethodSecuritySelector` → `GlobalMethodSecurityConfiguration` and a `MethodSecurityMetadataSourceAdvisor` around **`MethodSecurityInterceptor`**. That is the AccessDecisionManager / voter model. `@EnableMethodSecurity` uses `AuthorizationManager` interceptors instead.

On Security **6+**, the old types live in optional **`spring-security-access`**. Keep the annotation only if you add that module; **7.1** fails fast without it. Prefer migrating.

```java
@Configuration
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class OldMethodSecurityConfig {
}
```

**Listing 1.** Conceptual — this is the functional equivalent of bare `@EnableMethodSecurity`. Forgetting `prePostEnabled = true` leaves `@PreAuthorize` decorative.

```java
@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
}

@Configuration
@EnableMethodSecurity(securedEnabled = true, prePostEnabled = false)
public class SecuredOnlyConfig {
}
```

**Listing 2.** Conceptual Security **7.1** replacements. `@EnableGlobalMethodSecurity(securedEnabled = true)` maps to the second form because the **new** annotation would otherwise also turn pre/post **on**.

```d2
direction: down
old: "@EnableGlobalMethodSecurity\nprePostEnabled default false" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
new: "@EnableMethodSecurity\nprePostEnabled default true" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
stack: "MethodSecurityInterceptor\nvoters / metadata" {
  width: 260
  height: 50
  style.fill: "#ffcdd2"
}
am: "AuthorizationManager* advisors" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}

old -> stack
new -> am
```

**Fig. 1.** Same idea — enable method AOP — two implementations. See [[What is EnableMethodSecurity]], [[What is the difference between EnableMethodSecurity and EnableGlobalMethodSecurity]], [[What happens if you mix EnableMethodSecurity and EnableGlobalMethodSecurity]], [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]].

> [!warning] Default `false` plus Boot 3
> Bare `@EnableGlobalMethodSecurity` never enabled `@PreAuthorize`. After Boot **3**, dropping this annotation without adding `@EnableMethodSecurity` is the usual silent open methods. **Do not mix** the two: they import separate interceptor families. `spring-boot-starter-security` still does **not** enable method security by itself.

> [!tip] Interview answer
> `@EnableGlobalMethodSecurity` is the old, deprecated switch for method security. `prePostEnabled` defaulted to false, so you had to set it for `@PreAuthorize`. Use `@EnableMethodSecurity` instead — pre/post is on by default — and remove the old annotation rather than stacking both.
