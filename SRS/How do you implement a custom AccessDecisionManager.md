<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/MethodSecurity #SRS

# How do you implement a custom AccessDecisionManager?

> [!abstract] Short answer
> **`AccessDecisionManager` is deprecated** — implement **`AuthorizationManager`** instead. If you still write one, implement **`decide`**, **`supports(ConfigAttribute)`**, and **`supports(Class)`**: **`decide`** either returns (grant) or throws **`AccessDeniedException`** / **`InsufficientAuthenticationException`**. Do **not** hang a new manager on **`authorizeRequests().accessDecisionManager(...)`** on Boot 3 / Security 6+: that DSL drives **`FilterSecurityInterceptor`**. Use **`authorizeHttpRequests`** and **`.access(AuthorizationManager)`**.

## What `decide` actually does

`AccessDecisionManager` is called by **`AbstractSecurityInterceptor`** (web **`FilterSecurityInterceptor`**, method **`MethodSecurityInterceptor`**). It makes the **final** pre-invocation yes/no. Javadoc (7.1, `@Deprecated`, “Use AuthorizationManager instead”):

```java
void decide(Authentication authentication, Object object,
		Collection<ConfigAttribute> configAttributes)
		throws AccessDeniedException, InsufficientAuthenticationException;

boolean supports(ConfigAttribute attribute);

boolean supports(Class<?> clazz);
```

**Listing 1.** Contract. **`object`** is the secure object (`FilterInvocation`, `MethodInvocation`, …). **`supports(ConfigAttribute)`** is checked at startup so every configured attribute can be consumed. **`supports(Class)`** must match the interceptor’s secure-object type.

Grant = **return**. Deny = **throw**. There is no boolean result.

Stock managers tally **`AccessDecisionVoter`** votes (`ACCESS_GRANTED` / `ACCESS_DENIED` / `ACCESS_ABSTAIN`):

| Manager | Grant when |
| --- | --- |
| **`AffirmativeBased`** | ≥1 **GRANT** (a **DENY** is ignored if any **GRANT** exists) |
| **`ConsensusBased`** | Majority of non-abstain votes (tie / all-abstain are properties) |
| **`UnanimousBased`** | All non-abstain votes are **GRANT**; any **DENY** denies |

All three have **`allowIfAllAbstainDecisions`** (typically **false** → deny if everyone abstains). Architecture also allows a **custom tally** (weighted votes, veto **DENY**). Prefer a **custom `AccessDecisionVoter`** plus **`AffirmativeBased`** over rewriting the manager unless you need that tally.

```java
public final class CustomerAccessDecisionManager implements AccessDecisionManager {

	@Override
	public void decide(Authentication authentication, Object object,
			Collection<ConfigAttribute> configAttributes) {
		if (!authentication.isAuthenticated()) {
			throw new InsufficientAuthenticationException("Not authenticated");
		}
		// inspect MethodInvocation arguments, ConfigAttributes, authorities…
		throw new AccessDeniedException("Denied");
	}

	@Override
	public boolean supports(ConfigAttribute attribute) {
		return true; // or only attributes you understand
	}

	@Override
	public boolean supports(Class<?> clazz) {
		return MethodInvocation.class.isAssignableFrom(clazz);
	}
}
```

**Listing 2.** Conceptual custom manager. On Security **7**, this type lives in **`spring-security-access`**. Wire it only into a leftover **`AbstractSecurityInterceptor`**. The dump’s **`authorizeRequests().accessDecisionManager(...)`** is that old HTTP path — **`authorizeHttpRequests` does not take an `AccessDecisionManager`**.

## Current replacement

`AuthorizationManager` **supersedes** both **`AccessDecisionManager`** and **`AccessDecisionVoter`**. **`authorize`** returns a positive/negative **`AuthorizationDecision`**, or **`null`** to abstain. **`verify`** throws **`AccessDeniedException`** on deny. HTTP: **`AuthorizationFilter`** + **`authorizeHttpRequests`**. Method security: **`AuthorizationManagerBeforeMethodInterceptor`**.

```java
http
	.authorizeHttpRequests((authorize) -> authorize
		.requestMatchers("/admin/**").access(new CustomerAuthorizationManager())
		.anyRequest().authenticated());
```

**Listing 3.** Current HTTP hook. For a leftover ADM, wrap it with the documented **`AccessDecisionManagerAuthorizationManagerAdapter`** (call **`decide`**, map grant/deny to **`AuthorizationDecision`**) and pass **that** to **`.access(...)`** — do not re-enable **`authorizeRequests`**.

```d2
direction: down
old: "authorizeRequests +\nAccessDecisionManager" {
  width: 240
  height: 55
  style.fill: "#fce4ec"
}
fsi: "FilterSecurityInterceptor" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
neu: "authorizeHttpRequests +\nAuthorizationManager" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
af: "AuthorizationFilter" {
  width: 220
  height: 40
  style.fill: "#c8e6c9"
}

old -> fsi
neu -> af
```

**Fig. 1.** Security 6+ HTTP authorization is **`AuthorizationFilter`**, not a custom ADM on **`FilterSecurityInterceptor`** ([[What is the difference between AuthorizationFilter and FilterSecurityInterceptor]], [[What is AuthorizationManager in method security]], [[What is AccessDecisionManager]]).

> [!warning] A new AccessDecisionManager on Boot 3 fights AuthorizationFilter
> Boot 3 ships Spring Security 6. **`authorizeHttpRequests`** installs **`AuthorizationFilter`** and the **`AuthorizationManager`** API. **`authorizeRequests().accessDecisionManager(...)`** keeps **`FilterSecurityInterceptor`**, config attributes, and voters — the migration guide’s *not* recommended path. Implement **`AuthorizationManager`** (or adapt an old ADM). From Security **7**, you also need **`spring-security-access`** just to compile the legacy types.

> [!warning] `decide` is throw-to-deny
> Returning **`false`** does nothing; the interceptor treats a normal return as **grant**. Empty **`ConfigAttribute`** lists make every voter **abstain**, and with **`allowIfAllAbstainDecisions = false`** that is **deny**. **`InsufficientAuthenticationException`** is for **trust** (anonymous / remember-me), not missing roles — those are **`AccessDeniedException`**.

> [!tip] Interview answer
> AccessDecisionManager is the old final voter coordinator: decide either returns or throws AccessDeniedException. Spring Security 6 replaced it with AuthorizationManager on AuthorizationFilter — implement that, and register it with authorizeHttpRequests, not authorizeRequests. If you must keep an old manager, wrap it in the adapter the architecture docs show and put it on .access. On Security 7 the Access API is a separate spring-security-access module.
