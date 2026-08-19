<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Spring/Boot #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If you add spring-boot-starter-security and define no UserDetailsService, Boot uses username user and prints a generated password at startup:

```
Using generated security password: 3c2b54a6-8bc1-4e18-9f1e-02fd55a4c6b3
```

You can override with spring.security.user.name and spring.security.user.password, or replace the default user entirely with your own UserDetailsService.
> [!warning] Unverified traps from the dump
> - The generated password changes every restart unless you set it. Do not ship that default user to production.
