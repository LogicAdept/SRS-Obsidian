<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `@Transactional` on a Spring bean method. Spring AOP (a transaction interceptor / advisor) starts/commits/rolls back around that join point.

Same proxy rules: public API call through the proxy; self-invocation does not start a transaction.

> [!warning] Unverified traps from the dump
> - This is Framework/AOP mechanism; transaction semantics stay on #Java/Spring/Transactions for fill-tag.
> - Do not duplicate a full @Transactional attribute card here.
