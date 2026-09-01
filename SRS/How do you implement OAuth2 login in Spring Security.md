<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/OIDC #SRS

# How do you implement OAuth2 login in Spring Security?

> [!abstract] Short answer
> Put **`spring-security-oauth2-client`** on the classpath, register a **`ClientRegistration`** (Boot YAML or a **`ClientRegistrationRepository` bean**), and enable **`http.oauth2Login()`**. That is **authorization-code login** (OAuth 2.0 / OIDC): the user authenticates at the provider and Spring starts a **session**. It is **not** **`oauth2ResourceServer()`**, which validates **Bearer** tokens on an API.

## Client registration + `oauth2Login()`

Boot’s **`OAuth2ClientAutoConfiguration`** builds a **`ClientRegistrationRepository`** from `spring.security.oauth2.client.*` and a **`SecurityFilterChain`** that calls **`oauth2Login()`**. For Google (a **`CommonOAuth2Provider`** id), **`client-id`** and **`client-secret`** are enough — **`authorization-uri` / `token-uri` / `user-info-uri`** are pre-set when the **`registrationId`** is `google` (case-insensitive) or **`provider: google`**.

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          google:
            client-id: google-client-id
            client-secret: google-client-secret
```

**Listing 1.** Common provider. Custom issuers use **`spring.security.oauth2.client.provider.[id]`** (`authorization-uri`, `token-uri`, `user-info-uri`, `jwk-set-uri`, `user-name-attribute`) or OIDC **`issuer-uri`** (discovery). Login registrations typically set **`authorization-grant-type: authorization_code`** and **`redirect-uri: "{baseUrl}/login/oauth2/code/{registrationId}"`**.

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize
			.anyRequest().authenticated())
		.oauth2Login(Customizer.withDefaults());
	return http.build();
}
```

**Listing 2.** Current DSL. The dump’s **`authorizeRequests().and().oauth2Login()`** is the old matcher API. Without Boot, also expose **`ClientRegistrationRepository`**, **`OAuth2AuthorizedClientService`**, and **`OAuth2AuthorizedClientRepository`**.

```java
ClientRegistration google = CommonOAuth2Provider.GOOGLE.getBuilder("google")
	.clientId("google-client-id")
	.clientSecret("google-client-secret")
	.build();
```

**Listing 3.** Java config without repeating provider URLs. Grant type is **authorization code**.

Default protocol endpoints:

| Step | Default location |
| --- | --- |
| Start login (Authorization Request) | **`/oauth2/authorization/{registrationId}`** (`OAuth2AuthorizationRequestRedirectFilter`) |
| Provider callback (Authorization Response) | **`/login/oauth2/code/*`** (`OAuth2LoginAuthenticationFilter.DEFAULT_FILTER_PROCESSES_URI`) |
| Login page | Auto-generated links named by **`ClientRegistration.clientName`** |

Register the **same** callback at the provider (for Google: host + **`/login/oauth2/code/google`**). If you change **`redirectionEndpoint.baseUri`**, you **must** change **`ClientRegistration.redirectUri`** to match.

```d2
direction: down
app: "App oauth2Login()\nsession after success" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
redir: "/oauth2/authorization/{id}" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
idp: "Authorization server\n(code grant)" {
  width: 220
  height: 50
  style.fill: "#f3e5f5"
}
cb: "/login/oauth2/code/{id}" {
  width: 240
  height: 40
  style.fill: "#c8e6c9"
}

app -> redir
redir -> idp
idp -> cb
cb -> app
```

**Fig. 1.** Browser login. **`oauth2ResourceServer().jwt()`** never does this dance — it only checks a Bearer JWT ([[What is the difference between an OAuth2 client and a resource server]], [[What is the OAuth2 authorization code grant in Spring Security]], [[What is OAuth2AuthorizationRequestRedirectFilter]]).

Boot’s default **`InMemoryOAuth2AuthorizedClientService`** is for development; production should use **`JdbcOAuth2AuthorizedClientService`** (or your own). Custom providers: [[How do you register a custom OAuth2 identity provider]]. Versus form login: [[When should you use OAuth2 login versus form login]].

> [!warning] `oauth2Login` is not a resource server
> **`oauth2Login()`** is the **OAuth2 client** that **logs a user in**. **`oauth2ResourceServer()`** protects an API with a **JWT or opaque access token**. Enabling “OAuth2” with only **`issuer-uri`** under **`spring.security.oauth2.resourceserver`** does **not** give you a Google/GitHub login button.

> [!warning] Redirect URI is an exact string
> The provider’s registered redirect must match the processed pattern, including **`/login/oauth2/code/{registrationId}`**. A custom **`redirectionEndpoint.baseUri`** (for example **`/login/oauth2/callback/*`**) without updating **`redirect-uri`** yields a provider **`redirect_uri_mismatch`**. Behind a proxy, **`{baseUrl}`** must be the public URL.

> [!tip] Interview answer
> OAuth2 login is Spring Security’s client: ClientRegistration plus oauth2Login(), using the authorization code grant and, for Google-style providers, OIDC. Boot needs client-id and client-secret for CommonOAuth2Provider ids; the callback is /login/oauth2/code/{registrationId}. That is not oauth2ResourceServer, which validates bearer tokens instead of creating a browser session.
