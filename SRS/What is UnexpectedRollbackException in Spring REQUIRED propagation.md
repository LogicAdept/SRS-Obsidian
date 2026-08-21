<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

With REQUIRED, an inner logical scope can mark the shared physical transaction rollback-only. If the outer method catches the exception and still tries to commit, Spring throws UnexpectedRollbackException so the caller is not told that a commit succeeded when the transaction was rolled back.
> [!warning] Unverified traps from the dump
> - This is REQUIRED sharing one physical transaction, not REQUIRES_NEW.
> - setRollbackOnly without rethrowing produces the same surprise at outer commit.
