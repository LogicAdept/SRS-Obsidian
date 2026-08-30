<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

NoOpPasswordEncoder stores and compares passwords as plain text. Dumps mark it for tests only. {noop} in DelegatingPasswordEncoder is the same idea for a single hash.

Boot’s generated password and {noop}password in in-memory samples are this class of encoder.
> [!warning] Unverified traps from the dump
> - Leaving {noop} in production dumps is the classic interview fail.
