<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

AuthenticationSuccessHandler runs after a successful form login. Dumps use it to send USER to /welcome and ADMIN to another page instead of always SavedRequest or defaultSuccessUrl.

Wire it with formLogin().successHandler(successHandler). There is a matching AuthenticationFailureHandler for bad credentials.
> [!warning] Unverified traps from the dump
> - REST logins that return JSON should not redirect here; write 200 + body in the handler.
> - successHandler replaces the default SavedRequest-aware redirect unless you call the super handler.
