<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

NOT_SUPPORTED always runs non-transactionally. If a transaction is active, Spring suspends it for the method and resumes it afterward. Dumps recommend it for in-memory work or a slow external call so the outer transaction does not hold a database connection during the wait.
> [!warning] Unverified traps from the dump
> - Suspension still needs a transaction manager that can suspend; otherwise the setting may not do what the name suggests.
> - Work done under NOT_SUPPORTED is not rolled back if the resumed outer transaction fails.
