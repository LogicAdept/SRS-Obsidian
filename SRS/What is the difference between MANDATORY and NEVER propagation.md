<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

MANDATORY requires an existing transaction and throws if there is none. NEVER requires the absence of a transaction and throws if one exists. Both are guards rather than 'start a transaction' settings; neither creates a new transaction.
> [!warning] Unverified traps from the dump
> - Dumps sometimes contrast MANDATORY with REQUIRES_NEW; the throw-if-wrong-state pair is MANDATORY versus NEVER.
> - Both guards are proxy-only; a same-class call will not throw.
