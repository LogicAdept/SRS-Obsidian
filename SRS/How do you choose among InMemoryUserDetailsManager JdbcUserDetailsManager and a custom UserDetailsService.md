<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you choose among InMemoryUserDetailsManager, JdbcUserDetailsManager, and a custom UserDetailsService?

> [!abstract] Short answer
> Choose by **where users live** and **how much of `UserDetails` you need**. **`InMemoryUserDetailsManager`** is a non-persistent map for tests and demos. **`JdbcUserDetailsManager`** is the JDBC `UserDetailsManager` when you can use (or query-map onto) the default **`users` / `authorities`** tables. A **custom `UserDetailsService`** is `loadUserByUsername` against your own repository or model — including flags JDBC does not load. **`DaoAuthenticationProvider`** then matches the stored password with a **`PasswordEncoder`**.

## One interface, three stores

`UserDetailsService` is the read-only user DAO used by **`DaoAuthenticationProvider`**: one method, **`loadUserByUsername(String)`**, which must return a fully populated `UserDetails` and **never `null`**. Missing users throw **`UsernameNotFoundException`** ([[What is UsernameNotFoundException]], [[What is DaoAuthenticationProvider]]).

**`UserDetailsManager`** extends that interface with **`createUser` / `updateUser` / `deleteUser` / `changePassword` / `userExists`**. Both built-in managers implement it (and **`UserDetailsPasswordService.updatePassword`**). A production bean is often **only** `UserDetailsService` — login does not need the CRUD methods ([[What is UserDetailsManager versus UserDetailsService]], [[What is UserDetails and UserDetailsService in Spring Security]]).

| Store | Persistence | Typical when |
| --- | --- | --- |
| **`InMemoryUserDetailsManager`** | In-process `Map` | Tests, samples, a handful of hardcoded users |
| **`JdbcUserDetailsManager`** | JDBC `DataSource` | Default `users`/`authorities` (optional groups), or the same columns via custom SQL |
| **Custom `UserDetailsService`** | Whatever you call | JPA/existing user service, extra fields, lock/expiry flags JDBC ignores |

```d2
direction: down
dao: "DaoAuthenticationProvider\nloadUserByUsername + PasswordEncoder" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
choice: "Which UserDetailsService?" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
mem: "InMemoryUserDetailsManager\nmap, not durable" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
jdbc: "JdbcUserDetailsManager\nusers + authorities" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
custom: "Your UserDetailsService\nJPA / existing API" {
  width: 280
  height: 70
  style.fill: "#f3e5f5"
}

dao -> choice
choice -> mem
choice -> jdbc
choice -> custom
```

**Fig. 1.** Username/password login always goes through a `UserDetailsService`. The three choices differ in storage, not in the provider.

## In-memory: tests and getting started

Javadoc: *Non-persistent implementation of `UserDetailsManager` which is backed by an in-memory map. Mainly intended for testing and demonstration purposes.* Since **3.1**. Users vanish on restart; there is no shared store across instances.

```java
@Bean
UserDetailsService users() {
	UserDetails user = User.builder()
		.username("user")
		.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
		.roles("USER")
		.build();
	UserDetails admin = User.builder()
		.username("admin")
		.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
		.roles("USER", "ADMIN")
		.build();
	return new InMemoryUserDetailsManager(user, admin);
}
```

**Listing 1.** Reference in-memory bean. The `{bcrypt}…` value is a **pre-hashed** password (`password` in the Security docs), not a secret to copy into production configs ([[What is InMemoryUserDetailsManager]]).

WebFlux’s counterpart is **`MapReactiveUserDetailsService`**, not this class ([[What is MapReactiveUserDetailsService]]).

## JDBC: default schema, or queries remapped to it

**`JdbcDaoImpl`** implements `UserDetailsService` with JDBC. **`JdbcUserDetailsManager`** extends it and adds `UserDetailsManager` plus **`GroupManager`**. Default tables: **`users`** (`username`, `password`, `enabled`) and **`authorities`** (`username`, `authority`). DDL also lives at `JdbcDaoImpl.DEFAULT_USER_SCHEMA_DDL_LOCATION` (`org/springframework/security/core/userdetails/jdbc/users.ddl`). Optional **groups** / **group_members** / **group_authorities** when `enableGroups` is true.

