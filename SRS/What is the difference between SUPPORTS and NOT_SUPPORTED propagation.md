<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

SUPPORTS participates in a current transaction and otherwise runs with none. NOT_SUPPORTED never participates: it suspends any current transaction and always runs non-transactionally. SUPPORTS is the optional-join option; NOT_SUPPORTED is the force-no-transaction option.
> [!warning] Unverified traps from the dump
> - NOT_SUPPORTED is the one that suspends; SUPPORTS does not suspend an existing transaction.
> - A read under SUPPORTS inside a REQUIRED writer still sees uncommitted work of that same transaction.
