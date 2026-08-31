<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure LDAP authentication in Spring Security?

> [!abstract] Short answer
> Add **`spring-security-ldap`**, point a **`ContextSource`** at the directory, then publish an **`AuthenticationManager`** from **`LdapBindAuthenticationManagerFactory`** (bind is the usual mode). Search with **`userSearchBase` / `userSearchFilter`**, or a DN pattern **`uid={0},ou=people`**. Groups become **`GrantedAuthority`** via **`DefaultLdapAuthoritiesPopulator`**. LDAP **bind does not use `UserDetailsService`** — the server checks the password. Active Directory uses **`ActiveDirectoryLdapAuthenticationProvider`** (`user@domain`).

## Bind, not `DaoAuthenticationProvider`

LDAP username/password login still goes through **`AuthenticationManager`**, but **not** **`UserDetailsService`**: bind never returns the password (even hashed), so the app cannot compare locally. **`LdapAuthenticationProvider`** delegates to **`LdapAuthenticator`** (usually **`BindAuthenticator`**) and **`LdapAuthoritiesPopulator`**. Dependency: **`spring-security-ldap`** (Boot: also **`spring-boot-starter-data-ldap`**). Configure LDAP **connection pooling** on the JNDI side ([[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is DaoAuthenticationProvider]]).

A **`ContextSource`** is the LDAP equivalent of a JDBC **`DataSource`**:

```java
@Bean
AuthenticationManager authenticationManager(BaseLdapPathContextSource contextSource) {
	LdapBindAuthenticationManagerFactory factory =
		new LdapBindAuthenticationManagerFactory(contextSource);
	factory.setUserSearchBase("ou=people");
	factory.setUserSearchFilter("(uid={0})");
	return factory.createAuthenticationManager();
}
```

**Listing 1.** Current sample (**`LdapBindAuthenticationManagerFactory`** since **5.7**). `{0}` is the login name. Search is under `ou=people,<root DN>` from the `ContextSource` URL; omit the base to search from the root. If every user sits under one node, **`setUserDnPatterns("uid={0},ou=people")`** instead of a search. Wire this manager with **`http.authenticationManager(...)`** if the filter chain must not keep the default DAO provider ([[How do you configure a custom AuthenticationProvider in Spring Security]]).

Embedded demos: **`EmbeddedLdapServerContextSourceFactoryBean.fromEmbeddedLdapServer()`** or **`UnboundIdContainer`**. **Spring Security 7 removed Apache DS** — use UnboundID.

```d2
direction: down
login: "formLogin / httpBasic" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
ldap: "LdapAuthenticationProvider\nBindAuthenticator" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
dir: "LDAP bind as user DN" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
roles: "DefaultLdapAuthoritiesPopulator\ngroup search → GrantedAuthority" {
  width: 300
  height: 70
  style.fill: "#f3e5f5"
}

login -> ldap -> dir
ldap -> roles
```

**Fig. 1.** Bind authenticates; a **separate** search maps `groupOfNames` / `member` to authorities. Password-compare (`LdapPasswordComparisonAuthenticationManagerFactory`) is the other authenticator — it cannot LDAP-compare a **salted hash**.

## Groups → authorities

**`DefaultLdapAuthoritiesPopulator`**: search relative to **`groupSearchBase`** (`null` disables group search). Filter **`member={0}`** substitutes the user’s **full DN** (`{1}` = username). Default role attribute **`cn`**, prefix **`ROLE_`**, names uppercased. Example: member of `cn=developers` → **`ROLE_DEVELOPERS`**.

```java
@Bean
LdapAuthoritiesPopulator authorities(BaseLdapPathContextSource contextSource) {
	DefaultLdapAuthoritiesPopulator populator =
		new DefaultLdapAuthoritiesPopulator(contextSource, "ou=groups");
	populator.setGroupSearchFilter("member={0}");
	return populator;
}
```

**Listing 2.** Pass the populator to the factory with **`setLdapAuthoritiesPopulator`**. XML: `group-search-filter="member={0}"` on `<ldap-authentication-provider>` ([[What is GrantedAuthority in Spring Security]]).

## `ldapAuthentication()` DSL and Active Directory

**`AuthenticationManagerBuilder.ldapAuthentication()`** still exists (`LdapAuthenticationProviderConfigurer`, since **3.2**). The dump recipe is valid:

```java
auth.ldapAuthentication()
	.contextSource().url("ldap://localhost:8389/dc=springframework,dc=org")
	.and()
	.userSearchBase("ou=people")
	.userSearchFilter("(uid={0})")
	.groupSearchBase("ou=groups")
	.groupSearchFilter("member={0}");
```

**Listing 3.** Builder DSL. **`.url(...)`** is for a **remote** server, not the embedded instance. Prefer Listing 1 in Security 6/7. JDBC/in-memory remain **`UserDetailsService`** stores; LDAP is not ([[How do you configure JDBC authentication in Spring Security]]).

Active Directory’s usual **`user@domain`** pattern does not fit **`LdapAuthenticationProvider`** cleanly. Use **`ActiveDirectoryLdapAuthenticationProvider("example.com", "ldap://company.example.com/")`** (since **3.1**). Authorities come from **`memberOf`**. Optional **`setConvertSubErrorCodesToExceptions(true)`** maps AD subcodes (expired, locked, …) instead of a generic **`BadCredentialsException`**.

> [!warning] Empty passwords must not bind
> **`LdapAuthenticationProvider`** rejects an **empty** password. Some directories allow an **anonymous bind** with a DN and blank password, which would otherwise authenticate **as that user**.

> [!warning] Bind never reads `userPassword`
> Do not expect **`PasswordEncoder`** / `{bcrypt}` on the LDAP entry for bind. Comparison mode is a different factory and still cannot compare a **random-salt** hash via LDAP compare. For AD, logins are **`user@domain`**, not `uid={0},ou=people`.

> [!tip] Interview answer
> I add spring-security-ldap, configure a ContextSource, and publish an AuthenticationManager from LdapBindAuthenticationManagerFactory with a user DN pattern or uid search filter. Groups are mapped by DefaultLdapAuthoritiesPopulator, not UserDetailsService — bind authentication never returns the password. For Active Directory I use ActiveDirectoryLdapAuthenticationProvider with the domain and LDAP URL. The old auth.ldapAuthentication() DSL still works; Security 7 samples use the factory bean.
