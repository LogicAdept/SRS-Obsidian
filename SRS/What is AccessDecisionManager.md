<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/MethodSecurity #SRS

# What is `AccessDecisionManager`?

> [!abstract] Short answer
> The **legacy authorization engine**: **`AbstractSecurityInterceptor`** calls **`decide(Authentication, secureObject, ConfigAttribute[])`**. **Return** = allow. **Throw `AccessDeniedException`** (or **`InsufficientAuthenticationException`**) = deny. Stock implementations are **voter aggregators**: **`AffirmativeBased`**, **`ConsensusBased`**, **`UnanimousBased`**. **`AuthorizationManager` supersedes it.** HTTP today is **`AuthorizationFilter`**, not **`FilterSecurityInterceptor`**.

## Final yes/no for the old interceptor

Architecture still documents this under **legacy** components. The interceptor already loaded **`ConfigAttribute`s** from a **`SecurityMetadataSource`**. The manager only answers whether **this `Authentication`** may invoke **this secure object** (`FilterInvocation`, `MethodInvocation`, …).

```java
void decide(Authentication authentication, Object object,
		Collection<ConfigAttribute> configAttributes)
		throws AccessDeniedException, InsufficientAuthenticationException;

boolean supports(ConfigAttribute attribute);

boolean supports(Class<?> clazz);
```

**Listing 1.** Contract (Javadoc `@Deprecated`). **`supports(ConfigAttribute)`** is checked at interceptor **startup**. **`supports(Class)`** must match the interceptor’s secure-object type. There is **no boolean** return ([[What is AbstractSecurityInterceptor in Spring Security]], [[How do you implement a custom AccessDecisionManager]]).

Voters return **`ACCESS_GRANTED` / `ACCESS_DENIED` / `ACCESS_ABSTAIN`**. The three shipped managers tally those votes:

| Manager | Grants when |
| --- | --- |
| **`AffirmativeBased`** | ≥1 **GRANT** — a **DENY** is ignored if any **GRANT** exists |
| **`ConsensusBased`** | Majority of **non-abstain** votes (tie / all-abstain are properties) |
| **`UnanimousBased`** | Every non-abstain vote is **GRANT**; any **DENY** denies |

All three honor **`allowIfAllAbstainDecisions`** (usually **false** → deny if everyone abstains). Common voters: **`RoleVoter`** (`ROLE_*` attributes vs `GrantedAuthority`), **`AuthenticatedVoter`** (`IS_AUTHENTICATED_*`).

```d2
direction: down
asi: "AbstractSecurityInterceptor" {
  width: 230
  height: 36
  style.fill: "#fff3e0"
}
adm: "AccessDecisionManager" {
  width: 200
  height: 36
  style.fill: "#ffcdd2"
}
v1: "RoleVoter" {
  width: 120
  height: 32
  style.fill: "#ffe0b2"
}
v2: "AuthenticatedVoter" {
  width: 160
  height: 32
  style.fill: "#ffe0b2"
}
am: "AuthorizationManager" {
  width: 200
  height: 36
  style.fill: "#c8e6c9"
}

asi -> adm
adm -> v1
adm -> v2
adm -> am: "superseded by" {
  style.stroke: "#2e7d32"
}
```

**Fig. 1.** Voter era vs **`AuthorizationManager`** (`check` / `verify`, no `ConfigAttribute` list). HTTP: **`authorizeHttpRequests`** → **`AuthorizationFilter`**. Methods: **`@EnableMethodSecurity`** interceptors ([[What is FilterSecurityInterceptor]], [[What is the difference between AuthorizationFilter and FilterSecurityInterceptor]], [[What is AuthorizationManager in method security]]).

On Security **7**, `AccessDecisionManager`, voters, and friends live in **`spring-security-access`**. Adding that module is a **migration** step, not the current default.

> [!warning] `AffirmativeBased` is not unanimous
> One **GRANT** wins even if another voter **DENIED**. Dumps that name the three aggregators are describing this tally, not `AuthorizationManager`. All-abstain with the default flag is **deny**.

> [!warning] Do not wire this on Security 6+ HTTP DSL
> `authorizeRequests().accessDecisionManager(...)` is the **old** chain. **`authorizeHttpRequests().access(AuthorizationManager)`** is the replacement. A custom **`AccessDecisionManager`** does not run on **`AuthorizationFilter`**.

> [!tip] Interview answer
> AccessDecisionManager is the old final authorization API: AbstractSecurityInterceptor calls decide; return allows, AccessDeniedException denies. AffirmativeBased, ConsensusBased, and UnanimousBased combine AccessDecisionVoter votes. AuthorizationManager replaced it; AuthorizationFilter is the servlet filter.
