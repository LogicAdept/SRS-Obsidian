<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

REQUIRED is the default. If a transaction already exists on the thread, the method joins it; otherwise Spring starts a new one. Nested REQUIRED methods share one physical transaction, so a rollback-only mark from an inner method dooms the whole unit of work.
> [!warning] Unverified traps from the dump
> - Catching an inner RuntimeException does not clear rollback-only; the outer commit still fails.
> - Self-invocation never applies REQUIRED on the inner method because the proxy is skipped.
