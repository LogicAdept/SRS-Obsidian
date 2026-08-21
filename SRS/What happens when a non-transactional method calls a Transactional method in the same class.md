<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: if the caller has no @Transactional and it self-invokes a @Transactional method, no Spring transaction starts. The inner annotation is ignored, so a loop of this.processItem() does not get a per-item transaction or a unit-of-work rollback.

Contrast in the same dump: calling a non-transactional helper from an already-proxied @Transactional method still runs inside the outer interceptor, because you never left the proxy on the way in.
> [!warning] Unverified traps from the dump
> - Repository save without a surrounding Spring transaction may auto-commit statement by statement, so a later exception does not undo earlier writes.
> - The same processItem method starts a real transaction when another bean calls it through the proxy.
