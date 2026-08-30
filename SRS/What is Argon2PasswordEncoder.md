<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Argon2PasswordEncoder is a dump-recommended modern PasswordEncoder (with BCrypt and PBKDF2). Argon2 is a memory-hard hash; the encoder generates salt like the others.

DelegatingPasswordEncoder can verify {argon2}… prefixes while still encoding new passwords as bcrypt, which is the migration story.
> [!warning] Unverified traps from the dump
> - Switching the default id in DelegatingPasswordEncoder does not rewrite old {bcrypt} rows; it only changes newly encoded passwords.
