<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you implement custom token-based authentication in Spring Security?

> [!abstract] Short answer
> Prefer **`oauth2ResourceServer`** when the token is a **JWT** or **OAuth2 opaque** bearer. For a **proprietary** token, do **not** stuff a header into **`SecurityContextHolder`**. Use **`AuthenticationFilter`** (since **5.2**): an **`AuthenticationConverter`** builds an **unauthenticated** `Authentication`, an **`AuthenticationManager` / `AuthenticationProvider`** **validates** it, then the filter sets the context. Pair with **`SessionCreationPolicy.STATELESS`**. Replace the default **success handler** so the request **continues** into the API instead of a login redirect.

## Convert, authenticate, then continue the chain

Official bearer support is **`oauth2ResourceServer`** + **`BearerTokenAuthenticationFilter`** ([[What is BearerTokenAuthenticationFilter]], [[How do you configure JWT and form login as two SecurityFilterChain beans]]). A home-grown JWT parser duplicates signature, `iss`, `aud`, and clock-skew checks.

A custom scheme uses the same shape as form login ([[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[How do you configure a custom AuthenticationProvider in Spring Security]], [[What is OncePerRequestFilter]]):

1. **`AuthenticationConverter.convert`**: read a header (often `Authorization`). Return **`null`** if absent (no attempt). Throw **`AuthenticationException`** if the scheme is malformed. Return an **unauthenticated** token (`AbstractAuthenticationToken` with **`isAuthenticated() == false`**). Implementations should stay **immutable** after the provider authenticates.
2. **`AuthenticationManager.authenticate`**: a **`supports`**-matching **`AuthenticationProvider`** looks up or verifies the secret, expiry, and authorities. Failure → **`BadCredentialsException`** (or similar). Success → a **new** authenticated `Authentication`.
3. **`AuthenticationFilter`** (extends **`OncePerRequestFilter`**) sets **`SecurityContextHolder`**, saves via **`RequestAttributeSecurityContextRepository`** (this request only; default is **not** the HTTP session), then **`AuthenticationSuccessHandler`**. Failure uses **`AuthenticationEntryPointFailureHandler`** wrapping **`HttpStatusEntryPoint(UNAUTHORIZED)`** (**401**).

Default **success** handler is **`SavedRequestAwareAuthenticationSuccessHandler`** (form-login redirect). The 4-arg **`onAuthenticationSuccess`** (since **5.2**) still **`chain.doFilter`s** after the 3-arg method; a no-op 3-arg handler is how a token API **keeps processing** the resource. **`addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)`** is the documented place for an authentication filter.

**`SessionCreationPolicy.STATELESS`** installs **`NullSecurityContextRepository`** and skips saving the request for replay. Re-validate the token **every** request. Disable CSRF **only** for non-browser clients that do not send session cookies; a cookie-held token still needs CSRF.

```java
AuthenticationConverter converter = (request) -> {
	String header = request.getHeader(HttpHeaders.AUTHORIZATION);
	if (header == null) {
		return null;
	}
	if (!header.startsWith("Bearer ")) {
		throw new BadCredentialsException("Unsupported authorization scheme");
	}
	return UsernamePasswordAuthenticationToken.unauthenticated(header.substring(7), header.substring(7));
};

AuthenticationFilter tokenFilter = new AuthenticationFilter(
		new ProviderManager(apiTokenAuthenticationProvider()), converter);
tokenFilter.setSuccessHandler((request, response, authentication) -> { });
```

**Listing 1.** Convert → **`ProviderManager`**. The empty success handler lets the default 4-arg method **continue the filter chain**. Never mark the pre-auth token **`authenticated`**.

```java
@Bean
SecurityFilterChain api(HttpSecurity http, AuthenticationFilter tokenFilter) throws Exception {
	http
		.csrf((csrf) -> csrf.disable())
		.sessionManagement((session) -> session
			.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
		.addFilterBefore(tokenFilter, UsernamePasswordAuthenticationFilter.class)
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.exceptionHandling((exceptions) -> exceptions
			.authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED)));
	return http.build();
}
```

**Listing 2.** Stateless API chain. **`csrf.disable()`** is for **bearer-in-header, no cookie session** — not a default for browser apps. Missing token: converter returns **`null`**, anonymous/unauthenticated then **401** from the entry point ([[How do you handle authentication exceptions in Spring Security]]).

```d2
direction: down
req: "Authorization: Bearer …" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
conv: "AuthenticationConverter\nnull = skip" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
mgr: "AuthenticationProvider\nvalidate token" {
  width: 240
  height: 70
  style.fill: "#fce4ec"
}
ctx: "SecurityContextHolder\nrequest attribute only" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
api: "AuthorizationFilter\nthen controller" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

req -> conv -> mgr -> ctx -> api
```

**Fig. 1.** The provider is the trust boundary. The filter only **moves** a verified `Authentication`.

> [!warning] Header ≠ authentication
> Copying `Authorization` onto **`SecurityContextHolder`** without **`AuthenticationManager`** is a **forged-header** hole. The converter must not call **`setAuthenticated(true)`**. Leave the default **success handler** and a valid token **redirects** instead of invoking the controller.

> [!warning] Form login + sessions is a different app
> **`STATELESS`** does not magically ignore a leftover **`formLogin`**. Two mechanisms belong on **two `SecurityFilterChain`s** (or one chain that truly needs both). **`csrf.disable()`** while still using **cookie** credentials re-opens CSRF.

> [!tip] Interview answer
> For JWT or opaque OAuth2 I use oauth2ResourceServer. For a proprietary token I use AuthenticationFilter: AuthenticationConverter reads the header into an unauthenticated token, AuthenticationProvider validates it, then I replace the success handler so the filter chain continues. I set SessionCreationPolicy.STATELESS so nothing is stored in the HTTP session, and I never trust a header without going through AuthenticationManager.
