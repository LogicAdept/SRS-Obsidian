<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is InMemoryUserDetailsManager?

> [!abstract] Short answer
> **`InMemoryUserDetailsManager`** (**since 3.1**) is a **non-persistent `UserDetailsManager`** backed by a **`HashMap`**. Javadoc: *mainly intended for testing and demonstration purposes.* It is also a **`UserDetailsPasswordService`**. **`DaoAuthenticationProvider`** calls **`loadUserByUsername`**. Users are **not** shared across processes and **vanish on restart**. A **`UserDetailsService` bean** (this class counts) **replaces Boot’s generated `user` / console password**. WebFlux’s counterpart is **`MapReactiveUserDetailsService`**, not this type.

## A JVM map, not a user database

Implements **`UserDetailsManager`** (CRUD + **`changePassword`**) on top of **`UserDetailsService`** ([[What is UserDetailsManager versus UserDetailsService]], [[What is UserDetails and UserDetailsService in Spring Security]], [[What is DaoAuthenticationProvider]]). Keys are **`username.toLowerCase(Locale.ROOT)`** — lookup is **case-insensitive**. **`createUser`** wraps a normal **`User`** in an internal **`MutableUser`** so **`updatePassword` / `changePassword`** can rewrite the hash. **`loadUserByUsername`** copies to a new **`User`** unless the stored value is already a **`CredentialsContainer`**, then throws **`UsernameNotFoundException.fromUsername`** (**7.0**) if missing ([[What is UsernameNotFoundException]]).

Reference configuration is a **`@Bean UserDetailsService`** that **`return new InMemoryUserDetailsManager(users…)`** with **pre-encoded** `{bcrypt}…` passwords — not **`AuthenticationManagerBuilder.inMemoryAuthentication()`** ([[How do you configure in-memory authentication in Spring Security]]). Production stores are **`JdbcUserDetailsManager`** or a custom **`UserDetailsService`** ([[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]], [[What is JdbcUserDetailsManager]], [[How do you create a custom UserDetailsService in Spring Security]]).

Boot’s default in-memory user is a **different** auto-config bean: username **`user`**, random password at **WARN**. Publishing **this** class (or any **`UserDetailsService` / `AuthenticationProvider` / `AuthenticationManager`**) turns that off ([[What is the default username and password in Spring Boot Security]]). Reactive apps use **`MapReactiveUserDetailsService`** ([[What is MapReactiveUserDetailsService]]).

```java
@Bean
UserDetailsService users() {
	UserDetails user = User.builder()
		.username("user")
		.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
		.roles("USER")
		.build();
	return new InMemoryUserDetailsManager(user);
}
```

**Listing 1.** Official servlet sample: one (or more) **`UserDetails`** in the constructor. **`roles("USER")`** stores **`ROLE_USER`**.

```java
UserDetails found = manager.loadUserByUsername("user");
manager.createUser(admin);
manager.updatePassword(found, newEncodedHash);
```

**Listing 2.** Login needs only **`loadUserByUsername`**. **`createUser` / `updateUser` / `deleteUser` / `changePassword`** are admin/demo CRUD. **`changePassword`** uses the **`SecurityContext`** current name; without an **`AuthenticationManager`** it **does not** re-check the old password.

```d2
direction: down
map: "HashMap\nlowercase username → MutableUser" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
load: "loadUserByUsername" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
dao: "DaoAuthenticationProvider" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

map -> load -> dao
```

**Fig. 1.** The map is the **store**. Password matching stays on the **provider**.

> [!warning] Tests and demos, not production
> Restart, another instance, or a second JVM has **empty** users. The map is a **`HashMap`**, not a shared database. **`{noop}`** and **`User.withDefaultPasswordEncoder()`** are getting-started only — store a **pre-hashed** `{bcrypt}…` value. **`User` / `user` collide** because keys are lowercased.

> [!warning] A UserDetailsService bean kills Boot’s generated password
> Dumps that still expect the **console** password after adding **`InMemoryUserDetailsManager`** fail by design. OAuth2 Client / resource-server / SAML on the classpath also back off Boot’s default user — then you **must** declare this bean (or another **`UserDetailsService`**) if you still want form/Basic users.

> [!tip] Interview answer
> InMemoryUserDetailsManager is Spring Security’s map-backed UserDetailsManager for tests and samples. DaoAuthenticationProvider loads users from it; they disappear on restart and are not clustered. I expose it as a UserDetailsService bean with already-encoded passwords, and I know that bean replaces Boot’s generated user. For real storage I use JDBC or a custom UserDetailsService, and on WebFlux I use MapReactiveUserDetailsService.
