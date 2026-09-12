<!--
reps: 0
priority: 0
-->
#Security/OAuth2 #SRS

# What is the difference between an access token and a refresh token

> [!abstract] Short answer
> In OAuth 2.0 (RFC 6749) the **access token** is the credential presented to resource servers - short-lived, audience-scoped, the only token that should ever leave the client's hands toward APIs. The **refresh token** lives at the client, is presented **only to the authorization server** to obtain new access tokens, and exists so those short access tokens do not force the user to log in every few minutes. One grants resources; the other re-arms the first without re-authentication.

## The two-token flow

```d2
direction: right
c: "Client" { width: 130; height: 60; style.fill: "#e3f2fd" */
as: "Authorization Server" { width: 240; height: 70; style.fill: "#e8f5e9"
rs: "Resource Server / API" { width: 250; height: 70; style.fill: "#fff3e0" */
c -> as: "1. authenticate once"
as -> c: "2. access token (minutes) + refresh token (long)"
c -> rs: "3. call with access token"
c -> as: "4. access expired: refresh token -> new access token"
```

**Fig. 1.** The refresh token travels on one route only - client to authorization server. If it starts appearing at resource servers, the design has inverted.

The separation is deliberate blast-radius engineering:

- **Lifetime**: access tokens live minutes (typ. 5-60), refresh tokens live days to weeks or until rotation.
- **Audience**: access tokens name the resource server (`aud`); refresh tokens are meaningless to resource servers - they are credentials for the token endpoint only.
- **Exposure**: a stolen access token is a small window; a stolen refresh token is a *renewable* window, so storage rules are stricter - confidential clients keep it server-side, browsers get httpOnly cookies ([[Where should you store a JWT in a browser]]).
- **Revocation**: revoking a refresh token ends the whole session lineage; revoking an access token only works via the denylist/rotation levers of [[How do you revoke a JWT]].

## Rotation and reuse detection

RFC 6749 section 6 defines the refresh grant; section 10.4 makes the client responsible for refresh-token confidentiality. Modern authorization servers go further: every refresh use issues a **new refresh token and retires the old one**, and seeing the retired token again signals theft - the server revokes the session. That turns the refresh token into a self-reporting tripwire.

```http
POST /oauth/token
grant_type=refresh_token&refresh_token=...&client_id=...
```

**Listing 1.** The refresh grant: the only endpoint where the refresh token is ever presented.

> [!warning] "Access tokens are identity proof"
> An access token answers "what may this client do at this resource" - authorization. Using its claims as *authentication* of a user is a category error resource servers keep making; verification of the user happens at the authorization server, and the token inherits trust only within its audience and lifetime ([[What is JWT for]]).

> [!tip] Interview answer
> Access token: short-lived, audience-scoped, presented to APIs. Refresh token: long-lived, client-held, presented only to the token endpoint to mint new access tokens - the reason APIs can accept 15-minute tokens without user-visible logins. Rotation with reuse detection is the modern default, and a refresh token seen at a resource server is a design bug, not a token.
