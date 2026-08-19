<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pbkdf2PasswordEncoder is a dump PasswordEncoder alongside BCrypt and Argon2. PBKDF2 is a slow, salted KDF. Spring Security’s implementation encodes for matches() like the others.

DelegatingPasswordEncoder understands an {pbkdf2} id prefix for mixed hashes.
> [!warning] Unverified traps from the dump
> - Work factor / iterations must be high enough; dumps still prefer BCrypt or Argon2 for new apps.
