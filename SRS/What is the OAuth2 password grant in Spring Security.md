<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is the OAuth2 password grant in Spring Security?

> [!abstract] Short answer
> RFC 6749 **§4.3** (**resource owner password credentials**): the user types **username/password into the client**; the client **POSTs** `grant_type=password` plus those fields to the **token** endpoint (confidential clients also send **client id/secret**). RFC 9700 **§2.4**: this grant **MUST NOT** be used. Spring Security **7** **removed** it. In **5.8–6.x** it was **`PasswordOAuth2AuthorizedClientProvider`**, **`@Deprecated(forRemoval=true)`**. It is **not** `oauth2Login()` (authorization code) and **not** client credentials (no user password).

## The client sees the user’s password

RFC flow: (A) owner gives credentials to the **client** → (B) client authenticates at the **token** endpoint and sends **`username` / `password`** → (C) access token (optional refresh). **No** browser redirect to the authorization server. The client **MUST discard** the password after the token. RFC 6749 already limited it to **high-trust** apps (OS / privileged) when **other grants are not viable**.

| | Password (§4.3) | Authorization code | Client credentials |
| --- | --- | --- | --- |
| User involved | **Yes** — password **to the client** | Yes — password **only at the AS** | **No** |
| `grant_type` | **`password`** | `authorization_code` | `client_credentials` |
| Browser to `/authorize` | **No** | **Yes** | No |

RFC 9700: it **exposes owner credentials to the client**, enlarges the leak surface, **trains users to type passwords into the wrong app**, and **does not work** with MFA / WebAuthn ([[What is OAuth 2.0]], [[What is the OAuth2 authorization code grant in Spring Security]]).

```
POST /token
Authorization: Basic {client_id}:{client_secret}
Content-Type: application/x-www-form-urlencoded

grant_type=password&username={user}&password={password}
```

**Listing 1.** RFC token request. This is **not** form login (`UsernamePasswordAuthenticationFilter`) and **not** **`oauth2Login()`** ([[How do you implement OAuth2 login in Spring Security]]).

```java
// Spring Security 6.x only — gone in 7.0
OAuth2AuthorizedClientProvider provider = OAuth2AuthorizedClientProviderBuilder.builder()
		.password()   // @Deprecated(since = "5.8", forRemoval = true)
		.build();
```

**Listing 2.** Historical Client API: **`PasswordOAuth2AuthorizedClientProvider`** (since **5.2**). `authorize` needed context attributes **`USERNAME_ATTRIBUTE_NAME`** / **`PASSWORD_ATTRIBUTE_NAME`**. Security **7.0** “Removed support for password grant.” Current **`AuthorizationGrantType`** has **`AUTHORIZATION_CODE`**, **`CLIENT_CREDENTIALS`**, **`REFRESH_TOKEN`**, … — **no** password constant ([[What is the OAuth2 client credentials grant in Spring Security]], [[What is the OAuth2 implicit grant]]).

```d2
direction: down
user: "User password" {
  width: 140
  height: 36
  style.fill: "#ffcdd2"
}
client: "Client (must not do this)" {
  width: 220
  height: 40
  style.fill: "#ffe0b2"
}
as: "Authorization server\nPOST /token" {
  width: 200
  height: 48
  style.fill: "#fff3e0"
}

user -> client: "username + password"
client -> as: "grant_type=password"
as -> client: "access_token"
```

**Fig. 1.** The whole point of OAuth is that the **client does not collect** the owner’s password. Prefer **authorization code + PKCE** (user) or **client credentials** (machine).

> [!warning] RFC 9700 is MUST NOT, not a style preference
> Interviews that still walk the POST are testing recall, then the follow-up: **do not ship it**. “OAuth 2.1 drops password” is the same story as this BCP. A native app logging into a social IdP with the **user’s password** is the anti-pattern RFC 6749 already warned against.

> [!warning] Do not migrate Boot 2 samples forward
> YAML **`authorization-grant-type: password`** plus **`.password()`** on the provider builder **will not compile** on Security 7. Replacing it with **`oauth2Login()`** is a **different** grant (redirect), not a drop-in.

> [!tip] Interview answer
> The password grant is RFC 6749 resource owner password credentials: the client collects username and password and POSTs grant_type=password to the token endpoint. It is not authorization code and not client credentials. RFC 9700 forbids it. Spring Security deprecated PasswordOAuth2AuthorizedClientProvider in 5.8 and removed the grant in 7.0. Use oauth2Login (code + PKCE) or client credentials instead.