```java
@Bean
DataSource dataSource() {
	return new EmbeddedDatabaseBuilder()
		.setType(EmbeddedDatabaseType.H2)
		.addScript(JdbcDaoImpl.DEFAULT_USER_SCHEMA_DDL_LOCATION)
		.build();
}

@Bean
UserDetailsManager users(DataSource dataSource) {
	JdbcUserDetailsManager users = new JdbcUserDetailsManager(dataSource);
	users.createUser(User.builder()
		.username("user")
		.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
		.roles("USER")
		.build());
	return users;
}
```

**Listing 2.** Embedded H2 + default schema is a sample. Production must use an **external** `DataSource`. Oracle needs the dialect-specific DDL from the JDBC Authentication chapter ([[What is JdbcUserDetailsManager]]).

An **existing** schema that is still “username, password, enabled, authorities” does **not** force a custom `UserDetailsService`. Override **`setUsersByUsernameQuery`** and **`setAuthoritiesByUsernameQuery`** (column **order** must match the defaults). JDBC **does not** load account-expiry or credentials-expiry; it honours **`enabled`** only. Need lock/expiry columns or a JPA entity → custom service.

If **`enableAuthorities`** is `false`, `createUser` / `updateUser` / `deleteUser` **do not** write or delete authority rows. From **7.0**, **`updatePassword`** is a no-op unless **`setEnableUpdatePassword(true)`** — default `false` so hashed passwords are not written into a column that is too short.

## Custom `UserDetailsService`: your model

Expose a bean that implements **`loadUserByUsername`**. Spring uses it when **`AuthenticationManagerBuilder` has not been populated** and **no `AuthenticationProvider` bean** is defined.

```java
public class JpaUserDetailsService implements UserDetailsService {

	private final UserRepository users;

	public JpaUserDetailsService(UserRepository users) {
		this.users = users;
	}

	@Override
	public UserDetails loadUserByUsername(String username) {
		return users.findByUsername(username)
			.map(this::toUser)
			.orElseThrow(() -> new UsernameNotFoundException(username));
	}

	private UserDetails toUser(AppUser u) {
		return User.builder()
			.username(u.username())
			.password(u.passwordHash())
			.disabled(!u.enabled())
			.accountLocked(u.locked())
			.roles(u.roles().toArray(String[]::new))
			.build();
	}
}
```

**Listing 3.** Conceptual: `AppUser` / `UserRepository` are your types. Return a **new** `User` each call — `User` is **not** immutable; `eraseCredentials()` clears the password after authentication. Reusing one in-memory instance corrupts later logins.

`User.builder()` / the 7-arg `User` constructor are the stock `UserDetails`. You may implement **`UserDetails`** yourself when the principal must carry domain fields (tenant, email) that `User` does not have.

## Password encoding is not optional

All three stores hold **already encoded** passwords. **`DaoAuthenticationProvider.setPasswordEncoder`** defaults to **`PasswordEncoderFactories.createDelegatingPasswordEncoder()`**, which expects an id prefix (`{bcrypt}…`). Encode at registration time; do not store raw passwords.

> [!warning] `{noop}` and `User.withDefaultPasswordEncoder()` are demos
> XML samples prefix `{noop}` so **no encoding** runs. **`User.withDefaultPasswordEncoder()`** hashes at JVM start, but the **plain password stays in bytecode**; it is **`@Deprecated`** and **not safe for production**. Hash **ahead of time** (Boot CLI / `encoder.encode`) and paste `{bcrypt}…` into config or the database.

> [!warning] A custom `UserDetailsService` bean can be ignored
> The reference: the custom bean is used **only if** `AuthenticationManagerBuilder` is empty **and** there is **no** `AuthenticationProvider` bean. A leftover `DaoAuthenticationProvider` or `AuthenticationManagerBuilder` in-memory setup wins, and your JPA loader never runs.

> [!warning] `loadUserByUsername` must not return `null`
> The contract is a fully populated user or **`UsernameNotFoundException`**. Returning `null` (or a user with **no** `GrantedAuthority`) is invalid. JDBC with both `enableAuthorities` and `enableGroups` off can produce that empty-authority case.

> [!tip] Interview answer
> InMemoryUserDetailsManager is a map for tests and samples — not a durable user store. JdbcUserDetailsManager is Spring’s JDBC users and authorities tables, or the same shape with custom SQL. If I already have a user table or JPA model, or I need lock and expiry flags JDBC does not load, I implement UserDetailsService.loadUserByUsername and expose it as a bean. DaoAuthenticationProvider still needs a PasswordEncoder; `{noop}` and `withDefaultPasswordEncoder` are not production.
