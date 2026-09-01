<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Security/SAML #SRS

# What is SAML 2.0 support in Spring Security?

> [!abstract] Short answer
> The app is a **SAML 2.0 relying party / service provider**. Users log in at an **asserting party / identity provider** (Okta, ADFS, …) via the **Web Browser SSO Profile**. Module: **`spring-security-saml2-service-provider`** (OpenSAML, default **`OpenSaml5AuthenticationProvider`**). DSL: **`http.saml2Login()`**. Boot: **`RelyingPartyRegistrationRepository`** from asserting-party metadata. ACS: **`POST /login/saml2/sso/{registrationId}`** with **`SAMLResponse`**. It is **browser SSO with a session**, not **`oauth2ResourceServer().jwt()`**, not **`PasswordEncoder`**.

## Relying party, not a JWT API

Ported into Spring Security in **2019** (extension project since **2009**), same idea as OAuth 2.0 Login: redirect to a third party, then a local **`Authentication`**.

| SAML name | Also called |
| --- | --- |
| **Relying party (RP)** | Service provider — **your app** |
| **Asserting party (AP)** | Identity provider — **IdP** |

Flow: unauthenticated request → **`ExceptionTranslationFilter`** → **`Saml2WebSsoAuthenticationRequestFilter`** builds a signed **`AuthnRequest`** → browser to IdP → IdP POSTs **`SAMLResponse`** to the ACS → **`Saml2WebSsoAuthenticationFilter`** → **`OpenSaml5AuthenticationProvider`** (signature, decrypt, Issuer/Destination, assertion times, **`NameID`**) → **`Saml2Authentication`** / **`Saml2AuthenticatedPrincipal`**. Authorities include **`FACTOR_SAML_RESPONSE`** and **`ROLE_USER`**.

You must **already register this RP** with the IdP. Boot needs asserting-party metadata (`spring.security.saml2.relyingparty.registration.{id}…` or a metadata document). OpenSAML artifacts come from the **Shibboleth** Maven repository (separate from Maven Central).

```java
@Bean
SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.saml2Login(Customizer.withDefaults());
	return http.build();
}

@Bean
RelyingPartyRegistrationRepository relyingPartyRegistrations() {
	RelyingPartyRegistration registration = RelyingPartyRegistrations
			.fromMetadataLocation(assertingPartyMetadataLocation)
			.registrationId("example")
			.build();
	return new InMemoryRelyingPartyRegistrationRepository(registration);
}
```

**Listing 1.** Boot already publishes these when the saml2 starter/metadata is present. **`registrationId`** is an arbitrary key (ACS path uses it) ([[How do you implement OAuth2 login in Spring Security]], [[How do you register a custom OAuth2 identity provider]]).

```d2
direction: down
app: "RP / saml2Login()" {
  width: 180
  height: 40
  style.fill: "#c8e6c9"
}
idp: "AP / IdP" {
  width: 140
  height: 36
  style.fill: "#fff3e0"
}
acs: "POST /login/saml2/sso/{id}\nSAMLResponse" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}

app -> idp: "AuthnRequest"
idp -> acs: "browser POST"
acs -> app: "Saml2Authentication"
```

**Fig. 1.** XML **assertions**, not a Bearer JWT. Other SSO knobs: **`oauth2Login()`** (OAuth/OIDC) and **CAS** ([[What is OAuth 2.0]], [[What is EnableOAuth2Sso]], [[What is CAS authentication in Spring Security]], [[What is JwtDecoder in Spring Security]]).

> [!warning] Not `oauth2ResourceServer().jwt()`
> SAML login starts a **session** after a **browser POST** of **`SAMLResponse`**. A resource server validates **`Authorization: Bearer`**. Mixing **`saml2Login`** with **`jwt()`** on one chain is two protocols, not “SAML as JWT.”

> [!warning] OpenSAML is required at runtime
> Missing Shibboleth repo / OpenSAML versions fail at **`AuthnRequest`** / response parse. Static **`OpenSamlInitializationService.initialize()`** if you touch OpenSAML types. Multi-IdP: more than one **`RelyingPartyRegistration`**; first hit is often a **picker**.

> [!tip] Interview answer
> Spring Security SAML 2.0 support is relying-party Web Browser SSO: saml2Login, RelyingPartyRegistration, OpenSAML. The IdP authenticates; your app consumes SAMLResponse at /login/saml2/sso/{id}. It sits next to OAuth2 login and CAS, not PasswordEncoder or JWT resource-server config.
