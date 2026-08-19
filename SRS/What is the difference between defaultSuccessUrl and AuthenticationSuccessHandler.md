<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: defaultSuccessUrl("/home") is the built-in redirect after login when there is no SavedRequest. AuthenticationSuccessHandler is the strategy interface — dumps use it to send ADMIN vs USER to different pages. Wiring successHandler replaces the default SavedRequest-aware redirect unless you delegate to it.
> [!warning] Unverified traps from the dump
> - REST logins should not use either redirect; write 200 + body in the handler.
