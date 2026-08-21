<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use NEVER when running inside a transaction would be a configuration error, for example cache eviction that must not be tied to a database transaction that might later roll back. If a transaction is present, the method should throw rather than quietly participate.
> [!warning] Unverified traps from the dump
> - NEVER is uncommon in production code; interview dumps still expect you to name the throw-if-transaction-exists behavior.
> - NOT_SUPPORTED is the suspend-and-run alternative when you do not want an exception.
