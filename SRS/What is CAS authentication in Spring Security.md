<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is CAS authentication in Spring Security?

> [!abstract] Short answer
> **CAS** here is the **JA-SIG / Apereo Central Authentication Service** (enterprise SSO) — **not** compare-and-swap. The app is a CAS **service**: **`CasAuthenticationEntryPoint`** redirects the browser to the **CAS login URL** with a **`service`** callback. CAS returns **`/login/cas?ticket=ST-…`**. **`CasAuthenticationFilter`** (default process URL **`/login/cas`**) builds an **unauthenticated `CasServiceTicketAuthenticationToken`** (**since 6.1**). **`CasAuthenticationProvider`** validates the ticket with an Apereo **`TicketValidator`** (HTTPS to CAS), loads **authorities** via **`UserDetailsService`** (**password unused**), and returns a **`CasAuthenticationToken`** with **`FACTOR_CAS`**. There is **no** `http.cas()` DSL — you add the filter at **`CAS_FILTER`**.

## Ticket, not a local password POST

Listed with form login, OAuth2, SAML, remember-me, JAAS, and X.509 ([[What authentication mechanisms does Spring Security support]]). Sequence from the servlet CAS chapter:

1. Protected resource → **`ExceptionTranslationFilter`** → **`CasAuthenticationEntryPoint.commence`** ([[What is ExceptionTranslationFilter in Spring Security]], [[What is AuthenticationEntryPoint]]).
2. Redirect to CAS **`loginUrl`** plus **`service`** = this app’s callback (**`ServiceProperties.service`**, must match the filter URL).
3. After CAS login, browser returns with opaque **`ticket`**.
4. **`CasAuthenticationFilter`** (`AbstractAuthenticationProcessingFilter`) creates **`CasServiceTicketAuthenticationToken.stateful(ticket)`** (principal **`CAS_STATEFUL_IDENTIFIER`**, credentials = ticket). Older reference text still says **`UsernamePasswordAuthenticationToken`** — **7.1** uses the CAS token type.
5. **`CasAuthenticationProvider`** calls **`TicketValidator.validate`**, **`UserDetailsByNameServiceWrapper`**, **`AccountStatusUserDetailsChecker`** (**`setUserDetailsChecker` since 6.4**), then **`CasAuthenticationToken`** + **`FactorGrantedAuthority.CAS_AUTHORITY`**. (The same chapter’s “**FACTOR_BEARER**” wording does **not** match the provider.)
6. Success handler / saved request like form login.

**`sendRenew=true`** on **`ServiceProperties`** forces CAS to re-prompt (no SSO cookie reuse). Proxy tickets: **`authenticateAllArtifacts`**, **`Cas20ProxyTicketValidator`**, **`proxyReceptorUrl`**, **`StatelessTicketCache`**. Proxy success **continues the chain** and **skips** **`AuthenticationSuccessHandler`**.

**Single logout** is **not** `http.logout()` alone: local logout leaves the CAS TGT. Official pattern: extra **`LogoutFilter`** to the CAS **`/logout`**, Apereo **`SingleSignOutFilter`** + **`SingleSignOutHttpSessionListener`** for back-channel SLO ([[How do you implement logout in Spring Security]]).

```java
CasAuthenticationEntryPoint casEntryPoint = new CasAuthenticationEntryPoint();
casEntryPoint.setLoginUrl(casServerLogin); // enterprise CAS /login
casEntryPoint.setServiceProperties(serviceProperties);

http
	.exceptionHandling((ex) -> ex.authenticationEntryPoint(casEntryPoint))
	.addFilter(casFilter);
```

**Listing 1.** **`CasAuthenticationFilter`** is a **custom filter**, not `formLogin`. **`ServiceProperties.service`** must be the same callback the filter processes (**`/login/cas`** by default).

```java
CasAuthenticationProvider provider = new CasAuthenticationProvider();
provider.setTicketValidator(ticketValidator); // Apereo Cas20ServiceTicketValidator
provider.setAuthenticationUserDetailsService(new UserDetailsByNameServiceWrapper<>(users));
provider.setKey("unique-to-this-app");
```

**Listing 2.** Ticket proof is **CAS validation**. **`UserDetailsService`** only supplies **roles**; it does **not** check the password ([[What is AuthenticationManager and AuthenticationProvider in Spring Security]]).

```d2
direction: down
app: "protected resource" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
ep: "CasAuthenticationEntryPoint\nredirect to CAS /login" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cas: "CAS server\nusername/password" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}
flt: "CasAuthenticationFilter\n/login/cas?ticket=" {
  width: 260
  height: 70
  style.fill: "#fff8e1"
}
prv: "CasAuthenticationProvider\nTicketValidator + UserDetails" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

app -> ep -> cas -> flt -> prv
```

**Fig. 1.** Passwords are entered **on CAS**. The service only **validates tickets**.

> [!warning] Not compare-and-swap, not `formLogin`
> Wiring **`formLogin`** does **not** talk to CAS. The servlet reference still shows **XML `custom-filter position="CAS_FILTER"`**; **HttpSecurity** has **no** `cas()` **Customizer**. **`UserDetails.password`** is ignored — a matching local hash is **not** how CAS proves the user.

> [!warning] Local logout is not SSO logout
> **`http.logout()`** clears **this** session only. Other CAS services stay signed in until you redirect to the CAS logout URL and handle **`SingleSignOutFilter`**. In-memory **`ProxyGrantingTicketStorageImpl`** is **not** for production (official note).

> [!tip] Interview answer
> CAS is Apereo SSO: CasAuthenticationEntryPoint sends the browser to the CAS server, which returns a service ticket to /login/cas. CasAuthenticationFilter wraps that ticket in CasServiceTicketAuthenticationToken; CasAuthenticationProvider validates it with a TicketValidator and loads authorities without using the local password. The result is a CasAuthenticationToken with FACTOR_CAS. I do not confuse it with compare-and-swap or with oauth2Login.
