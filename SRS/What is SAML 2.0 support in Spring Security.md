<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/SAML #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: SAML 2.0 is an open standard so a user authenticates once and reaches multiple apps with the same credentials (SSO). Spring Security can integrate as a SAML 2.0 relying party / service provider.

It sits beside OAuth2/OIDC and CAS in the ‘authentication mechanisms’ lists, not as a PasswordEncoder.
> [!warning] Unverified traps from the dump
> - SAML is not JWT resource-server config. Dumps that mix saml2Login with oauth2ResourceServer().jwt() are naming two different protocols.
