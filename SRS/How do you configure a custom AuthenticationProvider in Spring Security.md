<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure a custom AuthenticationProvider in Spring Security?

> [!abstract] Short answer
> Implement **`AuthenticationProvider`**: **`supports(Class)`** names the `Authentication` types you handle; **`authenticate`** returns a **trusted** `Authentication` (authorities included), **`null`** to skip, or throws **`AuthenticationException`**. Register it with **`HttpSecurity.authenticationProvider(...)`**, an explicit **`ProviderManager`**, or **`AuthenticationManagerBuilder.authenticationProvider(...)`**. A **single** `AuthenticationProvider` **bean** is picked up only when the global builder is still empty.

## Implement the provider, then put it on a `ProviderManager`

Filters call **`AuthenticationManager.authenticate`**. The usual manager is **`ProviderManager`**, which walks a **list** of **`AuthenticationProvider`** instances. Each provider may succeed, fail, or decline so a later one can decide. If none can authenticate, the manager throws **`ProviderNotFoundException`** ([[What is ProviderManager in Spring Security]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]]).

```java
public final class CustomAuthenticationProvider implements AuthenticationProvider {

	@Override
	public Authentication authenticate(Authentication authentication) {
		String username = authentication.getName();
		String password = String.valueOf(authentication.getCredentials());
		if (!isValid(username, password)) {
			throw new BadCredentialsException("Bad credentials");
		}
		List<GrantedAuthority> authorities = List.of(new SimpleGrantedAuthority("ROLE_USER"));
		return UsernamePasswordAuthenticationToken.authenticated(
			username, authentication.getCredentials(), authorities);
	}

	@Override
	public boolean supports(Class<?> authentication) {
		return UsernamePasswordAuthenticationToken.class.isAssignableFrom(authentication);
	}

	private boolean isValid(String username, String password) {
		return false; // replace with real checks
	}
}
```

**Listing 1.** Conceptual provider. **`supports`** is a type gate, not a guarantee of success — `authenticate` may still return **`null`** so the next supporting provider runs. Success must be a **fully populated** `Authentication` (principal + **authorities**). Failure is **`AuthenticationException`**, not an unauthenticated token. Username/password is typical; a SAML/JWT provider would `supports` a different token type ([[What is DaoAuthenticationProvider]], [[What is UsernamePasswordAuthenticationToken]]).

```d2
direction: down
filter: "Filter / controller\nAuthentication request" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
pm: "ProviderManager" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
custom: "CustomAuthenticationProvider\nsupports? authenticate" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
next: "Next AuthenticationProvider\nor ProviderNotFoundException" {
  width: 300
  height: 70
  style.fill: "#f3e5f5"
}

filter -> pm -> custom
custom -> next
```

**Fig. 1.** Your class is one strategy on the list. `ProviderManager` tries providers in order until one returns non-null.

## Three registration styles (Spring Security 7.1)

**1. Additional provider on the filter chain** — `HttpSecurity.authenticationProvider` *adds* a provider to the manager that chain uses:

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http,
		CustomAuthenticationProvider custom) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.formLogin(Customizer.withDefaults())
		.authenticationProvider(custom);
	return http.build();
}
```

**Listing 2.** DSL add. Call it once per extra provider. This does **not** by itself remove **`DaoAuthenticationProvider`** if a `UserDetailsService` still built the default manager.

**2. Exclusive `ProviderManager`** — you control the exact list (and can publish the manager for a `@Controller` / `@Service`):

```java
@Bean
AuthenticationManager authenticationManager(CustomAuthenticationProvider custom) {
	return new ProviderManager(custom);
}
```

**Listing 3.** Only `custom` runs. Wire it with **`http.authenticationManager(authenticationManager)`** when this chain must not fall back to the global manager. `ProviderManager` also accepts a **parent** manager used only when local providers cannot authenticate.

**3. Global `AuthenticationManagerBuilder`** — still valid: `@Autowired void configure(AuthenticationManagerBuilder auth) { auth.authenticationProvider(custom); }`. XML: `<authentication-provider ref="myAuthenticationProvider"/>` inside `<authentication-manager>`.

A **`@Bean AuthenticationProvider`** is applied to the **global** manager only when **all** of these hold (source of `InitializeAuthenticationProviderBeanManagerConfigurer`, since **4.1**): the builder is **not** already configured, and the context has **exactly one** `AuthenticationProvider` bean. Zero beans: skip. **Two or more**: none of them are auto-wired — log says to publish a single bean or use the DSL.

> [!warning] Two-arg `UsernamePasswordAuthenticationToken` is not a successful login
> That constructor (and **`unauthenticated(...)`**, since **5.7**) sets **`isAuthenticated()` to `false`**. Providers must return the **three-arg** constructor or **`UsernamePasswordAuthenticationToken.authenticated(principal, credentials, authorities)`**. Calling **`setAuthenticated(true)`** on a two-arg token throws **`IllegalArgumentException`**. Empty **authorities** still counts as authenticated, but **`hasRole` / `hasAuthority`** then have nothing to match ([[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]], [[What is GrantedAuthority in Spring Security]]).

> [!warning] `null` vs throw vs a later `DaoAuthenticationProvider`
> Returning **`null`** means “not my decision.” Throwing **`BadCredentialsException`** is a decision, but **`ProviderManager`** still tries **later** supporting providers; a later success **replaces** that exception. **`AccountStatusException`** stops the list. If this provider must be the **only** username/password checker, give the chain a **`ProviderManager` that contains only it** — do not leave the default DAO provider on the same list.

> [!warning] Several `AuthenticationProvider` beans are silently unused
> Auto-config wires **one** bean, and only if `AuthenticationManagerBuilder` is empty. Multiple beans, or a builder already filled by `inMemoryAuthentication()` / `userDetailsService()`, leave your beans off the global manager. Register with **`http.authenticationProvider`** or **`new ProviderManager(...)`**.

> [!tip] Interview answer
> I implement AuthenticationProvider: supports filters the Authentication class, authenticate returns a trusted token with authorities, null, or AuthenticationException. I add it with HttpSecurity.authenticationProvider or wrap it in a ProviderManager when I need an exclusive list. A single AuthenticationProvider bean is auto-registered only if the global builder is empty; two beans are ignored. I never return the two-arg UsernamePasswordAuthenticationToken as success.
