<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use SUPPORTS for work that should join a caller transaction when one exists but is valid without starting its own, typically read or report methods. Called from REQUIRED, it sees that unit of work; called alone, it runs with no transaction.
> [!warning] Unverified traps from the dump
> - Do not use SUPPORTS for a multi-statement write that must roll back as one unit when invoked with no outer transaction.
> - Reads under SUPPORTS inside a writer still participate in that writer's uncommitted changes.
