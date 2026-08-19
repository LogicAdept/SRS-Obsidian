<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump architecture: after AbstractAuthenticationProcessingFilter succeeds or fails, it calls RememberMeServices.loginSuccess / loginFail. RememberMeAuthenticationFilter later turns the cookie into an Authentication. Implementations: token-based (hash) vs persistent tokens in a DB.
> [!warning] Unverified traps from the dump
> - If remember-me is not configured this is a no-op, not an extra filter error.
