<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is the OAuth2 implicit grant?

> [!abstract] Short answer
> RFC 6749 **§4.2**: an old **browser / SPA** grant. The authorization server redirects with **`response_type=token`** and puts the **access token in the URI fragment** (`#access_token=…`). There is **no** token-endpoint POST, **no** client secret, and **no refresh token**. RFC 9700 **§2.1.2**: clients **SHOULD NOT** use it. Spring Security **`oauth2Login()`** is **authorization code** (public clients: **PKCE**). **`AuthorizationGrantType`** has **no** `IMPLICIT`.

## Token in the fragment, not a code

RFC 6749 designed implicit for **JavaScript** public clients that cannot keep a secret. Unlike **§4.1**, the client does **not** redeem an intermediate **code**. The user-agent keeps the fragment locally; a script reads **`access_token`**. The token is therefore visible to the **resource owner** and **other apps on the device**.

| | Implicit (§4.2) | Authorization code (§4.1) |
| --- | --- | --- |
| Authorize query | **`response_type=token`** | **`response_type=code`** |
| Redirect carries | **`#access_token`** (fragment) | **`?code=`** (query) |
| Token endpoint | **None** | **`grant_type=authorization_code`** |
| Refresh token | **MUST NOT** | Optional |
| Client auth | **None** | Secret or **PKCE** |

RFC 9700: implicit and other types that issue **access tokens in the authorization response** leak and replay. Prefer **`code`** (or OIDC **`code id_token`**) so tokens appear only in the **token** response ([[What is the OAuth2 authorization code grant in Spring Security]], [[What is OAuth 2.0]]).

```
GET /authorize?response_type=token&client_id=…&redirect_uri=…&state=…

302 Location: {redirect_uri}#access_token=…&token_type=bearer&state=…
```

**Listing 1.** RFC implicit. That `#access_token` is **not** Spring’s login callback (`/login/oauth2/code/{id}?code=`).

```java
http.oauth2Login(Customizer.withDefaults());
```

**Listing 2.** Spring OAuth2 Login **is** the code grant. **`AuthorizationGrantType`** constants: **`AUTHORIZATION_CODE`**, **`CLIENT_CREDENTIALS`**, **`REFRESH_TOKEN`**, **`JWT_BEARER`**, **`DEVICE_CODE`**, **`TOKEN_EXCHANGE`** — **not** implicit. Public browser/native clients use **`authorization_code`** + PKCE (`client-authentication-method: none`) ([[How do you implement OAuth2 login in Spring Security]], [[What is the OAuth2 client credentials grant in Spring Security]]).

```d2
direction: down
impl: "Implicit (do not use)\n#access_token in browser" {
  width: 280
  height: 48
  style.fill: "#ffcdd2"
}
code: "Authorization code + PKCE\n?code= then POST /token" {
  width: 280
  height: 48
  style.fill: "#c8e6c9"
}
login: "oauth2Login()" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}

code -> login
```

**Fig. 1.** Implicit never hits Spring’s token client (`RestClientAuthorizationCodeTokenResponseClient`). Machine-to-machine is **client credentials**, not this grant.

> [!warning] Fragment tokens leak
> Browser **history**, **Referer**, extensions, and open-redirect tricks (RFC 9700 §4.1.2) can steal `#access_token`. There is **no** one-time code to bind with PKCE. Do **not** put access tokens in a **query** string either (RFC 6750).

> [!warning] Not a Spring Security 6/7 login option
> YAML **`authorization-grant-type: implicit`** is **not** a documented Client provider. Login samples and **`oauth2Login()`** are **authorization code**. Implicit is **not** “SPA OAuth”; current SPA/native recipe is **code + PKCE**.

> [!tip] Interview answer
> Implicit is RFC 6749’s old SPA grant: response_type=token and the access token in the redirect fragment, with no token endpoint and no refresh token. It is not recommended (RFC 9700). Spring Security oauth2Login uses authorization code; AuthorizationGrantType has no IMPLICIT. Public clients should use authorization code plus PKCE.
