<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you implement two-factor authentication in Spring Security?

> [!abstract] Short answer
> In **7.0+**, 2FA is **authorization of factors**, not a home-grown “half login.” Each mechanism adds a **`FactorGrantedAuthority`** (`FACTOR_PASSWORD`, `FACTOR_OTT`, `FACTOR_WEBAUTHN`, …). **`@EnableMultiFactorAuthentication(authorities = { PASSWORD_AUTHORITY, OTT_AUTHORITY })`** makes every `authenticated()` / `hasRole` rule also require those factors. Enable **`formLogin`** and **`oneTimeTokenLogin`** (or **WebAuthn**) so each factor can be obtained. Missing factors redirect to the matching login. **OTT is not TOTP** — Spring does **not** ship Google Authenticator; TOTP is a custom factor.

## Factors on Authentication, then authorize them

OWASP-style factors: something you **know**, **have**, **are**. At authentication time Spring attaches **`FactorGrantedAuthority`** (**since 7.0**) with **`issuedAt`**. MFA is: **(1)** require several of those authorities, **(2)** register a mechanism for each ([[How do you create a custom login form in Spring Security]]).

**`@EnableMultiFactorAuthentication`** publishes an **`AuthorizationManagerFactory`** so `hasRole("ADMIN")` also needs the listed factors. Empty **`authorities = {}`** only **enables** MFA wiring; then use **`AuthorizationManagerFactories.multiFactor().requireFactors(...).build()`** locally (for example `/admin/**` MFA, `/` password-only). **`permitAll` / `anonymous` / `denyAll`** are **not** wrapped. **`when(Authentication → boolean)`** (annotation **`when`** since **7.1**) applies MFA only for some users (or **`MultiFactorCondition.WEBAUTHN_REGISTERED`**). **`AllRequiredFactorsAuthorizationManager.anyOf`** allows **WebAuthn alone** *or* password+OTT. **`validDuration`** re-asks a factor that is too old. **Reactive MFA is not supported.**

A missing factor is **not** a 403-and-stop: the framework sends the user to the login that can issue that authority (**`defaultDeniedHandlerForMissingAuthority`**, **since 7.0**) ([[How do you handle authentication exceptions in Spring Security]]). Password-then-OTT: after form login, **`AuthorizationFilter`** fails for missing **`FACTOR_OTT`** and redirects to the OTT page. **`AuthenticationFilter.setMfaEnabled(true)`** **merges** authorities when the same principal completes a second factor.

**One-time token ≠ OTP.** Official OTT is a **server-generated** token (magic link / SMS) via **`oneTimeTokenLogin()`**. You **must** expose **`OneTimeTokenGenerationSuccessHandler`** — Spring will not email it for you. Default store is **`InMemoryOneTimeTokenService`**; production should use **`JdbcOneTimeTokenService`**. Default generate URL **`POST /ott/generate`**, submit **`GET /login/ott`**. **TOTP/HOTP** still means your own provider that grants a **`FactorGrantedAuthority`** (for example **`withFactor("totp")`**) and a **`requireFactors`** rule — not a Twilio filter bolted in front of **`UsernamePasswordAuthenticationFilter`**.

```java
@Configuration
@EnableWebSecurity
@EnableMultiFactorAuthentication(authorities = {
		FactorGrantedAuthority.PASSWORD_AUTHORITY,
		FactorGrantedAuthority.OTT_AUTHORITY
})
class SecurityConfig {

	@Bean
	SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
		http
			.authorizeHttpRequests((authorize) -> authorize
				.requestMatchers("/admin/**").hasRole("ADMIN")
				.anyRequest().authenticated()
			)
			.formLogin(Customizer.withDefaults())
			.oneTimeTokenLogin(Customizer.withDefaults());
		return http.build();
	}
}
```

**Listing 1.** Official global MFA. `/admin/**` needs **`ROLE_ADMIN` plus both factors**; everything else still needs **both factors**.

```java
@Bean
AuthorizationManagerFactory<Object> authz() {
	return AuthorizationManagerFactories.multiFactor()
		.requireFactors(
			FactorGrantedAuthority.PASSWORD_AUTHORITY,
			FactorGrantedAuthority.OTT_AUTHORITY)
		.build();
}
```

**Listing 2.** Same rules without the annotation shortcut. For **path-selective** MFA, **do not** publish this bean; call **`mfa.hasRole("ADMIN")`** / **`mfa.authenticated()`** only on the matchers that need two factors.

```d2
direction: down
pwd: "formLogin\nFACTOR_PASSWORD" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
ott: "oneTimeTokenLogin\nFACTOR_OTT" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
auth: "Authentication\nboth FactorGrantedAuthority" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
gate: "AuthorizationManager\nAllRequiredFactors" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}

pwd -> auth
ott -> auth
auth -> gate
```

**Fig. 1.** Second factor **adds** an authority. The user is already authenticated after password; they are **not** authorized for MFA routes until the second factor is present.

> [!warning] OTT is not Google Authenticator
> Dumps that say “Spring has no 2FA” are **stale** as of **7.0**. Dumps that wire Twilio **before** **`UsernamePasswordAuthenticationFilter`** and swap a flag on `Authentication` skip **`FactorGrantedAuthority`** and the missing-factor **entry point**. A filter that **`doFilter`s** without requiring the second factor is **not** MFA. In-memory OTT tokens vanish on restart.

> [!warning] Requiring factors without mechanisms
> `@EnableMultiFactorAuthentication` with **`FACTOR_OTT`** and **no** **`oneTimeTokenLogin`** leaves users **stuck** after password: the factor can never be issued. You still need a **delivery** bean for OTT. Do not treat **`authenticated()`** after password-only as “2FA complete” when a global factory is in play — **every** matcher except permit/deny/anonymous inherits the factors.

> [!tip] Interview answer
> I enable MFA with FactorGrantedAuthority: form login issues FACTOR_PASSWORD, one-time token login issues FACTOR_OTT, and @EnableMultiFactorAuthentication (or AuthorizationManagerFactories.multiFactor) requires both on the URLs that matter. Missing factors redirect to the login that can produce them. I do not confuse OTT magic links with TOTP; for authenticator apps I would grant my own factor authority and require it the same way.
