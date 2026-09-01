<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #SRS

# What is OAuth 2.0?

> [!abstract] Short answer
> **RFC 6749** — an **authorization** framework (not a login spec). A **client** gets an **access token** (a string with **scope** and **lifetime**) to call a **resource server**, **without** the **resource owner**’s password. The **authorization server** issues that token after authenticating the owner (or the client itself). “Sign in with Google” is usually **OAuth 2.0 + OpenID Connect**, not OAuth alone. In Spring: **`oauth2Login()` / `oauth2Client()`** = client; **`oauth2ResourceServer()`** = resource server.

## Four roles, then a token

RFC 6749 §1.1:

| Role | Who | Spring (typical) |
| --- | --- | --- |
| **Resource owner** | Grants access (the **end-user** when a person) | Not a filter |
| **Client** | App that calls APIs **on the owner’s behalf** | **`oauth2Login()`**, **`oauth2Client()`**, Gateway **TokenRelay** |
| **Authorization server** | Authenticates the owner, issues tokens | **Spring Authorization Server** / Google / Keycloak — **not** Spring Security’s minting job |
| **Resource server** | Hosts data; accepts **access tokens** | **`oauth2ResourceServer()`** + **`JwtDecoder`** or opaque introspection |

Abstract flow: owner authorizes → client presents a **grant** at the **token endpoint** → **access token** → client sends that token to the resource server.

RFC grants: **authorization code**, **client credentials** (client acts **on its own behalf**), plus **implicit** and **resource owner password** (legacy; do not use for new apps). **Refresh tokens** are optional extra credentials from the authorization server.

```java
http.oauth2Login(Customizer.withDefaults());
http.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
```

**Listing 1.** Two **different** Spring roles. Login starts a **browser session** after the code grant. Resource server validates a **Bearer** token on each API call — it does **not** run the authorization-code dance ([[How do you implement OAuth2 login in Spring Security]], [[How do you secure microservices with Spring Security]], [[What is JwtDecoder in Spring Security]]).

```d2
direction: down
ro: "Resource Owner" {
  width: 150
  height: 36
  style.fill: "#e3f2fd"
}
as: "Authorization Server" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
cl: "Client" {
  width: 120
  height: 36
  style.fill: "#c8e6c9"
}
rs: "Resource Server" {
  width: 160
  height: 40
  style.fill: "#c8e6c9"
}

ro -> as: "authenticates / consents"
cl -> as: "grant → access token"
cl -> rs: "access token"
as -> cl: "token"
```

**Fig. 1.** Password stays with the authorization server. The client stores an **access token**, not the user’s password ([[How do you refresh an expired JWT in Spring Security]], [[What is EnableOAuth2Sso]], [[What is EnableResourceServer]]).

An access token is **any string** the resource server understands (JWT **or** opaque). JWT is a common encoding, not part of RFC 6749.

> [!warning] OAuth 2.0 is not authentication
> RFC 6749 does not define how the user proves who they are to **your** app. **OpenID Connect** adds an **ID token** and a userinfo contract. “Sign in with Google” without OIDC is only “Google issued an access token for some API.”

> [!warning] Password grant is not the point of OAuth
> The framework exists so the client **never** sees the owner’s password. **ROPC** and **implicit** are in RFC 6749 and are **obsolete** in current Spring / OAuth 2.1 practice. Prefer **authorization code + PKCE** for users and **client credentials** for machines.

> [!tip] Interview answer
> OAuth 2.0 is RFC 6749 authorization: a client obtains a scoped access token from an authorization server so it can call a resource server without the user’s password. Four roles: resource owner, client, authorization server, resource server. Spring maps login/client vs resource server to different DSLs. Login/identity is OIDC on top.
