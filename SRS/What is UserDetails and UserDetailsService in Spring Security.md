<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is UserDetails and UserDetailsService in Spring Security?

> [!abstract] Short answer
> **`UserDetails`** is the **user snapshot** username/password authentication runs against: username, **password hash**, **`GrantedAuthority` collection**, and four account flags. **`UserDetailsService`** is the **read** strategy: **`loadUserByUsername(String)`** must return a **fully populated** **`UserDetails` (never `null`)** or throw **`UsernameNotFoundException`**. Javadoc: it is the **user DAO** **`DaoAuthenticationProvider`** uses. Stock stores: **`InMemoryUserDetailsManager`**, **`JdbcUserDetailsManager`**. Production usually implements the interface against your own tables. On success that **`UserDetails`** is typically **`Authentication.getPrincipal()`**.

## Snapshot versus the loader

**`UserDetails`** is data, not a filter. Stock type **`User`**. Getters: **`getUsername`**, **`getPassword`**, **`getAuthorities`** (never null), plus **`isEnabled` / `isAccountNonLocked` / `isAccountNonExpired` / `isCredentialsNonExpired`** (interface **defaults all `true`**). **`User.roles("USER")`** stores **`ROLE_USER`**; **`authorities("USER")`** stores **`USER`** ([[What account status flags does UserDetails expose]], [[What is GrantedAuthority in Spring Security]], [[What is the difference between Principal and UserDetails]]).

**`UserDetailsService`** javadoc: *Core interface which loads user-specific data.* One method. Lookup may be case-sensitive or not; the returned username **may differ in case** from the request. Missing user **or a user with no `GrantedAuthority`** → **`UsernameNotFoundException`**. **`fromUsername(username)`** since **7.0**. **`null` is not “not found”** — **`DaoAuthenticationProvider`** treats it as **`InternalAuthenticationServiceException`**. By default **`hideUserNotFoundExceptions`** turns a thrown not-found into **`BadCredentialsException`** ([[What is UsernameNotFoundException]], [[What is DaoAuthenticationProvider]]).

The provider then **`PasswordEncoder.matches`**. **`UserDetailsManager`** **extends** this interface with **CRUD / `changePassword`** — login only needs the load method ([[What is UserDetailsManager versus UserDetailsService]], [[How do you create a custom UserDetailsService in Spring Security]]).

| Implementation | Role |
| --- | --- |
| **`InMemoryUserDetailsManager`** (**since 3.1**) | Map for tests/demos |
| **`JdbcUserDetailsManager`** (**since 2.0**) | JDBC **`users` / `authorities`** |
| Custom **`UserDetailsService`** | Your JPA/repo model |
| LDAP **bind** | **Not** this interface for the password — the directory binds |

A **`UserDetailsService` `@Bean`** replaces Boot’s generated **`user`**. **`User` implements `CredentialsContainer`**: after login **`eraseCredentials()`** can clear the hash — return a **new** instance each load if you would otherwise cache one ([[What is InMemoryUserDetailsManager]], [[What is JdbcUserDetailsManager]], [[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]]).

```java
UserDetails user = User.builder()
	.username("user")
	.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
	.roles("USER")
	.build();
```

**Listing 1.** Snapshot with a **pre-hashed** password and **`ROLE_USER`**.

```java
@Bean
UserDetailsService users() {
	return username -> {
		if ("user".equals(username)) {
			return user;
		}
		throw UsernameNotFoundException.fromUsername(username);
	};
}
```

**Listing 2.** Minimal service. Prefer a class that **loads from your store** over a lambda that captures one **`User`** instance.

```d2
direction: down
uds: "UserDetailsService\nloadUserByUsername" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
ud: "UserDetails\nusername hash authorities flags" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
dao: "DaoAuthenticationProvider\nmatches + status checks" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
prin: "Authentication.getPrincipal()" {
  width: 260
  height: 50
  style.fill: "#f3e5f5"
}

uds -> ud -> dao -> prin
```

**Fig. 1.** The service **loads**. The provider **checks**. The token **holds** the snapshot.

> [!warning] Never return `null`
> **`loadUserByUsername`** javadoc: **never `null`**. Throw **`UsernameNotFoundException`**. Empty **`getAuthorities()`** is also not-found per that javadoc. Authorities must match **`hasRole` / `hasAuthority`** spelling (**`ROLE_`**).

> [!warning] `UserDetails` is not always the servlet Principal
> **`Authentication` implements `java.security.Principal`**. JWT / anonymous principals are **not** **`UserDetails`**. Caching the same **`User`** across logins plus **`eraseCredentials`** wipes the stored hash.

> [!tip] Interview answer
> UserDetails is the user record DaoAuthenticationProvider authenticates: username, encoded password, authorities, and four status flags. UserDetailsService.loadUserByUsername loads that record or throws UsernameNotFoundException — never null. In-memory and JDBC managers implement it; production usually maps your own user table. On success that UserDetails is typically the Authentication principal, not the servlet Principal itself.
