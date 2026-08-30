<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: DelegatingPasswordEncoder reads an {id} prefix on the stored hash ({bcrypt}…, {argon2}…, {noop}…) and routes matches() to that encoder. PasswordEncoderFactories.createDelegatingPasswordEncoder() is the recommended default so you can migrate algorithms without invalidating every row.
> [!warning] Unverified traps from the dump
> - A bare BCryptPasswordEncoder cannot verify a hash produced by another scheme. The {id} prefix is the migration story.
