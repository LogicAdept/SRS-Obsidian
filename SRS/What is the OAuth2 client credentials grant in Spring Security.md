<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is the OAuth2 client credentials grant in Spring Security?

> [!abstract] Short answer
> RFC 6749 **§4.4**: **machine-to-machine**. There is **no** resource owner in the flow. A **confidential** client **POSTs** `grant_type=client_credentials` to the **token** endpoint, authenticating with **client id/secret** (HTTP Basic in the RFC example), and gets an **access token** for **its own** scopes. Spring: **`authorization-grant-type: client_credentials`**, **`ClientCredentialsOAuth2AuthorizedClientProvider`**, **`OAuth2AuthorizedClientManager`**. It is **not** login and **not** the authorization-code grant.

## Token endpoint only — no browser redirect

RFC: the client requests resources **under its control** (or pre-arranged access). **MUST** be a **confidential** client. Steps: (A) authenticate at the token endpoint → (B) access token. **No** authorize redirect, **no** `code`, **no** user password. A **refresh token SHOULD NOT** be issued.

Spring OAuth2 Client (not Resource Server):

| Piece | Role |
| --- | --- |
| **`ClientRegistration`** with **`client_credentials`** | Needs **`token-uri`** (no authorization endpoint) |
| **`RestClientClientCredentialsTokenResponseClient`** | Token POST |
| **`ClientCredentialsOAuth2AuthorizedClientProvider`** | `OAuth2AuthorizedClientProviderBuilder.clientCredentials()` |
| **`OAuth2AuthorizedClientManager.authorize(...)`** | Returns **`OAuth2AccessToken`** to attach as outbound Bearer |

The overview’s use case is **one access token per application**. Downstream APIs still **validate** that Bearer as a resource server ([[What is the difference between an OAuth2 client and a resource server]], [[How do you secure microservices with Spring Security]]).

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          job-client:
            client-id: job-client
            client-secret: secret
            authorization-grant-type: client_credentials
            scope: read
        provider:
          job-client:
            token-uri: "{issuer}/oauth2/token"
```

**Listing 1.** No `authorization-uri` / `redirect-uri`. Contrast **`authorization_code`** on `oauth2Login()` ([[What is the OAuth2 authorization code grant in Spring Security]], [[What is OAuth 2.0]]).

```java
@Bean
OAuth2AuthorizedClientManager authorizedClientManager(
		ClientRegistrationRepository registrations,
		OAuth2AuthorizedClientRepository authorizedClients) {
	OAuth2AuthorizedClientProvider provider = OAuth2AuthorizedClientProviderBuilder.builder()
			.clientCredentials()
			.build();
	DefaultOAuth2AuthorizedClientManager manager =
			new DefaultOAuth2AuthorizedClientManager(registrations, authorizedClients);
	manager.setAuthorizedClientProvider(provider);
	return manager;
}
```

**Listing 2.** Then `OAuth2AuthorizeRequest.withClientRegistrationId("job-client").principal(...)`. `RestClient` can use **`OAuth2ClientHttpRequestInterceptor`**.

```d2
direction: down
svc: "Confidential client\n(batch / service)" {
  width: 220
  height: 48
  style.fill: "#e3f2fd"
}
as: "Authorization server\nPOST /token" {
  width: 200
  height: 48
  style.fill: "#fff3e0"
}
rs: "Resource server" {
  width: 160
  height: 36
  style.fill: "#c8e6c9"
}

svc -> as: "grant_type=client_credentials\n+ client id/secret"
as -> svc: "access_token (not a user)"
svc -> rs: "Authorization: Bearer"
```

**Fig. 1.** No user-agent. Password grant also has a user, but hands the **user’s password** to the client — a different (legacy) grant.

> [!warning] This token is not a person
> There is **no** end-user principal from the grant. Do **not** use it for “log in as Alice.” `oauth2Login()` is authorization code (OIDC). The resource server will see **client** scopes (`SCOPE_…`), not a human subject unless the authorization server puts one in the JWT by local policy.

> [!warning] Default cache is per servlet principal
> In a web app that also logs users in, Spring scopes authorized clients to **the current user name**, so each user can mint a **separate** client-credentials token. Overview: **any** request can obtain one — authorize who may call the manager. For **one token per app**, set a fixed principal (`RequestAttributePrincipalResolver` on **`OAuth2ClientHttpRequestInterceptor`**). RFC: **no public clients** (no SPA holding the secret).

> [!tip] Interview answer
> Client credentials is machine-to-machine OAuth 2.0: confidential client authenticates at the token endpoint with grant_type=client_credentials and gets a token for itself. No browser, no user, no authorization code. Spring uses a ClientRegistration plus OAuth2AuthorizedClientManager / ClientCredentialsOAuth2AuthorizedClientProvider. Do not confuse it with oauth2Login or with the password grant.
