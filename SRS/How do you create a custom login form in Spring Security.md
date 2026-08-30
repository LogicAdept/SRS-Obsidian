<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps keep form login but point it at your page:

```java
http.authorizeRequests().anyRequest().authenticated()
    .and()
    .formLogin().loginPage("/login").permitAll();
```

The page POSTs username and password to /login (unless you change loginProcessingUrl). Include the CSRF hidden field on browser forms. permitAll() on the login page is required or the redirect loops.
> [!warning] Unverified traps from the dump
> - The login page itself must be permitAll; otherwise unauthenticated users cannot see it.
> - POST /login needs a CSRF token when CSRF is on (the default for cookie sessions).
