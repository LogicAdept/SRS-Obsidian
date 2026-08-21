<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

REQUIRES_NEW always opens an independent physical transaction. Any outer transaction is suspended until the inner method returns. Inner commit or rollback does not follow the outer outcome, so work such as an audit row can persist after the caller rolls back.
> [!warning] Unverified traps from the dump
> - Inner REQUIRES_NEW is ignored on this.inner() because the call never hits the proxy.
> - The suspended outer transaction keeps its connection while the inner one takes another.
