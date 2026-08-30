<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps either set a page or a handler:

```java
http.exceptionHandling().accessDeniedPage("/access-denied");
```

Or implement AccessDeniedHandler and send a custom HTML/JSON body. This runs only when the user is already authenticated but authorization failed.
> [!warning] Unverified traps from the dump
> - accessDeniedPage is not the login page. Unauthenticated users hit the AuthenticationEntryPoint instead.
