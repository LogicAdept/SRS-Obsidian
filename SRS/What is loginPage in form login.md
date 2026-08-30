<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump custom login: formLogin().loginPage("/login") or "/custom-login".permitAll(). That URL must be reachable anonymously or the redirect loops.

The HTML form POSTs to /login by default (username and password fields). CSRF hidden field required when CSRF is on.
> [!warning] Unverified traps from the dump
> - loginPage does not always change the processing URL. Dumps forget loginProcessingUrl when the form action is not /login.
