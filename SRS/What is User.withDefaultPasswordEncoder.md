<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/PasswordEncoder #Security/Cryptography #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump samples (especially WebFlux MapReactiveUserDetailsService) build users with User.withDefaultPasswordEncoder().username(...).password(...).roles(...).

Dumps treat it as a shortcut that encodes with a default encoder so you can type a raw password in code. They also mark it not for production.
> [!warning] Unverified traps from the dump
> - The encoder is visible in the binary / easy to recover. Use PasswordEncoder.encode and a real UserDetailsService.
