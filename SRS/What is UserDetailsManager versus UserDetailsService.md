<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is UserDetailsManager versus UserDetailsService?

> [!abstract] Short answer
> **`UserDetailsService`** is **read-only**: **`loadUserByUsername(String)`** returns a **`UserDetails`** (never **`null`**) or throws **`UsernameNotFoundException`**. That is all **`DaoAuthenticationProvider`** needs for login. **`UserDetailsManager` extends `UserDetailsService`** with **admin CRUD**: **`createUser`**, **`updateUser`**, **`deleteUser`**, **`changePassword`**, **`userExists`**. **`InMemoryUserDetailsManager`** and **`JdbcUserDetailsManager`** are managers. A production bean against your own schema is **usually just `UserDetailsService`** — extra manager methods are **not** required to authenticate.

## Load for login versus mutate users

Javadoc for **`UserDetailsService`**: *Core interface which loads user-specific data* — the **user DAO** strategy for **`DaoAuthenticationProvider`**. One method. Missing user or no authorities → **`UsernameNotFoundException`** ([[What is UserDetails and UserDetailsService in Spring Security]], [[What is DaoAuthenticationProvider]], [[What is UsernameNotFoundException]]).

**`UserDetailsManager`** (**`org.springframework.security.provisioning`**) adds:

| Method | Purpose |
| --- | --- |
| **`createUser(UserDetails)`** | Insert |
| **`updateUser(UserDetails)`** | Replace (not the current password-upgrade path) |
| **`deleteUser(String)`** | Remove |
| **`changePassword(old, new)`** | Current authenticated user; may re-check **`old`** |
| **`userExists(String)`** | Probe without loading the full snapshot |

**`UserDetailsPasswordService.updatePassword`** is a **separate** interface used when a **`PasswordEncoder`** **upgrades** a hash during login. JDBC’s **`updatePassword`** is a **no-op** unless **`enableUpdatePassword`** (**since 7.0**, default **false**). In-memory implements both manager and password-service ([[What is JdbcUserDetailsManager]], [[What is InMemoryUserDetailsManager]]).

**`JdbcDaoImpl`** is JDBC **`UserDetailsService` only**. **`JdbcUserDetailsManager` extends it** to add the manager (+ optional **groups**). **`LdapUserDetailsManager`** is the directory manager. Reactive apps use **`ReactiveUserDetailsService`**, not this pair.

A **`UserDetailsService` `@Bean`** (manager or not) **replaces Boot’s generated user**. Login never calls **`createUser`**. Implement manager methods only when **this process** is the user admin API ([[How do you create a custom UserDetailsService in Spring Security]], [[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]]).

```java
public interface UserDetailsService {
	UserDetails loadUserByUsername(String username) throws UsernameNotFoundException;
}
```

**Listing 1.** Login contract (**7.1.1**). **Never return `null`.**

```java
@Bean
UserDetailsManager users() {
	UserDetails user = User.builder()
		.username("user")
		.password("{bcrypt}$2a$10$GRLdNijSQMUvl/au9ofL.eDwmoohzzS7.rmNSJZ.0FxO/BTk76klW")
		.roles("USER")
		.build();
	return new InMemoryUserDetailsManager(user);
}
```

**Listing 2.** A **manager** you can also **`createUser`** in tests. A JPA app would **`@Bean UserDetailsService`** without implementing CRUD here.

```d2
direction: down
mgr: "UserDetailsManager\nCRUD + changePassword + userExists" {
  width: 320
  height: 70
  style.fill: "#fff3e0"
}
uds: "UserDetailsService\nloadUserByUsername" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
dao: "DaoAuthenticationProvider" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

mgr -> uds -> dao
```

**Fig. 1.** Manager **is-a** service. The provider **only** calls the load method.

> [!warning] Do not implement a manager “for login”
> **`DaoAuthenticationProvider`** never calls **`createUser`**. A custom **`UserDetailsManager`** that no-ops CRUD still works for authentication — you paid for an interface you do not use. Put registration in **your** application service; implement **`UserDetailsService`** (or adapt an existing user port).

> [!warning] `changePassword` is not `updateUser`
> **`changePassword`** updates the **current `SecurityContext`** principal’s secret (and may verify **`oldPassword`**). **`updateUser`** rewrites a **named** account. Password-upgrade during **`matches`** goes through **`UserDetailsPasswordService`**, which JDBC **disables by default** in **7.0**.

> [!tip] Interview answer
> UserDetailsService is loadUserByUsername — that is the only method DaoAuthenticationProvider needs. UserDetailsManager extends it with create, update, delete, changePassword, and userExists. InMemoryUserDetailsManager and JdbcUserDetailsManager are managers for tests or the default JDBC schema. For a JPA user table I implement UserDetailsService only and keep registration in my own service.
