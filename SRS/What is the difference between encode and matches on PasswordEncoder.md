<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: encode(raw) hashes for storage (salt inside the string for BCrypt/Argon2/PBKDF2). matches(raw, encoded) re-hashes the presented password and compares — it does not decrypt.
> [!warning] Unverified traps from the dump
> - Calling encode again and comparing strings yourself breaks because a new salt makes a new hash. Always matches().
