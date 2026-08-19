<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

AccessDecisionManager is the old voter-style final authorization decision. decide(Authentication, object, ConfigAttributes) allows the call or throws AccessDeniedException / InsufficientAuthenticationException. supports() advertises which attributes and secure-object types you handle.

Dumps register it on authorizeRequests().accessDecisionManager(...). Spring Security 6 prefers AuthorizationManager instead of this API.
> [!warning] Unverified traps from the dump
> - Writing a new AccessDecisionManager on Boot 3 is fighting the current AuthorizationFilter model.
