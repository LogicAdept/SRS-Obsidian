<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure multiple AuthenticationProviders in Spring Security?

> [!abstract] Short answer
> Put several **`AuthenticationProvider`** instances on one **`ProviderManager`**. Call **`HttpSecurity.authenticationProvider(...)`** once per extra provider, or construct **`new ProviderManager(first, second)`**. **`supports(Class)`** is a type gate; **`authenticate`** returns a trusted **`Authentication`**, **`null`** (try the next), or throws. The **first non-null** result wins. **Two `@Bean` providers are not auto-wired** — use the DSL or an explicit manager.

## One manager, a list of strategies

**`ProviderManager`** is the usual **`AuthenticationManager`**. It walks its **`List<AuthenticationProvider>`** in order. Each provider may succeed, fail, or decline so a later one can decide. If none authenticate, it throws **`ProviderNotFoundException`**, then tries an optional **parent** manager ([[What is ProviderManager in Spring Security]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]]).

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http,
		LdapAuthenticationProvider ldap,
		DaoAuthenticationProvider dao) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.httpBasic(Customizer.withDefaults())
		.authenticationProvider(ldap)
		.authenticationProvider(dao);
	return http.build();
}
```

**Listing 1.** **`HttpSecurity.authenticationProvider`** *adds* a provider (call it **per** extra implementation). Typical mix: LDAP bind plus **`DaoAuthenticationProvider`** for local users ([[What is DaoAuthenticationProvider]], [[How do you configure LDAP authentication in Spring Security]]).

```java
@Bean
AuthenticationManager authenticationManager(
		CustomAuthenticationProvider custom,
		DaoAuthenticationProvider dao) {
	return new ProviderManager(custom, dao);
}
```

**Listing 2.** Exclusive list you control. Use **`http.authenticationManager(...)`** when this chain must not keep the global DAO manager. **`AuthenticationManagerBuilder.authenticationProvider(...)`** can be chained the same way (`auth.inMemoryAuthentication()` and `auth.jdbcAuthentication()` each add a provider).

A **single** `AuthenticationProvider` **bean** is applied to the global manager only if the builder is still empty (`InitializeAuthenticationProviderBeanManagerConfigurer`, since **4.1**). **Two or more beans: none of them are auto-registered** — log tells you to publish one bean or use the DSL ([[How do you configure a custom AuthenticationProvider in Spring Security]]).

```d2
direction: down
token: "UsernamePasswordAuthenticationToken" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
pm: "ProviderManager" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
a: "Provider A\nsupports? authenticate" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
b: "Provider B\nor parent / ProviderNotFoundException" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

token -> pm -> a -> b
```

**Fig. 1.** Same `Authentication` type can be offered to several providers. **`supports`** is not a guarantee of success.

## `supports`, `null`, throw, order

**`supports(Class)`** means the provider can **evaluate** that `Authentication` class. It may still return **`null`** from **`authenticate`** so the next supporting provider runs.

| `authenticate` result | Meaning |
| --- | --- |
| Non-null `Authentication` | This provider **decided success**. **No later provider is tried.** |
| `null` | Cannot decide; try the next that **`supports`** the type |
| `AuthenticationException` | Failure from this provider. A **later** supporting provider may still **succeed** and **replace** that exception |
| `AccountStatusException` | **Stop** the list (locked/disabled, …) |

So “first success wins” is exact. “First that `supports` wins” is **not**: a `BadCredentialsException` from DAO does **not** by itself block LDAP if LDAP is later and also supports username/password.

> [!warning] A greedy `supports` plus a non-null return shadows everyone after
> If provider A **`supports`** `UsernamePasswordAuthenticationToken` and returns an authenticated token, LDAP/JWT providers **never run**. Put the **narrowest** / **most specific** provider **first** only if it returns **`null`** when the credentials are not for it. If it should be the **only** username/password checker, give the chain a **`ProviderManager` that contains only it**.

> [!warning] `null` is skip; throw is a decision — except later success can override
> Returning an **unauthenticated** two-arg **`UsernamePasswordAuthenticationToken`** is **not** success. Empty **authorities** still authenticate but **`hasRole`** has nothing to match. Do not register multiple providers as beans and expect them all to be used.

> [!tip] Interview answer
> ProviderManager tries AuthenticationProviders in list order. I add each with HttpSecurity.authenticationProvider or pass them to new ProviderManager. supports is a type filter; authenticate returns a trusted token, null, or AuthenticationException. The first non-null success wins; AccountStatusException stops the list. Two AuthenticationProvider beans are ignored by auto-config — I wire them on the DSL.
