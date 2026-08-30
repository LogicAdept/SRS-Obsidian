<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps add a second factor after password: custom filter before UsernamePasswordAuthenticationFilter, or a /verify-otp endpoint that checks TOTP/SMS (Google Authenticator / Twilio in the dump) before completing authentication.

Typical flow: username+password succeeds but Authentication is not fully privileged until OTP validates; then you replace the Authentication in the SecurityContext.
> [!warning] Unverified traps from the dump
> - A filter that always chain.doFilter without checking OTP is not 2FA.
> - Spring Security has no built-in TOTP switch in the dumps; you write the extra step.
