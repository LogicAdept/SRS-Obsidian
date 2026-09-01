<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is the OAuth2 refresh token grant?

> [!abstract] Short answer
> RFC 6749 **§1.5 / §6**: the client **POSTs** `grant_type=refresh_token` and the **refresh token** to the **authorization server token endpoint** and gets a **new access token** (optional **new** refresh token) **without** the user’s password. Refresh tokens are **never** sent to the **resource server**. Spring: **`RefreshTokenOAuth2AuthorizedClientProvider`** + **`RestClientRefreshTokenTokenResponseClient`**, usually chained after **authorization code**. The resource server still **rejects** an expired access token until the client presents a new one.

## A second token, used only at the AS

A refresh token is an **opaque** (to the client) credential issued **with** an access token. It obtains **another** access token when the current one expires, or one with **identical or narrower** scope. Issuing it is **optional**. RFC flow after expiry: resource server returns **invalid token** → client authenticates at the **token** endpoint with the refresh token → new access token.

| Rule | Source |
| --- | --- |
| `grant_type` **MUST** be **`refresh_token`** | RFC 6749 §6 |
| Confidential clients **MUST** authenticate; token is **bound to that client** | §6 |
| New `scope` **MUST NOT** exceed the original grant | §6 |
| If a **new** refresh token is issued, **discard** the old one | §6 (rotation) |
| **Never** send the refresh token to a resource server | §1.5 |
| Implicit: **MUST NOT** issue refresh tokens | §4.2 |
| Client credentials: refresh **SHOULD NOT** be included | §4.4.3 |

RFC 9700: public clients **MUST** use **rotation** or **sender-constrained** refresh tokens (DPoP / mTLS). Authorization servers **SHOULD** expire unused refresh tokens ([[What is OAuth 2.0]], [[What is the OAuth2 authorization code grant in Spring Security]]).

```
POST /token
Authorization: Basic {client_id}:{client_secret}
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token={refresh_token}
```

**Listing 1.** No `username` / `password`. This is **not** the password grant.

```java
OAuth2AuthorizedClientProvider provider = OAuth2AuthorizedClientProviderBuilder.builder()
		.authorizationCode()
		.refreshToken()
		.build();
```

**Listing 2.** Spring Client. If **`OAuth2AuthorizedClient.getRefreshToken()`** is present and **`getAccessToken()`** is expired, **`RefreshTokenOAuth2AuthorizedClientProvider`** refreshes automatically via **`RestClientRefreshTokenTokenResponseClient`**. **`AuthorizationGrantType.REFRESH_TOKEN`** exists; **`authorize()`** returns **`null`** when there is nothing to refresh ([[How do you refresh an expired JWT in Spring Security]], [[What is the OAuth2 client credentials grant in Spring Security]]).

```d2
direction: down
rs: "Resource server\nrejects expired access token" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}
client: "OAuth2 client" {
  width: 160
  height: 36
  style.fill: "#c8e6c9"
}
as: "Authorization server\ngrant_type=refresh_token" {
  width: 240
  height: 48
  style.fill: "#fff3e0"
}

rs -> client: "invalid_token"
client -> as: "refresh_token (not to RS)"
as -> client: "new access_token"
client -> rs: "Authorization: Bearer"
```

**Fig. 1.** **`JwtDecoder`** on the API does **not** mint tokens ([[What is JwtDecoder in Spring Security]], [[What is JWT clock skew in Spring Security]]).

> [!warning] Refresh is not a resource-server feature
> An expired Bearer is still a **401**. Clock skew is **not** a refresh. The client (or SPA) talks to the **token** endpoint; the API only **validates** the next access token.

> [!warning] Refresh tokens are high-value secrets
> They represent the **full** consented grant. Do **not** put them in URLs or send them downstream. Implicit has **no** refresh token; do not invent one. After rotation, reuse of the **old** refresh token is a **breach signal** (RFC 9700) — Spring drops the saved **`OAuth2AuthorizedClient`** if refresh fails.

> [!tip] Interview answer
> The refresh token grant is RFC 6749 section 6: POST grant_type=refresh_token to the authorization server for a new access token without the user. Refresh tokens never go to the resource server. Spring Security’s client auto-refreshes via RefreshTokenOAuth2AuthorizedClientProvider after authorization code. JwtDecoder does not refresh. Public clients should use rotation or sender-constrained refresh tokens.
