<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps configure logout on HttpSecurity:

```java
http.logout()
    .logoutUrl("/logout")
    .logoutSuccessUrl("/login?logout")
    .permitAll();
```

Default is POST /logout (CSRF applies). Success typically invalidates the session, clears the SecurityContext, and redirects. You can also set a LogoutSuccessHandler or delete cookies (remember-me).
> [!warning] Unverified traps from the dump
> - GET /logout is not the default in modern Spring Security; CSRF-protected POST is.
> - A stateless JWT API usually has no server session to invalidate; logout is token revocation or client-side discard.
