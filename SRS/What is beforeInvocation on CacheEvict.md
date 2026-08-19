<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`beforeInvocation = true` evicts before the method body. Dumps present it as automated eviction so the entry is gone even if the method fails.

> [!warning] Unverified traps from the dump
> - Evicting before a failed delete can drop a cache entry while the row still exists.

