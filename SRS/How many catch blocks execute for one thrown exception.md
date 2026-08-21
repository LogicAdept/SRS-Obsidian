<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

At most one catch clause of that try statement. Handlers are considered in source order; the first whose type is assignment-compatible with the thrown object runs. Sibling catch blocks for the same throw are skipped.
> [!warning] Unverified traps from the dump
> - An exception thrown from inside catch is not handled by later sibling catch clauses of the same try.
> - finally still runs after that single catch, including when catch itself throws.
