<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Security/OAuth2 #Security/JWT #SRS

# What authentication mechanisms does Spring Security support?

> [!abstract] Short answer
> Servlet **Authentication Mechanisms** (reference TOC): **username/password**, **OAuth 2.0 Login** (OIDC and providers like GitHub), **SAML 2.0 Login**, **CAS**, **Remember Me**, **JAAS**, **pre-authentication** (SiteMinder / Java EE), and **X.509**. Username/password is presented as **form login** and **HTTP Basic**, with users in **memory**, **JDBC**, or **LDAP**. **7.x** also first-classes **`oneTimeTokenLogin`**, **`webAuthn`**, and **OAuth2 Resource Server** (**JWT** or **opaque** bearer). Every path ends in an **`Authentication`** on **`SecurityContextHolder`**. **JWT is not its own mode** — it is **`oauth2ResourceServer().jwt()`** (or a custom converter). **OAuth2 password and implicit grants are obsolete.**

## Filters differ; the Authentication contract does not

Architecture: a **filter** (or `AuthenticationManager` call) produces **`Authentication`**; **`ProviderManager`** picks a supporting **`AuthenticationProvider`**. **In-memory / JDBC / LDAP** are **where passwords live**, not extra login types ([[How does form login work internally in Spring Security]], [[How do you configure HTTP Basic authentication in Spring Security]], [[How do you configure LDAP authentication in Spring Security]], [[How do you configure in-memory authentication in Spring Security]]).

| Mechanism | Typical DSL / type | Notes |
| --- | --- | --- |
| Form login | **`formLogin`** | Session cookie; CSRF on POST `/login` |
| HTTP Basic | **`httpBasic`** | `Authorization: Basic`; TLS required |
| Digest | **`DigestAuthenticationFilter`** | Still in **7.1**; needs **plaintext/`NoOpPasswordEncoder`** — not a first-class DSL |
| LDAP bind | **`LdapBindAuthenticationManagerFactory`** | Not a `UserDetailsService` |
| OAuth2 Login / OIDC | **`oauth2Login`** | Client feature; needs OAuth2 Client |
| Resource server | **`oauth2ResourceServer`** | **JWT** (`JwtDecoder`) or **opaque** introspect |
| SAML 2.0 | **`saml2Login`** | |
| CAS | CAS support | **`FACTOR_CAS`** |
| Remember-me | **`rememberMe`** | Hash or persistent token ([[How do you configure remember-me in Spring Security]]) |
| X.509 | **`x509`** | Client cert |
| WebAuthn / passkeys | **`webAuthn`** | **7.x** |
| One-time token | **`oneTimeTokenLogin`** | Magic link; **not TOTP** ([[How do you implement two-factor authentication in Spring Security]]) |
| Pre-auth / JAAS | Pre-auth filter / JAAS | External SSO already authenticated the user |
| Custom token | **`AuthenticationFilter`** | Proprietary header ([[How do you implement custom token-based authentication in Spring Security]]) |

**`FactorGrantedAuthority`** (**7.0**) labels how the current `Authentication` was obtained: **`FACTOR_PASSWORD`**, **`FACTOR_OTT`**, **`FACTOR_WEBAUTHN`**, **`FACTOR_X509`**, **`FACTOR_BEARER`**, **`FACTOR_AUTHORIZATION_CODE`**, **`FACTOR_CAS`**, **`FACTOR_SAML_RESPONSE`**. Combine them with MFA. **`AnonymousAuthenticationFilter`** is a stand-in principal, not a login.

OAuth2 in Spring Security is **resource server**, **client** (including **login**), and (separately) **authorization server**. **Client credentials** is machine-to-machine, not a user login. Mix browser form and API JWT with **two `SecurityFilterChain`s** ([[How do you configure JWT and form login as two SecurityFilterChain beans]]).

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.httpBasic(Customizer.withDefaults())
	.formLogin(Customizer.withDefaults());
```

**Listing 1.** Official username/password sample: **form + Basic**, users from a **`UserDetailsService`** (in-memory in that sample).

```java
http.oauth2ResourceServer((oauth2) -> oauth2.jwt(Customizer.withDefaults()));
```

**Listing 2.** Bearer JWT API. Issuer / JWK is **Boot properties** or a **`JwtDecoder`** bean — not a third `http.jwt()` switch.

```d2
direction: down
mech: "form / Basic / OTT / WebAuthn\noauth2Login / resource server / SAML" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
am: "AuthenticationManager\nProviderManager" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
ctx: "SecurityContextHolder\nAuthentication + FactorGrantedAuthority" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

mech -> am -> ctx
```

**Fig. 1.** Choose a **mechanism** (filter). Storage (JDBC vs LDAP) only feeds **password** providers.

> [!warning] JWT ≠ a login page
> **`oauth2ResourceServer().jwt()`** validates a bearer access token. **`oauth2Login()`** is the browser redirect to an IdP. Calling that “JWT mode” conflates **resource server** and **login**. Dumps still list **password grant** and **implicit**; current OAuth2 practice and Spring’s client docs center **authorization code** (login) and **client credentials** (app-to-app).

> [!warning] Digest and OpenID 2.0
> Digest still exists but the reference tells you to use **TLS** and **insecure password storage**. Do not pick it for new work. **OpenID 2.0** is gone; **OIDC** is **`oauth2Login`**. Remember-me is on the official mechanisms list; it is **not** a substitute for OAuth2.

> [!tip] Interview answer
> Spring Security authenticates through filters that all produce an Authentication: form login and HTTP Basic for passwords, oauth2Login for OIDC, oauth2ResourceServer for JWT or opaque bearers, plus SAML, CAS, X.509, remember-me, WebAuthn, and one-time tokens. In-memory, JDBC, and LDAP are user stores for username/password, not separate protocols. JWT is resource-server bearer validation, not a distinct Spring “mode,” and the OAuth2 password grant is not how you log humans in.
