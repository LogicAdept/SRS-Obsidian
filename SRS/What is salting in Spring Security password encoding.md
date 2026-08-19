<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Salting appends a unique random value to a password before hashing so two identical passwords hash differently and rainbow tables fail.

Dumps: Spring Security applies salting automatically since 3.1. BCrypt, PBKDF2, and Argon2 generate and store the salt inside the encoded value. You do not store a separate salt column with those encoders.
> [!warning] Unverified traps from the dump
> - MD5 or SHA-256 without a unique salt is the dump’s ‘less secure’ list.
