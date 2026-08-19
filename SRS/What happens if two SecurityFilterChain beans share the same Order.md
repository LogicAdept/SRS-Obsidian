<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: undefined — Spring does not guarantee ordering for same-priority beans. Always use distinct @Order values. (Missing @Order entirely is a different failure: both default to the same unordered bucket.)
> [!warning] Unverified traps from the dump
> - Same @Order is not a compile error. You only see the wrong chain win in production.
