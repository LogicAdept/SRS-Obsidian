<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: do not store plain-text passwords. Hashing is a one-way transform (MD4/MD5/SHA in old lists; BCrypt/PBKDF2/Argon2 as PasswordEncoder). Store the hash; at login re-hash the input and compare.

That is PasswordEncoder.encode / matches, not reversible encryption.
> [!warning] Unverified traps from the dump
> - MD5/SHA-1 in dump algorithm lists are not acceptable PasswordEncoder choices for new apps.
