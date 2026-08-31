<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is AuthenticationManager and AuthenticationProvider in Spring Security?

> [!abstract] Short answer
> **`AuthenticationManager`** is the **entry API**: **`authenticate(Authentication)`** returns a **fully populated** token (authorities included) or throws **`AuthenticationException`**. Stock implementation is **`ProviderManager`**. **`AuthenticationProvider`** is **one strategy** on that manager: **`supports(Class)`** is the **type gate**; **`authenticate`** returns a **trusted `Authentication`**, **`null`** (try the next), or throws. Filters call the **manager**, never a provider directly. **`DaoAuthenticationProvider`** handles **`UsernamePasswordAuthenticationToken`**. A JWT resource server uses a **different token type**, so it does **not** “fall into” LDAP/DAO.

## Manager is the process; providers are the checks

Architecture: a filter builds an **unauthenticated** **`Authentication`** and calls **`AuthenticationManager`**. You store the **result** on **`SecurityContext`**, not the manager ([[What is the difference between Authentication and AuthenticationManager]], [[What is UsernamePasswordAuthenticationToken]]).

**`AuthenticationManager`** (**`@FunctionalInterface`**) contract, in order when the manager can test the state: **`DisabledException`**, **`LockedException`**, then **always** credential checking (**`BadCredentialsException`**). **`ProviderManager`** does **not** check the password itself — it walks **`List<AuthenticationProvider>`** ([[What is ProviderManager in Spring Security]]).

**`AuthenticationProvider`**:

| Result | Meaning |
| --- | --- |
| **`supports` false** | Skip (wrong `Authentication` class) |
| **`authenticate` → token** | This provider **decided**; later ones are skipped |
| **`null`** | Decline; next provider |
| **`AuthenticationException`** | Fail — **`AccountStatusException` / `InternalAuthenticationServiceException` abort** the list (**SEC-546**); **`BadCredentialsException`** is **remembered** and the list **continues** |

**`DaoAuthenticationProvider`** **`supports` only `UsernamePasswordAuthenticationToken`**. LDAP bind uses the **same** token type — **order and abort rules matter**. **`JwtAuthenticationProvider`** **`supports` JWT tokens**, not form/Basic tokens. Dump “JWT sent to LDAP → 401 because of list order” is the **wrong** failure mode; **`supports`** already separates those types ([[What is DaoAuthenticationProvider]], [[How do you configure multiple AuthenticationProviders in Spring Security]]).

Register with **`HttpSecurity.authenticationProvider(...)`**, **`new ProviderManager(first, second)`**, or **`AuthenticationManagerBuilder`**. **`InitializeAuthenticationProviderBeanManagerConfigurer` (since 4.1)** picks up a **single** **`AuthenticationProvider` `@Bean`** only if the builder is still empty; **two beans are ignored**. **`@Order` on provider beans is not the list order** — pass an explicit list ([[How do you configure a custom AuthenticationProvider in Spring Security]]). Success tokens: **`UsernamePasswordAuthenticationToken.authenticated(...)` (since 5.7)**; do **not** return the two-arg constructor ([[What is an authenticated versus unauthenticated UsernamePasswordAuthenticationToken]]).

```java
AuthenticationManager manager = new ProviderManager(List.of(daoProvider, ldapProvider));
Authentication result = manager.authenticate(
	UsernamePasswordAuthenticationToken.unauthenticated(username, password));
```

**Listing 1.** Manager API. **DAO then LDAP**: a **bad password** from DAO does **not** by itself skip LDAP; a **locked** account **does**.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 2.** The filter holds an **`AuthenticationManager`** (usually **`ProviderManager` + `DaoAuthenticationProvider`** when a **`UserDetailsService`** is present).

```d2
direction: down
filter: "UsernamePasswordAuthenticationFilter\nhttpBasic / x509 / …" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
mgr: "AuthenticationManager\nProviderManager" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
p1: "AuthenticationProvider\nsupports + authenticate" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
p2: "next provider if null" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

filter -> mgr -> p1
p1 -> p2: "null"
```

**Fig. 1.** The **manager** is what filters call. **Providers** are the pluggable checks.

> [!warning] `supports` is the type gate, not `@Order`
> Form/Basic never invoke a JWT provider. Two **`@Bean AuthenticationProvider`s** are **not** auto-chained. **`ProviderNotFoundException`** means no provider **supported** the token (or all returned **`null`**), not “bad password.” Hidden **`UsernameNotFoundException`** is **`BadCredentialsException`** on DAO ([[What is UsernameNotFoundException]]).

> [!warning] Returning `null` from your only provider is not success
> **`null`** means **skip**. A custom provider that always returns **`null`** yields **`ProviderNotFoundException`**. Returning the **unauthenticated** two-arg token leaves **`isAuthenticated() == false`**. After success, **`eraseCredentials()`** (default **on**) clears secrets on the result.

> [!tip] Interview answer
> AuthenticationManager.authenticate is the API filters call. ProviderManager implements it by asking AuthenticationProviders in order: supports is the type check; authenticate returns a trusted token, null to skip, or throws. DaoAuthenticationProvider is the username/password provider. JWT uses a different Authentication type so it does not race DAO. I wire an explicit list when I have more than one provider; I do not rely on @Order on two provider beans.
