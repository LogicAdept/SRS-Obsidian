<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is JAAS support in Spring Security?

> [!abstract] Short answer
> Spring Security can **delegate username/password authentication to JAAS** (`javax.security.auth.login.LoginContext` / `LoginModule`) instead of **`DaoAuthenticationProvider`**. The integration is an **`AuthenticationProvider`**: **`AbstractJaasAuthenticationProvider`** plus **`DefaultJaasAuthenticationProvider`** (inject a JAAS **`Configuration`**, often **`InMemoryConfiguration`**) or **`JaasAuthenticationProvider`** (a **`login.conf` `ConfigFile`** via **`loginConfig`**). Success is a **`JaasAuthenticationToken`** (holds the **`LoginContext`**) with **`JaasGrantedAuthority`** values from your **`AuthorityGranter`s**, plus **`FACTOR_PASSWORD`**. There is **no** `http.jaas()` DSL. Most Boot apps never configure this.

## LoginModule, then map principals to authorities

JAAS is a **JDK** login SPI. Spring already collected username/password on an **`Authentication`** (typically form or Basic). It then creates a **`LoginContext`**, feeds **`NameCallback` / `PasswordCallback`** through **`JaasNameCallbackHandler`** and **`JaasPasswordCallbackHandler`** (defaults if you set none), and calls **`login()`** ([[How does form login work internally in Spring Security]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is DaoAuthenticationProvider]]).

JAAS “roles” are **principals on the `Subject`**. Spring needs **`GrantedAuthority`** strings, so each principal is passed to every **`AuthorityGranter.grant(Principal)`**. Returned names become **`JaasGrantedAuthority`**. Spring **ships no production granter** — NT groups, Unix groups, and custom principals are **your** mapping ([[What is GrantedAuthority in Spring Security]], [[What is a principal in Spring Security]]). On success it still adds **`FACTOR_PASSWORD`**.

**`supports`**: **`UsernamePasswordAuthenticationToken`**. Failure wraps **`LoginException`** in **`AuthenticationServiceException`** — this provider **does not** emit locked/disabled account exceptions. Session destroy calls **`LoginContext.logout()`** for a **`JaasAuthenticationToken`**.

**`JaasAuthenticationProvider`** expects the JVM default **`Configuration`** to be a **`ConfigFile`**; it sets **`login.config.url.X`**. Prefer **`DefaultJaasAuthenticationProvider` + injected `Configuration`** so you are not bound to that file. Default **`loginContextName`** is **`SPRINGSECURITY`**. Register the provider like any other ([[How do you configure a custom AuthenticationProvider in Spring Security]], [[What authentication mechanisms does Spring Security support]]).

**`JaasApiIntegrationFilter`** (`jaas-api-provision` in XML) runs the chain as **`Subject.doAs`** so legacy JAAS code can call **`Subject.getSubject(AccessController.getContext())`**.

```java
DefaultJaasAuthenticationProvider jaas = new DefaultJaasAuthenticationProvider();
AppConfigurationEntry module = new AppConfigurationEntry(
	"sample.SampleLoginModule",
	AppConfigurationEntry.LoginModuleControlFlag.REQUIRED,
	Map.of());
jaas.setConfiguration(new InMemoryConfiguration(
	Map.of("SPRINGSECURITY", new AppConfigurationEntry[] { module })));
jaas.setAuthorityGranters(new AuthorityGranter[] { granter });
```

**Listing 1.** Official shape in Java: inject **`Configuration`**, implement **`AuthorityGranter`**. **`JaasAuthenticationProvider.setLoginConfig(resource)`** is the **file** alternative (`JAASTest { … }` + **`loginContextName`**).

```java
http.authenticationProvider(jaas)
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 2.** Form login still produces **`UsernamePasswordAuthenticationToken`**. JAAS is the **provider**, not a second login page.

```d2
direction: down
tok: "UsernamePasswordAuthenticationToken" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
lc: "LoginContext.login\nLoginModule + callbacks" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
ag: "AuthorityGranter → JaasGrantedAuthority\n+ FACTOR_PASSWORD" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

tok -> lc -> ag
```

**Fig. 1.** Spring owns the HTTP login. JAAS owns **`LoginModule`**. You own the **principal → authority** map.

> [!warning] Listing JAAS is not using it
> Boot form/Basic uses **`DaoAuthenticationProvider` + `UserDetailsService`**. JAAS is an **optional provider** for shops that already have **`LoginModule`s**. There is **no** production **`AuthorityGranter`**. **`authenticate` does not** implement account-status flags. **`JaasAuthenticationProvider`** mutates JVM **`login.config.url.X`** — **`DefaultJaasAuthenticationProvider`** is the less coupled of the two.

> [!warning] Subject vs SecurityContext
> A populated **`SecurityContext`** is **not** a JAAS **`Subject`**. Code that calls **`Subject.getSubject`** needs **`JaasApiIntegrationFilter`** (and an authenticated **`JaasAuthenticationToken`**). **`LoginContext.logout`** runs on **session destroyed**, not merely a 302 to `/login`.

> [!tip] Interview answer
> Spring Security’s JAAS support is an AuthenticationProvider that calls LoginContext.login with the username and password already on the token, then maps Subject principals to GrantedAuthority through AuthorityGranter. I would use DefaultJaasAuthenticationProvider with an injected Configuration, not a global login.conf, and I would not confuse that with ordinary form login. Most applications never need it; UserDetailsService is the default path.
