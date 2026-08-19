<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/OAuth2 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps enable oauth2Login() and list a client registration (Google, or a custom issuer) in YAML: client-id, client-secret, scopes, redirect-uri, authorization-grant-type authorization_code, plus provider authorization-uri / token-uri / user-info-uri (or a Spring Boot issuer-uri shortcut).

```java
http.authorizeRequests().anyRequest().authenticated().and().oauth2Login();
```

That is the OAuth2/OIDC client (login) path, not oauth2ResourceServer (validate bearer tokens).
> [!warning] Unverified traps from the dump
> - oauth2Login and oauth2ResourceServer solve different problems; many dumps conflate them with ‘OAuth2 support’.
> - Redirect URI must match the provider registration exactly, including the /login/oauth2/code/{id} path.
