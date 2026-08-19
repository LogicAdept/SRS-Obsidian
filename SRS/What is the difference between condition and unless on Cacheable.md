<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`condition` runs before the method: if false, the cache is not consulted and the result is not stored. It cannot use `#result`. `unless` runs after the method: if true, the result is not stored. It can use `#result` (example `unless = "#result == null"`).

Use `condition` to filter on inputs (`#id > 0`); `unless` to filter on the return value.

> [!warning] Unverified traps from the dump
> - Swapping them is a common dump trap: `#result` in `condition` is not available.

