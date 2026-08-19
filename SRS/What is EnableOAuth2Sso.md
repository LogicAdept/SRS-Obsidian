<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Older Boot dumps: @EnableOAuth2Sso on a WebSecurityConfigurerAdapter turns the app into an OAuth2 SSO client (redirect to the auth server, then a local session).

Paired in the same dumps with @EnableResourceServer on the API. Current dumps replace this with oauth2Login() and oauth2ResourceServer().
> [!warning] Unverified traps from the dump
> - @EnableOAuth2Sso is from the deprecated spring-security-oauth2 / Boot autoconfigure line, not Spring Security 6’s oauth2Login.
