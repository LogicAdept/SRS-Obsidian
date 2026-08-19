<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/JWT #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: JwtAccessTokenConverter (old spring-security-oauth2) converts between JWT-encoded OAuth2 access tokens and OAuth2Authentication. convertAccessToken encodes; extractAuthentication reads claims. You set a signing key on the converter.

This is the legacy authorization-server/resource-server token enhancer, not the Spring Security 5.2+ JwtDecoder / Nimbus path.
> [!warning] Unverified traps from the dump
> - spring-security-oauth2 is end-of-life. Current dumps use oauth2ResourceServer().jwt() and JwtDecoder instead.
