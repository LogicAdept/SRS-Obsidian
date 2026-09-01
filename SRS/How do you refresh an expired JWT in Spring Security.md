<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# How do you refresh an expired JWT in Spring Security?

> [!abstract] Short answer
> You do **not** refresh inside **`JwtDecoder`**. The **resource server rejects** an access JWT whose **`exp`** is past **`JwtTimestampValidator`** (default **60s** skew). The **OAuth2 client** (or the browser SPA) sends the **refresh token** to the **authorization server token endpoint** (`grant_type=refresh_token`) and then calls the API with the **new** access JWT.

## Resource server vs client vs token endpoint

An access JWT is **self-contained**. Spring Security’s resource server validates **`iss` / `exp` / `nbf`** (and signature). Expiry is **`BadJwtException` / `JwtValidationException`**, not a JJWT **`JWTExpiredException`**, and not **`PasswordEncoder`**. Clock skew is **not** a refresh.

A **new** access token comes from the **authorization server**, typically OAuth 2.0 **refresh_token**:

1. Authorization-code (or similar) response optionally included an **`OAuth2RefreshToken`**.
2. When **`OAuth2AuthorizedClient.getAccessToken()`** is expired **and** **`getRefreshToken()`** is present, **`RefreshTokenOAuth2AuthorizedClientProvider`** re-authorizes.
3. **`RestClientRefreshTokenTokenResponseClient`** POSTs to the token endpoint. Spring Authorization Server handles that grant with **`OAuth2RefreshTokenAuthenticationConverter` / `OAuth2RefreshTokenAuthenticationProvider`** on **`OAuth2TokenEndpointFilter`** (default path `/oauth2/token`).

```java
@Bean
OAuth2AuthorizedClientManager authorizedClientManager(
		ClientRegistrationRepository registrations,
		OAuth2AuthorizedClientRepository authorizedClients) {
	OAuth2AuthorizedClientProvider provider =
			OAuth2AuthorizedClientProviderBuilder.builder()
					.authorizationCode()
					.refreshToken() // RefreshTokenOAuth2AuthorizedClientProvider
					.build();
	DefaultOAuth2AuthorizedClientManager manager =
			new DefaultOAuth2AuthorizedClientManager(registrations, authorizedClients);
	manager.setAuthorizedClientProvider(provider);
	return manager;
}
```

**Listing 1.** Client-side auto-refresh. **`authorize()`** returns **`null`** if there is no refresh token or the access token is **not** expired (default client clock skew **60s**). Failed refresh **removes** the saved **`OAuth2AuthorizedClient`**.

```d2
direction: down
rs: "Resource server\nJwtDecoder + exp" {
  width: 220
  height: 50
  style.fill: "#ffcdd2"
}
client: "OAuth2 client /\nRefreshTokenOAuth2AuthorizedClientProvider" {
  width: 280
  height: 55
  style.fill: "#c8e6c9"
}
as: "Authorization server\n/oauth2/token refresh_token" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}

rs -> client: "401 expired access JWT"
client -> as: "refresh token"
as -> client: "new access JWT"
client -> rs: "Authorization: Bearer"
```

**Fig. 1.** The API that **validates** JWTs does not mint replacements. The token endpoint does ([[What is the OAuth2 refresh token grant]], [[What is the difference between an OAuth2 client and a resource server]], [[Why should you not catch Exception when validating a JWT]], [[What is JWT clock skew in Spring Security]]).

If **your** app **is** the authorization server, implement refresh **there** (SAS already does). A homemade `/refresh` that accepts the **expired access JWT** on every business URL is not the OAuth2 grant: the refresh credential is the **refresh token**, held and rotated by the client/AS, not replayed as a Bearer on resource endpoints.

> [!warning] Do not “refresh” by accepting expired access JWTs
> Widening **`JwtTimestampValidator`** or catching decode failures so an expired Bearer still gets in is not refresh. The resource server must keep rejecting that token until the client presents a **new** access JWT.

> [!warning] `JwtDecoder` has no refresh API
> **`NimbusJwtDecoder`** only validates. Auto-refresh exists on **`OAuth2AuthorizedClientManager`**, and only when a refresh token was issued. No refresh token means the user must authorize again — not a second call with the dead access JWT.

> [!tip] Interview answer
> Spring Security resource servers do not refresh JWTs; JwtTimestampValidator fails expired access tokens. The OAuth2 client uses RefreshTokenOAuth2AuthorizedClientProvider to call the authorization server token endpoint with grant_type=refresh_token. Spring Authorization Server already implements that grant. Homemade endpoints that accept the expired access JWT on every API are the wrong model.
