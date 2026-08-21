<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use NESTED when a sub-step should be undoable on its own (one bad batch item, a failing validation) without aborting the outer unit of work, while still committing only with the outer transaction. Prefer it over REQUIRES_NEW when you want one connection and you accept that outer rollback undoes the nested work.
> [!warning] Unverified traps from the dump
> - Do not pick NESTED when the inner row must remain if the outer business operation fails; that is REQUIRES_NEW.
> - Confirm the transaction manager actually implements savepoints before relying on partial rollback.
