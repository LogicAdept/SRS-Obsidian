<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Boot/Actuator #SRS

# How do you implement security auditing in Spring Security?

> [!abstract] Short answer
> Listen to **authentication and authorization events**, do not flip **`@EnableJpaAuditing`**. Publish **`DefaultAuthenticationEventPublisher`**, then **`@EventListener`** on **`AuthenticationSuccessEvent`** / **`AbstractAuthenticationFailureEvent`**. For HTTP denials, add **`SpringAuthorizationEventPublisher`** and listen for **`AuthorizationDeniedEvent`**. Boot Actuator stores those as **`AuditEvent`s** when you expose an **`AuditEventRepository`**.

## Security events, not entity timestamps

Spring Security fires application events for login success/failure. You subscribe with Spring’s **`@EventListener`**. That is independent of servlet **`AuthenticationSuccessHandler` / `AuthenticationFailureHandler`**.

Boot already registers a **`DefaultAuthenticationEventPublisher`**. Without Boot, declare the publisher bean yourself:

```java
@Bean
AuthenticationEventPublisher authenticationEventPublisher(
		ApplicationEventPublisher applicationEventPublisher) {
	return new DefaultAuthenticationEventPublisher(applicationEventPublisher);
}

@Component
class AuthenticationEvents {
	@EventListener
	void onSuccess(AuthenticationSuccessEvent success) {
		Authentication auth = success.getAuthentication();
		Object details = auth.getDetails();
		if (details instanceof WebAuthenticationDetails web) {
			String ip = web.getRemoteAddress(); // TCP/IP of the request
		}
	}

	@EventListener
	void onFailure(AbstractAuthenticationFailureEvent failure) {
		// failure.getException() — mapped type, not a generic Exception
	}
}
```

**Listing 1.** Conceptual listeners. **`AbstractAuthenticationEvent.getAuthentication()`** is the source. **`WebAuthenticationDetails`** records **`getRemoteAddress()`** and **`getSessionId()`** (session is not created just to fill the id).

`DefaultAuthenticationEventPublisher` maps **exact** exception classes (subclasses do **not** inherit the mapping):

| Exception | Event |
| --- | --- |
| **`BadCredentialsException`**, **`UsernameNotFoundException`**, **`InvalidBearerTokenException`** | **`AuthenticationFailureBadCredentialsEvent`** |
| **`LockedException`** | **`AuthenticationFailureLockedEvent`** |
| **`DisabledException`** | **`AuthenticationFailureDisabledEvent`** |
| **`AccountExpiredException`** | **`AuthenticationFailureExpiredEvent`** |
| **`CredentialsExpiredException`** | **`AuthenticationFailureCredentialsExpiredEvent`** |
| **`AuthenticationServiceException`** | **`AuthenticationFailureServiceExceptionEvent`** |

Extend with **`setAdditionalExceptionMappings`** or **`setDefaultAuthenticationFailureEvent`**.

Authorization: **`AuthorizationFilter`** publishes **`AuthorizationDeniedEvent`** (and can publish **`AuthorizationGrantedEvent`**, off by default — too noisy). Register **`SpringAuthorizationEventPublisher`**.

```java
@Bean
AuthorizationEventPublisher authorizationEventPublisher(
		ApplicationEventPublisher applicationEventPublisher) {
	return new SpringAuthorizationEventPublisher(applicationEventPublisher);
}
```

**Listing 2.** Deny events for access-denied auditing. Filter grants with **`setShouldPublishEvent`** if you need successes.

## Actuator `AuditEventRepository`

With Spring Security on the classpath, Actuator’s audit framework publishes **authentication success**, **failure**, and **access denied** by default. Enable persistence by declaring **`AuditEventRepository`**. **`InMemoryAuditEventRepository`** is for development; production needs your store. Customize mapping via **`AbstractAuthenticationAuditListener`** / **`AbstractAuthorizationAuditListener`**. The **`auditevents`** endpoint exposes the repository. You can also **`publishEvent(new AuditApplicationEvent(...))`** for business events.

```d2
direction: down
authn: "ProviderManager /\nfilters" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
pub: "DefaultAuthenticationEventPublisher" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
authz: "AuthorizationFilter" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
apub: "SpringAuthorizationEventPublisher" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
listen: "@EventListener /\nAuditEventRepository" {
  width: 240
  height: 50
  style.fill: "#c8e6c9"
}

authn -> pub
authz -> apub
pub -> listen
apub -> listen
```

**Fig. 1.** Login audit is **authentication events**. 403-style denials are **authorization events**. Neither is JPA **`@CreatedBy`**.

`@EnableJpaAuditing` stamps **`@CreatedBy` / `@LastModifiedBy` / `@CreatedDate` / `@LastModifiedDate`** on entities. **`AuditorAware`** may *read* **`SecurityContextHolder`** for the current principal — it still does **not** record logins ([[How do you implement auditing in Spring Data JPA]], [[What is the difference between AuthenticationException and AccessDeniedException]], [[What is AuthenticationFailureHandler]]).

> [!warning] `@EnableJpaAuditing` is not a security audit log
> Entity **createdBy / lastModified** answers “who last saved this row?” Login/lockout reporting needs **`AuthenticationSuccessEvent`**, failure events, and/or **`AuditEventRepository`**. Mixing the two is the dump’s confusion.

> [!warning] Failure events are exact-type and coarse
> **`UsernameNotFoundException`** is published as the **same** event type as bad credentials. Unmapped **`AuthenticationException`** subclasses produce **no** event unless you add mappings. **`InMemoryAuditEventRepository`** is not a production audit store. Do not enable all **`AuthorizationGrantedEvent`s** without a filter.

> [!tip] Interview answer
> Security auditing in Spring Security is application events: DefaultAuthenticationEventPublisher plus @EventListener on success and AbstractAuthenticationFailureEvent. Boot Actuator turns those into AuditEvents once you provide an AuditEventRepository. Access-denied needs SpringAuthorizationEventPublisher. EnableJpaAuditing is Spring Data entity timestamps, not a login audit trail.
