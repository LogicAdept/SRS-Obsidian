<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/OIDC #SRS

# How would you explain OAuth OpenID Connect?

> [!abstract] Short answer
> **OAuth 2.0 (RFC 6749)** is **authorization**: a **client** gets an **access token** to call a **resource server** without the user’s password. It does **not** define how your app learns **who** logged in. **OpenID Connect 1.0** is an **identity layer on OAuth 2.0**: request **`scope=openid`**, get an **ID Token** (JWT) with **`iss` / `sub` / `aud` / `exp` / `iat`**, optionally **UserInfo**. The AS is an **OpenID Provider (OP)**; your app is a **Relying Party (RP)**. Spring: **`oauth2Login()`** with **`openid`** uses **`OidcUserService`**; GitHub/Facebook-style login without `openid` is **OAuth-only**.

## Authorization vs authentication

RFC 6749: tokens grant **access to HTTP resources**. Without a profile, OAuth **cannot** tell the RP that an End-User authenticated.

OIDC Core: authentication is an **extension** of that process. The Authentication Request **MUST** include **`openid`**. Missing `openid` may still be valid OAuth, but it is **not** OpenID Connect. Result: **ID Token** (signed JWT) plus usually an **access token**. The access token may call **UserInfo** (and APIs); the ID Token is **for the RP** to verify the login.

| | OAuth 2.0 | OpenID Connect |
| --- | --- | --- |
| Question | What may this client do? | Who authenticated? |
| Token for that | **Access token** (any string; often JWT) | **ID Token** (JWT, **MUST** be JWS) |
| Extra endpoint | Token / authorize | **UserInfo** (claims with the access token) |
| Names | client / AS / RS | **RP** / **OP** |
| Spring login | `oauth2Login` + **`DefaultOAuth2UserService`** | `scope: openid` → **`OidcUserService`**, **`OidcUser`** |

Preferred OIDC path: **authorization code** (`response_type=code`) so tokens come from the **token** endpoint, not the browser ([[What is OAuth 2.0]], [[What is the OAuth2 authorization code grant in Spring Security]]).

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          my-op:
            scope: openid,profile
```

**Listing 1.** **`openid`** switches Spring to OIDC (`OidcUserService`). Without it, even `oauth2Login()` is OAuth userinfo, not an ID Token ([[How do you implement OAuth2 login in Spring Security]], [[How do you integrate Keycloak with Spring Security]]).

```json
{
  "iss": "{issuer}",
  "sub": "24400320",
  "aud": "{client_id}",
  "exp": 1311281970,
  "iat": 1311280970
}
```

**Listing 2.** Required ID Token claims (OIDC §2). **`aud` MUST** include the RP’s **`client_id`**. Optional: **`nonce`**, **`auth_time`**, **`acr` / `amr`**. Profile fields (`name`, `email`) may live here or on **UserInfo**.

```d2
direction: down
oauth: "OAuth 2.0\naccess_token → APIs" {
  width: 240
  height: 48
  style.fill: "#fff3e0"
}
oidc: "OIDC\nid_token → who logged in" {
  width: 240
  height: 48
  style.fill: "#c8e6c9"
}
login: "oauth2Login() + openid" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}

oidc -> oauth: "built on"
oidc -> login
```

**Fig. 1.** An API that validates **Bearer access tokens** is still a **resource server**, not OIDC login ([[What is the difference between an OAuth2 client and a resource server]], [[When should you use OAuth2 login versus form login]]).

> [!warning] An access token is not an ID Token
> “Sign in with X” that only returns an access token proves **the IdP issued API access**, not a standard **`sub`**. **GitHub and Facebook** are called out in Spring as **OAuth login without OIDC**. Do **not** send the **ID Token** as `Authorization: Bearer` to your APIs unless that is an explicit contract — resource servers expect an **access** JWT ([[How do you configure Spring as an OAuth2 resource server]]).

> [!warning] `openid` is not optional if you mean OIDC
> OIDC: if `openid` is absent, behavior is **unspecified** as OpenID Connect. Spring will **not** use **`OidcUserService`**. OIDC implicit (`response_type=id_token`) is a spec path; Spring **`oauth2Login()`** is the **code** grant.

> [!tip] Interview answer
> OAuth 2.0 is authorization: access tokens for APIs, no standard identity. OpenID Connect adds authentication on that stack: scope openid, ID Token JWT (iss, sub, aud, exp, iat), optional UserInfo. The IdP is the OpenID Provider; your app is the Relying Party. In Spring, oauth2Login with openid is OIDC; without it, or for GitHub-style providers, it is OAuth-only login.
