<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/OIDC #SRS

# How do you register a custom OAuth2 identity provider?

> [!abstract] Short answer
> Add a **`ClientRegistration`** that is **not** one of **`CommonOAuth2Provider`** (Google, GitHub, Facebook, X, Okta). In Boot, that is `spring.security.oauth2.client.registration.{id}` plus **`provider.{id}`** endpoints (or **`issuer-uri`** for OIDC discovery), then **`oauth2Login()`**. Without Boot, **`ClientRegistration.withRegistrationId(...)`** in an **`InMemoryClientRegistrationRepository`**.

## Registration + provider, not a Google enum

`CommonOAuth2Provider` only pre-fills **authorization / token / user-info** URIs when the **`registrationId`** (or **`provider`**) matches **`google`**, **`github`**, **`facebook`**, **`x`**, or **`okta`**. A private IdP needs those URIs (or discovery) spelled out.

Boot maps:

| Property | `ClientRegistration` |
| --- | --- |
| `registration.[id].client-id` / `client-secret` | `clientId` / `clientSecret` |
| `registration.[id].authorization-grant-type` | `authorizationGrantType` (login: **`authorization_code`**) |
| `registration.[id].redirect-uri` | `redirectUri` (default `{baseUrl}/login/oauth2/code/{registrationId}`) |
| `registration.[id].scope` | `scopes` |
| `provider.[id].authorization-uri` / `token-uri` / `user-info-uri` | provider endpoints |
| `provider.[id].user-name-attribute` | user-info claim used as the name |
| `provider.[id].jwk-set-uri` | ID-token / OIDC keys |
| `provider.[id].issuer-uri` | OIDC/AS metadata discovery |

If **`registration.[id].provider`** is omitted, the **registration id** is the provider id.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          my-idp:
            client-id: my-client
            client-secret: "…"
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
            scope: openid,profile,email
        provider:
          my-idp:
            authorization-uri: "{idp}/oauth2/authorize"
            token-uri: "{idp}/oauth2/token"
            user-info-uri: "{idp}/userinfo"
            user-name-attribute: sub
            jwk-set-uri: "{idp}/oauth2/jwks"
```

**Listing 1.** Custom provider properties. OIDC shortcut: **`issuer-uri`** on the provider instead of listing endpoints (Boot GETs `{issuer}/.well-known/openid-configuration`). Java equivalent: **`ClientRegistrations.fromIssuerLocation(issuer)`**.

```java
@Bean
ClientRegistrationRepository clientRegistrationRepository() {
	ClientRegistration idp = ClientRegistration.withRegistrationId("my-idp")
			.clientId("my-client")
			.clientSecret("…")
			.clientAuthenticationMethod(ClientAuthenticationMethod.CLIENT_SECRET_BASIC)
			.authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
			.redirectUri("{baseUrl}/login/oauth2/code/{registrationId}")
			.scope("openid", "profile", "email")
			.authorizationUri("{idp}/oauth2/authorize")
			.tokenUri("{idp}/oauth2/token")
			.userInfoUri("{idp}/userinfo")
			.userNameAttributeName("sub")
			.jwkSetUri("{idp}/oauth2/jwks")
			.clientName("My IdP")
			.build();
	return new InMemoryClientRegistrationRepository(idp);
}
```

**Listing 2.** Same object as YAML. A **`ClientRegistrationRepository` `@Bean`** replaces Boot’s property-built repo. Still enable **`http.oauth2Login()`**. Login starts at **`/oauth2/authorization/{registrationId}`**.

```d2
direction: down
common: "CommonOAuth2Provider\ngoogle github facebook x okta" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
custom: "provider.* URIs\nor issuer-uri discovery" {
  width: 260
  height: 50
  style.fill: "#c8e6c9"
}
reg: "ClientRegistration +\noauth2Login()" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}

common -> reg
custom -> reg
```

**Fig. 1.** Well-known brands use the enum. Everyone else is **`spring.security.oauth2.client.provider`** or **`ClientRegistration.Builder`** ([[How do you implement OAuth2 login in Spring Security]], [[What is OAuth2AuthorizationRequestRedirectFilter]], [[What is the OAuth2 authorization code grant in Spring Security]], [[How do you integrate Keycloak with Spring Security]]).

**`OAuth2LoginAuthenticationFilter`** only handles **`/login/oauth2/code/*`** by default. A custom **`redirect-uri`** must stay under that pattern **or** you change **`oauth2Login().redirectionEndpoint().baseUri(...)`**. Register the **same** expanded URI at the IdP (including **`{registrationId}`**, proxy **`{baseUrl}`** / **`X-Forwarded-*`**). **`user-name-attribute`** must exist on the user-info (or ID-token) payload.

> [!warning] Redirect URI is a contract, not a local-only setting
> The IdP’s allowed redirect list must equal the expanded **`{baseUrl}/login/oauth2/code/{registrationId}`**. Changing the path without **`redirectionEndpoint.baseUri`** means the callback never hits **`OAuth2LoginAuthenticationFilter`**.

> [!warning] A `google` registration id is not a custom IdP
> If **`registrationId`** is **`google`**, Boot applies **`CommonOAuth2Provider.GOOGLE`** endpoints even if you meant your own server. Use a distinct id (and **`provider:`** only when you intend those defaults). Missing **`user-name-attribute`** fails user-info mapping.

> [!tip] Interview answer
> A custom OAuth2 IdP is a ClientRegistration with authorization, token, and user-info URIs (or issuer-uri discovery), plus client-id/secret and authorization_code. CommonOAuth2Provider only covers Google, GitHub, Facebook, X, and Okta. Redirect URI defaults to {baseUrl}/login/oauth2/code/{registrationId} and must match both the IdP and OAuth2LoginAuthenticationFilter. Then oauth2Login() — not oauth2ResourceServer.
