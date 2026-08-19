<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps list:

- BCryptPasswordEncoder — usual default, adaptive, salted.
- Pbkdf2PasswordEncoder
- Argon2PasswordEncoder
- NoOpPasswordEncoder — testing only (plain text).
- DelegatingPasswordEncoder — {id} prefix, recommended factory default.

PasswordEncoder.encode hashes; matches(raw, encoded) re-hashes and compares.
> [!warning] Unverified traps from the dump
> - MD5/SHA-1 in dump ‘less secure’ lists are not the modern PasswordEncoder beans.
