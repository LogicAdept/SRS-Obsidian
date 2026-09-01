<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/OAuth2 #Security/OIDC #Java/Spring/Security/Authentication #SRS

# When should you use OAuth2 login versus form login?

> [!abstract] Short answer
> **`formLogin()`** when **this app owns** usernames and passwords (`UserDetailsService` / `DaoAuthenticationProvider`, **POST `/login`**, session). **`oauth2Login()`** when **identity is delegated** to Google, GitHub, Keycloak, or another OIDC provider: authorization-code (the user types the **IdP** password, never yours). Both end in a **browser session**. **HTTP Basic** is for **machine** clients that send `Authorization: Basic` on each request — not a login page. **`oauth2ResourceServer()`** is an **API** that checks **Bearer** tokens, not a login mechanism.

## Who stores the password?

| | Form login | OAuth2 / OIDC login |
| --- | --- | --- |
| DSL | **`http.formLogin()`** | **`http.oauth2Login()`** |
| Credential POST | **`username` / `password`** to **this** app | **None** to this app — browser goes to the **authorization server** |
| Typical store | **`UserDetailsService`**, JDBC, LDAP | **`ClientRegistration`** (client-id/secret for the **RP**) |
| Filters | **`UsernamePasswordAuthenticationFilter`** | **`OAuth2AuthorizationRequestRedirectFilter`** + **`OAuth2LoginAuthenticationFilter`** |
| Default `/login` | Generated **form** | Generated **links** named by **`ClientRegistration.clientName`** |
| CSRF on login POST | **Required** | N/A (redirect grant) |

You **may** enable **both** on one chain. **`DefaultLoginPageGeneratingFilter`** can show the form **and** OAuth client links (`setFormLoginEnabled` / `setOauth2LoginEnabled`). That is local users **plus** “Sign in with Google,” not two resource-server modes ([[How do you use form login authentication in Spring Boot]], [[How do you implement OAuth2 login in Spring Security]], [[What is DefaultLoginPageGeneratingFilter]]).

```java
http.formLogin(Customizer.withDefaults());
http.oauth2Login(Customizer.withDefaults());
```

**Listing 1.** Left: this app checks passwords. Right: **authorization code** / OIDC; register a **`ClientRegistration`**. HTTP Basic is **`http.httpBasic()`** for curl/machines ([[When should you use HTTP Basic versus form login]], [[What is the OAuth2 authorization code grant in Spring Security]]).

```d2
direction: down
browser: "Browser" {
  width: 120
  height: 32
  style.fill: "#e3f2fd"
}
form: "formLogin()\nPOST /login → UserDetailsService" {
  width: 280
  height: 48
  style.fill: "#fff3e0"
}
oauth: "oauth2Login()\nredirect to IdP" {
  width: 240
  height: 48
  style.fill: "#c8e6c9"
}
rs: "oauth2ResourceServer()\nBearer JWT — not login" {
  width: 260
  height: 48
  style.fill: "#ffcdd2"
}

browser -> form: "owns passwords"
browser -> oauth: "delegates identity"
```

**Fig. 1.** A JSON API that only validates tokens uses **`oauth2ResourceServer()`**, often on a **separate** `SecurityFilterChain` from the UI ([[What is the difference between an OAuth2 client and a resource server]], [[How do you configure JWT and form login as two SecurityFilterChain beans]]).

> [!warning] `oauth2Login` is not a resource server
> Login starts a **session** after the code grant. **`oauth2ResourceServer().jwt()`** never shows `/login`. Putting **`issuer-uri`** only under **`resourceserver`** does **not** create Google/GitHub buttons. **`@EnableOAuth2Sso`** is the old client annotation, not form login.

> [!warning] OAuth2 login is not the password grant
> Collecting the **IdP** password in your form and POSTing `grant_type=password` is **forbidden** (RFC 9700) and **removed** in Security **7**. Form login means **your** `UserDetailsService`. Keycloak/Google users belong on **`oauth2Login()`** ([[How do you integrate Keycloak with Spring Security]], [[How does form login work internally in Spring Security]]).

> [!tip] Interview answer
> Form login when the app stores and checks passwords: POST /login, session, CSRF. oauth2Login when an IdP authenticates the user with authorization code / OIDC and this app never sees that password. Both are browser sessions. HTTP Basic is for simple clients with Authorization: Basic. oauth2ResourceServer validates Bearer tokens on an API and is not a login page.
