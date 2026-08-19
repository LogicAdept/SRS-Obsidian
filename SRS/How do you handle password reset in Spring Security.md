<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump steps (application logic, not a built-in filter):

1. Generate a reset token (UUID in the dump).
2. Store token+email and send it by mail.
3. On submit, verify the token.
4. Update the password with PasswordEncoder.encode.

Spring Security does not ship a reset-password endpoint in that dump.
> [!warning] Unverified traps from the dump
> - Storing a raw UUID without expiry/single-use is the dump’s incomplete recipe.
