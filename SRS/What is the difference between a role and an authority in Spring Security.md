<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring Security only stores **authorities** (`GrantedAuthority`). A **role** is a convention: an authority whose name starts with `ROLE_`.

`hasRole("ADMIN")` looks for `ROLE_ADMIN`. `hasAuthority("READ_REPORTS")` looks for that exact string.

If you store `"ADMIN"` without the prefix and then call `hasRole("ADMIN")`, the check fails.

> [!warning] Unverified traps from the dump
> - Mixing `hasRole` with authorities that were saved without `ROLE_` is a classic 403 with a “valid” login.
> - Method security SpEL uses the same `hasRole` / `hasAuthority` functions.
