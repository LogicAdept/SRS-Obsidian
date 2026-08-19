<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/Keycloak #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Keycloak is an open-source IAM (login, SSO, federation). Dumps integrate it as OAuth2/OIDC so the app does not store passwords.

Older dump recipe: keycloak-spring-security-adapter, @KeycloakConfiguration extending KeycloakWebSecurityConfigurerAdapter, keycloakAuthenticationProvider(), RegisterSessionAuthenticationStrategy, then hasRole rules.

Newer dumps instead use spring-boot-starter-oauth2-client / oauth2-resource-server against Keycloak’s issuer-uri — same idea as any OIDC provider.
> [!warning] Unverified traps from the dump
> - The KeycloakWebSecurityConfigurerAdapter adapter is the old dump. Boot 3 / Security 6 interviews expect oauth2Login or oauth2ResourceServer plus issuer-uri.
