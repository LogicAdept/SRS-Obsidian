<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use MANDATORY on an internal helper that must run in the caller's transaction and should fail loudly if invoked with no transaction, for example writing an outbox row or a critical audit that must stay atomic with the business update.
> [!warning] Unverified traps from the dump
> - MANDATORY does not start a transaction for a forgotten @Transactional on the facade; it only throws.
> - A same-class call will not enforce the mandatory rule.
