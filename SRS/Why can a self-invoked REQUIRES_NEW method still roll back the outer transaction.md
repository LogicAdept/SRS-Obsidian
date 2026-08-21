<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: inner @Transactional(propagation = REQUIRES_NEW) is ignored on this.inner(). The inner work stays in the outer physical transaction if one exists. When the inner call fails, that shared transaction rolls back — including work the caller expected REQUIRES_NEW to commit independently (audit log, per-item refund).

The popular lie is that REQUIRES_NEW always starts a new transaction. That is only true after the call crosses a proxy (another bean or a self-injected proxy).
> [!warning] Unverified traps from the dump
> - A loop of this.placeOrder() with REQUIRES_NEW on placeOrder can roll back every item when one fails.
> - After the inner method is moved to another bean, REQUIRES_NEW can commit even if the outer transaction later rolls back.
