<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

FAQ dump: **nothing happens.** `equals()` is **ignored**. Only reference equality matters.

> [!warning] Unverified traps from the dump
> - Overriding `hashCode` is ignored the same way in the hashCode dumps (`identityHashCode` instead).
> - Two `equals` instances are still two keys if they are not `==`.
