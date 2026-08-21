<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MANDATORY joins an existing transaction and refuses to start one. If none is active, Spring throws IllegalTransactionStateException (dumps quote 'No existing transaction found for transaction marked with propagation mandatory'). Use it on helpers that must stay atomic with the caller.
> [!warning] Unverified traps from the dump
> - A dump that calls MANDATORY the opposite of REQUIRES_NEW is sloppy: NEVER is the throw-if-a-transaction-exists counterpart.
> - Calling a MANDATORY method from the same class skips the proxy, so the mandatory check never runs.
