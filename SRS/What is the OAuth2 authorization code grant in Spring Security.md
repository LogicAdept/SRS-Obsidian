<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is the OAuth2 authorization code grant in Spring Security?

> [!abstract] Short answer
> RFC 6749 **§4.1**: the **browser** grant. The client sends the user to the authorization endpoint (`response_type=code`); the authorization server **redirects back with a one-time `code`**; the client **POSTs** that code to the **token** endpoint (`grant_type=authorization_code`) with a **client secret** (confidential) or **PKCE**. Spring maps this to **`oauth2Login()`** (and **`oauth2Client()`** code grant): **`GET /oauth2/authorization/{registrationId}`** then **`/login/oauth2/code/*`**. It is **not** machine-to-machine (**client credentials**).

## Redirect with a code, then a back-channel token POST

RFC flow (A–E): user-agent → **authorize** → user authenticates/consents → redirect includes **`code`** (and **`state`**) → client **token** request authenticates and sends the **same** `redirect_uri`. The **access token** (optional **refresh token**) is in that **token** response, never in the first redirect. The code **MUST NOT** be used twice; RFC recommends it expire within **10 minutes**.

Spring Client:

| Piece | Role |
| --- | --- |
| **`ClientRegistration`** with **`authorization-grant-type: authorization_code`** | Boot YAML / `CommonOAuth2Provider` |
| **`OAuth2AuthorizationRequestRedirectFilter`** | Starts the grant; default **`/oauth2/authorization/{id}`** |
| **`OAuth2LoginAuthenticationFilter`** | Login callback; default **`/login/oauth2/code/*`** |
| **`RestClientAuthorizationCodeTokenResponseClient`** | Exchanges **`code`** at the token URI |
| **`AuthorizationCodeOAuth2AuthorizedClientProvider`** | Same grant for **`oauth2Client()`** (not only login) |

OAuth 2.0 Login **is** this grant. “Login with Google” is **authorization code** (usually plus **OIDC** `id_token`), not a special Spring grant ([[How do you implement OAuth2 login in Spring Security]], [[What is OAuth2AuthorizationRequestRedirectFilter]]).

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: google-client-id
            client-secret: google-client-secret
            authorization-grant-type: authorization_code
            redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"
```

**Listing 1.** Confidential client. Public clients omit the secret, set **`client-authentication-method: none`**, and Spring **automatically** adds PKCE (`code_challenge`). Force PKCE with **`ClientRegistration.clientSettings.requireProofKey=true`**.

```java
http.oauth2Login(Customizer.withDefaults());
```

**Listing 2.** Installs the redirect filter + login callback. Customize **`oauth2Login().authorizationEndpoint()`** / **`redirectionEndpoint()`** if you change those default paths ([[How do you register a custom OAuth2 identity provider]], [[What is the difference between an OAuth2 client and a resource server]]).

```d2
direction: down
app: "Client oauth2Login()" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
as: "Authorization server" {
  width: 180
  height: 36
  style.fill: "#fff3e0"
}
token: "POST /token\ngrant_type=authorization_code" {
  width: 280
  height: 48
  style.fill: "#c8e6c9"
}

app -> as: "GET /authorize?response_type=code"
as -> app: "redirect ?code=… (not the access token)"
app -> token: "code + secret or PKCE"
token -> app: "access_token (+ refresh)"
```

**Fig. 1.** Front channel carries the **code**. Token POST is **client → AS** ([[What is OAuth 2.0]]).

> [!warning] The first redirect is not a token
> A query `access_token` on the callback is **implicit**, not this grant. Reusing a `code` must fail; the authorization server **SHOULD** revoke tokens already issued from that code.

> [!warning] SPA + client-secret is not the public-client recipe
> Public clients (native / browser) cannot keep a secret. Spring’s PKCE path is **empty secret** + **`client-authentication-method: none`**. A confidential web app still uses a **server-side** secret. This grant needs a **user-agent**; **client credentials** is the app-only grant.

> [!tip] Interview answer
> Authorization code is the browser OAuth 2.0 grant: redirect to the authorization server, come back with a one-time code, exchange it at the token endpoint. Spring Security implements it with oauth2Login (and oauth2Client): /oauth2/authorization/{id} out, /login/oauth2/code/{id} back. The access token is not in that first redirect. Public clients use PKCE, not a secret in the SPA.
