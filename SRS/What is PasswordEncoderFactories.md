<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: PasswordEncoderFactories.createDelegatingPasswordEncoder() returns the factory DelegatingPasswordEncoder: new encodes use the default id (bcrypt in dumps), old hashes still verify via their prefix.
> [!warning] Unverified traps from the dump
> - User.withDefaultPasswordEncoder() is not this factory. Dumps mark withDefaultPasswordEncoder as demo-only and unsafe.
