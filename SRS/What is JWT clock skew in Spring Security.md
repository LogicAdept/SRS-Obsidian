<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/OAuth2 #Security/JWT #Security/OAuth2 #SRS

# What is JWT clock skew in Spring Security?

> [!abstract] Short answer
> Leeway **`JwtTimestampValidator`** applies when comparing **`exp`** and **`nbf`** to **now**. Resource Server default is **60 seconds**. A JWT is expired only if **`now - skew` is after `exp`**; too early only if **`now + skew` is before `nbf`**. Auth-server clocks a few minutes ahead still yield **401** (`invalid_token`). Widen with **`new JwtTimestampValidator(Duration…)`** on **`NimbusJwtDecoder.setJwtValidator`**. Confirm **DEBUG**: **`Jwt expired at …`**, not a missing Bearer.

## `exp` / `nbf` plus drift

JWT resource-server docs: every machine can drift, so tokens look expired on one node and valid on another. The validator is an **`OAuth2TokenValidator<Jwt>`** (since 5.1). Default constructor uses **`Duration.of(60, SECONDS)`**. **`Clock.systemUTC()`** unless you **`setClock`**.

```java
if (expiry != null && Instant.now(clock).minus(clockSkew).isAfter(expiry)) {
	// Jwt expired at {exp}
}
if (notBefore != null && Instant.now(clock).plus(clockSkew).isBefore(notBefore)) {
	// Jwt used before {nbf}
}
```

**Listing 1.** Effective window is **`[nbf − skew, exp + skew]`**. Empty **`exp`/`nbf`** are allowed by default (7.0 flags **`allowEmptyExpiryClaim` / `allowEmptyNotBeforeClaim`**).

Boot `issuer-uri` already installs this validator at **60s**. To change it you **replace** the decoder’s validator list — include **issuer** again or you drop **`iss`**:

```java
@Bean
JwtDecoder jwtDecoder() {
	NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuerUri);
	decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
			new JwtTimestampValidator(Duration.ofMinutes(2)),
			new JwtIssuerValidator(issuerUri)));
	return decoder;
}
```

**Listing 2.** Official composition. **`Duration.ofSeconds(60)`** in the docs is the **default**, not a “fix”. A larger **`Duration`** is the dump’s staging knob ([[How do you debug a silent 401 from an OAuth2 resource server]], [[How do you refresh an expired JWT in Spring Security]]).

```d2
direction: down
as: "Authorization Server\nclock" {
  width: 180
  height: 40
  style.fill: "#fff3e0"
}
jwt: "JWT exp / nbf" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
rs: "Resource Server\nJwtTimestampValidator\n±60s default" {
  width: 220
  height: 56
  style.fill: "#c8e6c9"
}

as -> jwt
jwt -> rs
```

**Fig. 1.** Skew is **resource-server JWT validation**, not refresh. **`OAuth2AuthorizedClientProvider.setClockSkew`** (client credentials / refresh) is a **different** 60s on the **client**. Widening that bean does not stop API **401**s ([[Why should you not catch Exception when validating a JWT]]).

Failure is **`OAuth2Error` `invalid_token`** with description **`Jwt expired at …`** / **`Jwt used before …`** (DEBUG on **`JwtTimestampValidator`**). TRACE on **`org.springframework.security`** if the body is empty.

> [!warning] Minutes of drift still miss a 60s window
> Several minutes ahead on the issuer → **401** even with the default. NTP the hosts first. A huge skew **accepts expired tokens**. That is not refresh ([[How do you refresh an expired JWT in Spring Security]]).

> [!warning] `setJwtValidator` replaces the whole list
> A validator that is **only** `JwtTimestampValidator` drops **`JwtIssuerValidator`**. Copy the docs’ **`DelegatingOAuth2TokenValidator`**. Do not `catch (Exception)` around decode to “fix” clocks.

> [!tip] Interview answer
> Clock skew is JwtTimestampValidator’s 60-second leeway on exp and nbf so small NTP drift does not 401 a still-fresh JWT. Configure a larger Duration on NimbusJwtDecoder if clocks are worse; sync time before widening. Client-provider clockSkew is a separate setting.
