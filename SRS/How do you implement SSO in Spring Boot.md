<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Security/OAuth2 #SRS

# How do you implement SSO in Spring Boot?

> [!abstract] Short answer
> Browser SSO is **OAuth2 Login / OpenID Connect**: add **`spring-boot-starter-security-oauth2-client`**, register a client (`authorization_code`, scope **`openid`**), and call **`http.oauth2Login()`**. The user hits **`/oauth2/authorization/{registrationId}`**, the IdP redirects to **`/login/oauth2/code/{registrationId}`**, Boot keeps a **servlet session**. APIs do **not** do that dance — they are a **resource server** (`issuer-uri` / JWK) and check a **Bearer JWT**. Do **not** use **`@EnableOAuth2Sso`** or **`WebSecurityConfigurerAdapter`**. Enterprise alternative: **SAML 2** (`saml2Login()`).

## One IdP, two Spring roles

SSO means **one identity provider**, many apps. In current Spring that IdP is almost always an **OIDC authorization server** (Keycloak, Okta, Auth0, Entra, or **Spring Authorization Server**). Each **user-facing** app is an **OAuth2 client**. Each **API** is a **resource server**. Mixing those two in one process needs an explicit **`SecurityFilterChain`** — Boot’s default web security **backs off** when you combine modules ([[What is the difference between an OAuth2 client and a resource server]]).

Boot 4 starter IDs: **`spring-boot-starter-security-oauth2-client`** (old `spring-boot-starter-oauth2-client` is **deprecated**). Same pattern for **resource-server** and **authorization-server**.

```properties
spring.security.oauth2.client.registration.my-oidc-client.provider=my-oidc-provider
spring.security.oauth2.client.registration.my-oidc-client.client-id=${CLIENT_ID}
spring.security.oauth2.client.registration.my-oidc-client.client-secret=${CLIENT_SECRET}
spring.security.oauth2.client.registration.my-oidc-client.authorization-grant-type=authorization_code
spring.security.oauth2.client.registration.my-oidc-client.scope=openid,profile
spring.security.oauth2.client.registration.my-oidc-client.redirect-uri={baseUrl}/login/oauth2/code/{registrationId}
spring.security.oauth2.client.provider.my-oidc-provider.issuer-uri=${IDP_ISSUER}
```

**Listing 1.** `OAuth2ClientProperties`. **`openid`** selects **OIDC** (`OidcUserService`, `id_token`). Omit it and Security uses **`DefaultOAuth2UserService`** (GitHub/Facebook-style). Common provider IDs with built-in metadata: **`google`**, **`github`**, **`facebook`**, **`x`**, **`okta`**. Discovery: Boot GETs `{issuer}/.well-known/openid-configuration` ([[How do you register a custom OAuth2 identity provider]]).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated());
	http.oauth2Login(Customizer.withDefaults());
	return http.build();
}
```

**Listing 2.** Default callback matcher is **`/login/oauth2/code/*`**. Change `redirect-uri` only if you also change `oauth2Login().redirectionEndpoint().baseUri(...)`. Login start path: **`/oauth2/authorization/my-oidc-client`** ([[How do you implement OAuth2 login in Spring Security]], [[What is the OAuth2 authorization code grant in Spring Security]]).

```properties
spring.security.oauth2.resourceserver.jwt.issuer-uri=${IDP_ISSUER}
```

**Listing 3.** API side. Validates signature and issuer; optional `audiences`. Opaque tokens use **introspection**, not a homemade HMAC filter.

```d2
direction: down
browser: "Browser app\noauth2Login + session" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
idp: "OIDC IdP\nauthorization_code" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
api: "Resource server\nBearer JWT" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

browser -> idp
idp -> browser
browser -> api
```

**Fig. 1.** The session lives in the **BFF / UI**. The API trusts the **access token**, not a shared cookie secret ([[How do you configure Spring as an OAuth2 resource server]], [[How would you explain OAuth OpenID Connect]]).

SAML 2: **`spring-boot-starter-security-saml2`** + `spring.security.saml2.relyingparty.registration.*` and **`http.saml2Login()`**. That is still SSO; it is a **different** protocol than OIDC.

If **you** are the IdP, add **`spring-boot-starter-security-oauth2-authorization-server`** and register clients under `spring.security.oauth2.authorizationserver.client`. Auto-config is a **getting-started** default (`InMemoryRegisteredClientRepository`) — production wants JDBC (or equivalent) for clients **and** for `OAuth2AuthorizedClientService` on the login app.

> [!warning] `@EnableOAuth2Sso` is not current Spring
> Dumps copy **`spring-security-oauth2-autoconfigure`**, **`WebSecurityConfigurerAdapter`**, **`@EnableResourceServer`**, and **`antMatchers`**. That stack is gone ([[What is EnableOAuth2Sso]], [[Why was WebSecurityConfigurerAdapter removed]]). A signed JWT checked with a **shared secret you invented** is also not SSO.

> [!warning] Login is not a resource server
> `oauth2Login()` establishes a **user session**. `oauth2ResourceServer()` authenticates a **Bearer token**. One `SecurityFilterChain` that only calls `oauth2Login()` will **401** machine callers. `InMemoryOAuth2AuthorizedClientService` is **dev-only**.

> [!tip] Interview answer
> I implement browser SSO with OIDC: security-oauth2-client, a client registration with authorization_code and the openid scope, issuer-uri, and oauth2Login on the filter chain. Redirects go to /login/oauth2/code/{id}. APIs are resource servers with the same issuer. I do not use EnableOAuth2Sso. SAML2 is the other Boot-supported SSO path for older IdPs.
