<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps log auth events with Actuator AuditEventRepository plus an @EventListener on AbstractAuthenticationEvent (or AuthenticationSuccessEvent). On success they store principal name, event type, and remote address from WebAuthenticationDetails.

Some dumps also flip @EnableJpaAuditing — that is Spring Data entity auditing, not the same as security event audit.
> [!warning] Unverified traps from the dump
> - Mixing @EnableJpaAuditing with security AuditEvent is a dump confusion. JPA auditing is createdBy/lastModified, not login logs.
