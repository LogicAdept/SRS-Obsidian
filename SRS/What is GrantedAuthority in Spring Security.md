<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

GrantedAuthority is an authority granted to an Authentication: a role or a permission. Implementations expose getAuthority() as a string (for example ROLE_ADMIN or a custom permission name).

UserDetails.getAuthorities() returns a collection of GrantedAuthority. Authorization rules such as hasAuthority and hasRole compare against those strings.
> [!warning] Unverified traps from the dump
> - hasRole("ADMIN") typically implies a ROLE_ prefix; hasAuthority expects the full string such as ROLE_ADMIN.
