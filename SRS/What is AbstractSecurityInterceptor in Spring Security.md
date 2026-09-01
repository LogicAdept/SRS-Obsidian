<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/MethodSecurity #SRS

# What is `AbstractSecurityInterceptor` in Spring Security?

> [!abstract] Short answer
> The **deprecated** parent of the old authorization interceptors. Subclasses present a **secure object** (`FilterInvocation`, `MethodInvocation`, …). The parent reads **`Authentication`** from **`SecurityContextHolder`**, loads **`ConfigAttribute`s** from a **`SecurityMetadataSource`**, and calls **`AccessDecisionManager.decide`**. Deny is **`AccessDeniedException`**. Replacements: **`AuthorizationFilter`** (HTTP), **`AuthorizationManagerBeforeMethodInterceptor` / `After`** (methods), **`AuthorizationChannelInterceptor`** (messaging).

## Shared before / proceed / after template

It is **authorization**, not a login filter. Subclasses implement **`getSecureObjectClass()`** and **`obtainSecurityMetadataSource()`**. The parent runs:

1. **`beforeInvocation(secureObject)`** — attributes from the metadata source.
2. Empty attributes → **public** (return, unless **`rejectPublicInvocations`**).
3. No `Authentication` on the holder → **`AuthenticationCredentialsNotFoundException`**.
4. If **`isAuthenticated() == false`** or **`alwaysReauthenticate`**, call **`AuthenticationManager`** and put the result back on the holder.
5. **`accessDecisionManager.decide(authentication, secureObject, attributes)`**.
6. Optional **`RunAsManager`** swap.
7. Subclass **proceeds**.
8. **`finallyInvocation`** restores the holder; **`afterInvocation`** may run **`AfterInvocationManager`** (post-filter / post-authorize in the old model).

Concrete dumps name two children. Javadoc also lists **`ChannelSecurityInterceptor`**:

| Subclass | Secure object | Today |
| --- | --- | --- |
| **`FilterSecurityInterceptor`** | HTTP **`FilterInvocation`** | **`AuthorizationFilter`** (`authorizeHttpRequests`) |
| **`MethodSecurityInterceptor`** | AOP **`MethodInvocation`** | **`AuthorizationManagerBeforeMethodInterceptor`** / **`After`** (`@EnableMethodSecurity`) |
| **`ChannelSecurityInterceptor`** | messaging | **`AuthorizationChannelInterceptor`** |

```java
Collection<ConfigAttribute> attributes = metadataSource.getAttributes(secureObject);
if (attributes == null || attributes.isEmpty()) {
	return; // public invocation
}
Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
accessDecisionManager.decide(authentication, secureObject, attributes);
```

**Listing 1.** The decision the dumps mean — parent template around that `decide` call. Real code also re-authenticates and run-as ([[What is FilterSecurityInterceptor]], [[What is MethodSecurityInterceptor]], [[How do you implement a custom AccessDecisionManager]]).

```d2
direction: down
asi: "AbstractSecurityInterceptor\n(deprecated)" {
  width: 260
  height: 44
  style.fill: "#fff3e0"
}
fsi: "FilterSecurityInterceptor" {
  width: 210
  height: 36
  style.fill: "#ffe0b2"
}
msi: "MethodSecurityInterceptor" {
  width: 220
  height: 36
  style.fill: "#ffe0b2"
}
adm: "AccessDecisionManager\nvoters" {
  width: 200
  height: 40
  style.fill: "#ffcdd2"
}
af: "AuthorizationFilter" {
  width: 180
  height: 36
  style.fill: "#c8e6c9"
}
ami: "AuthorizationManager\nmethod interceptors" {
  width: 220
  height: 40
  style.fill: "#c8e6c9"
}

asi -> fsi
asi -> msi
fsi -> adm
msi -> adm
fsi -> af: "replaced by" {
  style.stroke: "#2e7d32"
}
msi -> ami: "replaced by" {
  style.stroke: "#2e7d32"
}
```

**Fig. 1.** One deprecated template, two dump types, one voter API. Security 6+ HTTP DSL never installs this class ([[What is the difference between AuthorizationFilter and FilterSecurityInterceptor]], [[What is AuthorizationFilter in Spring Security]], [[What is AuthorizationManager in method security]], [[What is SecurityContextHolder]]).

On Security **7** the Access API lives in **`spring-security-access`**. Default Boot 3 / Security 6 chains show **`AuthorizationFilter`**, not **`FilterSecurityInterceptor`**. Servlet **`ExceptionTranslationFilter`** still turns thrown **`AuthenticationException` / `AccessDeniedException`** into 401/403.

> [!warning] Authorization, with a login-shaped footgun
> It does **not** collect a username. It **does** call **`AuthenticationManager`** when the current `Authentication` is unauthenticated or **`alwaysReauthenticate`** is set. A **null** holder is **`AuthenticationCredentialsNotFoundException`**, not “anonymous”. Anonymous is a real `Authentication` from **`AnonymousAuthenticationFilter`**, earlier in the chain.

> [!warning] Empty metadata is public
> No `ConfigAttribute`s → the interceptor **allows** the call. **`rejectPublicInvocations=true`** fails closed. That is the old “undeclared URL is open” trap; **`AuthorizationFilter`** with no matching `requestMatchers` **denies**.

> [!tip] Interview answer
> AbstractSecurityInterceptor is the old shared authorization engine: SecurityContextHolder, SecurityMetadataSource, AccessDecisionManager, then AccessDeniedException. FilterSecurityInterceptor did HTTP; MethodSecurityInterceptor did methods. It is deprecated. Use AuthorizationFilter and AuthorizationManager interceptors instead.
