<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use NOT_SUPPORTED to force work off the current transaction: a slow HTTP notification, in-memory processing, or anything that should not hold the database connection. The outer transaction is suspended for the call and resumed after.
> [!warning] Unverified traps from the dump
> - The outer connection is still allocated while suspended; this avoids timeout from a slow call more than it frees the pool slot.
> - If the external side effect must be atomic with the database write, NOT_SUPPORTED is the wrong tool.
