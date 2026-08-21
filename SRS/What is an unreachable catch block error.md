<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A compile-time error when a later catch can never run because an earlier catch already handles that type. Catch clauses are matched top-down, so a parent type must come after its subclasses. Unrelated exception types may appear in any order.
> [!warning] Unverified traps from the dump
> - This is the multiple-catch-blocks rule. Multi-catch (A | B) has a different compile error if A and B are in a parent-child relationship.
> - Only one matching catch runs for a given thrown object.
