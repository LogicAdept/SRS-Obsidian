<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: in @PreFilter / @PostFilter the default SpEL name for the element being kept or dropped is filterObject (maps use filterObject for values). Example dump: filterObject.owner == authentication.name.
> [!warning] Unverified traps from the dump
> - filterObject is not returnObject. returnObject is @PostAuthorize on the whole return value.
