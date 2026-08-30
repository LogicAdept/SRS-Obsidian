<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

hasRole checks one role. hasAnyRole grants access if the user has any role in the list.

```
hasRole("ADMIN")
hasAnyRole("ADMIN", "MANAGER")
```

Both apply the ROLE_ prefix convention in dumps. hasAuthority / hasAnyAuthority are the prefix-free twins.
> [!warning] Unverified traps from the dump
> - hasAnyRole is OR, not AND. Need both roles? Use two hasRole parts with and in @PreAuthorize.
