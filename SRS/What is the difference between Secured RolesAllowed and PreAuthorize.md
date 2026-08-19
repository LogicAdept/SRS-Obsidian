<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

All three secure methods via AOP. `@Secured` (Spring) and `@RolesAllowed` (JSR-250) only check roles/authorities. `@PreAuthorize` takes SpEL, so it can use method arguments (`#userId`), `and`/`or`, and `authentication`.

`@EnableMethodSecurity` (Security 6) replaces `@EnableGlobalMethodSecurity` and turns **pre/post** annotations on by default. Set `jsr250Enabled` / `securedEnabled` for the other two.

SpEL also appears on `@PostAuthorize`, `@PreFilter`, `@PostFilter`. `@Secured` and `@RolesAllowed` cannot use SpEL.

> [!warning] Unverified traps from the dump
> - After a Boot 3 upgrade, `@PreAuthorize` “stops working” if you still expect the old annotation and forgot `@EnableMethodSecurity`.
> - Self-invocation skips the method-security proxy, same as `@Transactional`.
