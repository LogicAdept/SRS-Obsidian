<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: returnObject is the whole return value in @PostAuthorize. filterObject is each element (or map value) in @PreFilter / @PostFilter. Mixing them is a common SpEL typo.
> [!warning] Unverified traps from the dump
> - @PostAuthorize("filterObject.owner == …") does nothing useful — filterObject is not defined there.
