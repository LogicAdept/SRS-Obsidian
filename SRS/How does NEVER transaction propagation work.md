<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

NEVER requires that no transaction be active. The method runs non-transactionally; if a transaction already exists, Spring throws IllegalTransactionStateException. Dumps treat this as a rare guard for code that must not see a transactional resource.
> [!warning] Unverified traps from the dump
> - Self-invocation from a REQUIRED method never triggers NEVER, so the expected exception does not appear.
> - Most projects never use NEVER; NOT_SUPPORTED suspends instead of throwing.
