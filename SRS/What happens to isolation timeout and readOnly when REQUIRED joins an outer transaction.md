<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/Propagation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A participating REQUIRED method joins the outer transaction's characteristics. Local isolation, timeout, and readOnly on the inner annotation are ignored. An independent inner transaction from REQUIRES_NEW can declare its own isolation, timeout, and readOnly instead of inheriting the outer ones.
> [!warning] Unverified traps from the dump
> - Putting Isolation.SERIALIZABLE on an inner REQUIRED repository method does not raise the outer isolation.
> - readOnly=true on an inner REQUIRED join does not make the shared transaction read-only.
