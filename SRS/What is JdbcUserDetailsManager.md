<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# What is JdbcUserDetailsManager?

> [!abstract] Short answer
> **`JdbcUserDetailsManager`** (**since 2.0**) is the JDBC **`UserDetailsManager`**: it **extends `JdbcDaoImpl`** (the JDBC **`UserDetailsService`**) and adds **CRUD** plus optional **groups**. Default tables are **`users(username, password, enabled)`** and **`authorities(username, authority)`**. **`DaoAuthenticationProvider`** still **`PasswordEncoder.matches`** the stored hash. This is **`JdbcTemplate` SQL**, not Spring Data JPA. **`AuthenticationManagerBuilder.jdbcAuthentication().dataSource(...)`** builds this same type.

## Schema-backed UserDetailsService plus admin SQL

Login only needs **`loadUserByUsername`** from the parent DAO (default queries: username/password/enabled, then username/authority). Missing user → **`UsernameNotFoundException`**. The manager adds **`createUser` / `updateUser` / `deleteUser` / `changePassword` / `userExists`**, implements **`GroupManager`**, and **`UserDetailsPasswordService`** ([[What is UserDetailsManager versus UserDetailsService]], [[What is UserDetails and UserDetailsService in Spring Security]], [[What is DaoAuthenticationProvider]], [[What is UsernameNotFoundException]]).

Stock DDL lives at **`JdbcDaoImpl.DEFAULT_USER_SCHEMA_DDL_LOCATION`** (`users.ddl`). Remap **`usersByUsernameQuery` / `authoritiesByUsernameQuery`** when column **order** matches. Optional **`groups` / `group_members` / `group_authorities`** with **`enableGroups`**. If **`enableAuthorities` is false**, **`createUser` / `updateUser` / `deleteUser` do not** write the **`authorities`** table — and this class **cannot tell** a user’s own authorities from **group** ones when it rewrites them.

**`updatePassword`** (**`UserDetailsPasswordService`**, used when the encoder **upgrades** a hash) is a no-op unless **`setEnableUpdatePassword(true)`** (**since 7.0**, default **false**) so a too-long hash cannot silently blow the column. **`changePassword`** updates the **current `SecurityContext` user** (optional re-auth via **`AuthenticationManager`**).

Not **`InMemoryUserDetailsManager`**, not LDAP **`LdapUserDetailsManager`**, not a JPA repository. An entity model belongs in a **custom `UserDetailsService`** ([[What is InMemoryUserDetailsManager]], [[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]], [[How do you configure JDBC authentication in Spring Security]], [[How do you create a custom UserDetailsService in Spring Security]]).

```java
@Bean
UserDetailsManager users(DataSource dataSource) {
	JdbcUserDetailsManager jdbc = new JdbcUserDetailsManager(dataSource);
	jdbc.setEnableUpdatePassword(true);
	return jdbc;
}
```

**Listing 1.** Production-shaped bean. Load schema with migrations (or **`withDefaultSchema()`** only on **embedded** DBs). Store **`{bcrypt}…`**, not **`{noop}`**.

```sql
insert into users (username, password, enabled) values (?,?,?);
insert into authorities (username, authority) values (?,?);
```

**Listing 2.** Default **`DEF_CREATE_USER_SQL` / `DEF_INSERT_AUTHORITY_SQL`**. Extra JDBC parameters can carry lock/expiry flags (**mapper since 6.5**); the **stock `users.ddl` does not**.

```d2
direction: down
ds: "DataSource\nusers + authorities" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
jdbc: "JdbcUserDetailsManager\nJdbcDaoImpl.loadUserByUsername" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
dao: "DaoAuthenticationProvider\nPasswordEncoder.matches" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

ds -> jdbc -> dao
```

**Fig. 1.** JDBC is the **store**. The **provider** still checks the password.

> [!warning] Not JPA and not “just a DataSource”
> Pointing **`jdbcAuthentication().dataSource`** at a JPA schema does not map entities. Wrong column order on a custom query **silently mis-binds** password/enabled. Group-enabled apps that also **`updateUser`** can **wipe or duplicate** authorities because group and user rows are not distinguished.

> [!warning] `enableUpdatePassword` defaults to false
> **7.0** refuses encoder **upgrade** writes until you opt in — otherwise **`updatePassword` returns the same `UserDetails`**. **`enabled`** is what JDBC loads by default; lock/expiry flags need **wider SQL**. **`createUser` stores `user.getPassword()` as-is** — encode **before** insert.

> [!tip] Interview answer
> JdbcUserDetailsManager is Spring Security’s JDBC UserDetailsManager: JdbcDaoImpl for loadUserByUsername plus SQL CRUD on the default users and authorities tables. DaoAuthenticationProvider still matches the PasswordEncoder hash. I remap the two select queries if the schema is close, enable updatePassword in 7.x if I want hash upgrades, and I write a custom UserDetailsService when the model is JPA. It is not Spring Data and it is not LDAP.
