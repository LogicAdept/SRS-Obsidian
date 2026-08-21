<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

REQUIRED joins or creates one shared physical transaction: an inner rollback rolls back the caller too. REQUIRES_NEW suspends the outer transaction and starts a second physical one that can commit even if the outer later rolls back. Reach for REQUIRES_NEW when the inner work must survive, for example an audit log.
> [!warning] Unverified traps from the dump
> - Two REQUIRED methods in one class still share the outer transaction because this.inner() skips the proxy.
> - REQUIRES_NEW is not a savepoint; it takes a second connection and can deadlock on rows the outer transaction still locks.
