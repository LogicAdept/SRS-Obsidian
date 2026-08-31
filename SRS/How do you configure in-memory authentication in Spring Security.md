<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure in-memory authentication in Spring Security?

> [!abstract] Short answer
> Expose an **`InMemoryUserDetailsManager`** as the **`UserDetailsService`** bean, built from **`User.builder()`** users whose passwords are **already encoded** (typically `{bcrypt}…`). That manager is a **non-persistent map** for tests and demos. **`DaoAuthenticationProvider`** then matches the login password. Prefer this bean over **`AuthenticationManagerBuilder.inMemoryAuthentication()`**. **`{noop}`** and **`User.withDefaultPasswordEncoder()`** are getting-started only.

## A map-backed `UserDetailsService`

Javadoc: *Non-persistent implementation of `UserDetailsManager` which is backed by an in-memory map. Mainly intended for testing and demonstration purposes.* Users vanish on restart and are not shared across instances. **`loadUserByUsername`** is what **`DaoAuthenticationProvider`** calls ([[What is InMemoryUserDetailsManager]], [[What is UserDetails and UserDetailsService in Spring Security]], [[What is DaoAuthenticationProvider]]).

The servlet reference sample hashes `password` ahead of time (Spring Boot CLI / `PasswordEncoderFactories.createDelegatingPasswordEncoder()`) and stores the **delegating** id prefix:

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

**Listing 1.** Current Java configuration. **`roles("USER")`** is stored as **`ROLE_USER`**. XML: `<user-service>` with the same `{bcrypt}…` passwords. Production persistence is **`JdbcUserDetailsManager`** or a custom **`UserDetailsService`**, not this map ([[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]]).

```d2
direction: down
login: "formLogin / httpBasic" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
dao: "DaoAuthenticationProvider" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
mem: "InMemoryUserDetailsManager\nMap of UserDetails" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

login -> dao -> mem
```

**Fig. 1.** In-memory auth is still username/password through the provider. Only the **store** is a JVM map. WebFlux’s counterpart is **`MapReactiveUserDetailsService`**, not this class ([[What is MapReactiveUserDetailsService]]).

## `AuthenticationManagerBuilder` DSL (still valid, not the 7.x sample)

**`inMemoryAuthentication()`** returns **`InMemoryUserDetailsManagerConfigurer`**. **`withUser(String)`** (since **3.2**) can be called repeatedly; **`.and()`** returns the configurer to add another user. Password and authorities are required on each builder:

```java
@Autowired
void configure(AuthenticationManagerBuilder auth) throws Exception {
	auth.inMemoryAuthentication()
		.withUser("user").password("{noop}password").roles("USER")
		.and()
		.withUser("admin").password("{noop}password").roles("USER", "ADMIN");
}
```

**Listing 2.** Global-builder style from dumps. `{noop}` tells **`DelegatingPasswordEncoder`** to use **no** encoding — demos only. This **configures** the builder (`isConfigured() == true`), which **suppresses** auto-pickup of a separate `UserDetailsService` / `AuthenticationProvider` bean.

In Boot, a **`UserDetailsService`**, **`AuthenticationProvider`**, or **`AuthenticationManager`** bean **stops** **`UserDetailsServiceAutoConfiguration`** from creating the generated **`user`** / random password. A **`SecurityFilterChain`** bean alone does **not**. After you add Listing 1, the log line `Using generated security password:` is gone — that password no longer works ([[What is the default username and password in Spring Boot Security]]).

> [!warning] `{noop}` and `User.withDefaultPasswordEncoder()` are not production
> XML samples prefix `{noop}` so **no** encoder runs. **`withDefaultPasswordEncoder()`** hashes at JVM start but the **plain password stays in bytecode**; it is **`@Deprecated`** and **not safe for production**. Hash **outside** the source and paste `{bcrypt}…`. A raw `BCryptPasswordEncoder` bean is optional; the default matcher is already **`DelegatingPasswordEncoder`** (bcrypt id).

> [!warning] This is not a user database
> The map is process-local. `createUser` / `updateUser` / `changePassword` exist (`UserDetailsManager`) but die with the JVM. Do not put real accounts here.

> [!tip] Interview answer
> I register an InMemoryUserDetailsManager as the UserDetailsService with User.builder() and pre-hashed `{bcrypt}` passwords. It is a map for tests and samples, not production storage. In Boot that bean replaces the generated user/password. I do not ship `{noop}` or withDefaultPasswordEncoder. The older auth.inMemoryAuthentication().withUser() DSL still works on AuthenticationManagerBuilder but is not the current reference sample.
