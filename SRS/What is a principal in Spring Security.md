<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A principal is the entity performing an action — a user, device, or system (the “who”). Credentials (password, token) prove that principal. The secured resource is the “what”.

After login the principal sits on the Authentication in the SecurityContext. authentication.getPrincipal() typically returns a UserDetails. Dumps also call the logged-in user “the principal” and read it via SecurityContextHolder.
> [!warning] Unverified traps from the dump
> - Anonymous requests still have an Authentication whose principal is not your UserDetails (often a string anonymousUser).
