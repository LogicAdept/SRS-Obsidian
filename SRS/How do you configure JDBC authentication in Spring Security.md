<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #SRS

# How do you configure JDBC authentication in Spring Security?

> [!abstract] Short answer
> Give Spring a **`DataSource`** and a **`JdbcUserDetailsManager`** (the JDBC **`UserDetailsManager`**). Default tables are **`users(username, password, enabled)`** and **`authorities(username, authority)`**. Store passwords **already encoded** (`{bcrypt}…`). An existing schema with the same column **order** can remap **`usersByUsernameQuery` / `authoritiesByUsernameQuery`**. This is **JDBC**, not JPA — a custom **`UserDetailsService`** is the usual replacement for an entity model.

## Default schema, then a manager bean

**`JdbcDaoImpl`** is the JDBC **`UserDetailsService`**. **`JdbcUserDetailsManager`** extends it and adds CRUD (`UserDetailsManager`) plus optional **groups**. **`DaoAuthenticationProvider`** still does the password match ([[What is JdbcUserDetailsManager]], [[What is DaoAuthenticationProvider]], [[What is UserDetails and UserDetailsService in Spring Security]]).

Default DDL (also `JdbcDaoImpl.DEFAULT_USER_SCHEMA_DDL_LOCATION` = `org/springframework/security/core/userdetails/jdbc/users.ddl`):

```sql
create table users(
	username varchar_ignorecase(50) not null primary key,
	password varchar_ignorecase(500) not null,
	enabled boolean not null
);
create table authorities (
	username varchar_ignorecase(50) not null,
	authority varchar_ignorecase(50) not null,
	constraint fk_authorities_users foreign key(username) references users(username)
);
create unique index ix_auth_username on authorities (username,authority);
```

**Listing 1.** Reference default schema. Adjust types for the dialect (**Oracle** needs its own script in the JDBC Authentication chapter). Optional **`groups` / `group_members` / `group_authorities`** when **`enableGroups`** is true. JDBC honours **`enabled`** only — not account/credentials expiry.

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

**Listing 2.** Current servlet sample. Embedded H2 is for getting started; production must use an **external** `DataSource`. Prefer **Flyway/Liquibase** to create tables and insert users **once**, not `createUser` on every startup. XML: `<jdbc-user-service>`.

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
jdbc: "JdbcUserDetailsManager\nJdbcDaoImpl SQL" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
db: "users + authorities" {
  width: 240
  height: 50
  style.fill: "#f3e5f5"
}

login -> dao -> jdbc -> db
```

**Fig. 1.** Same provider as in-memory auth; only the store is JDBC ([[How do you configure in-memory authentication in Spring Security]], [[How do you choose among InMemoryUserDetailsManager JdbcUserDetailsManager and a custom UserDetailsService]]).

## Custom SQL vs a JPA `UserDetailsService`

If table/column names differ, keep JDBC and override the queries. Returned **column positions** must match the defaults (`username, password, enabled` and `username, authority`). Missing **`enabled`**: `select username, password, 'true' as enabled from …`.

**`AuthenticationManagerBuilder.jdbcAuthentication()`** (since **3.2**) still works. **`dataSource`** is the only required attribute; **`withDefaultSchema()`** loads the default DDL (embedded DBs). Custom queries:

```java
@Autowired
void configure(AuthenticationManagerBuilder auth, DataSource dataSource) throws Exception {
	auth.jdbcAuthentication()
		.dataSource(dataSource)
		.usersByUsernameQuery("select username, password, enabled from users where username = ?")
		.authoritiesByUsernameQuery("select username, authority from authorities where username = ?");
}
```

**Listing 3.** DSL equivalent of `setUsersByUsernameQuery` / `setAuthoritiesByUsernameQuery`. Prefer the **`JdbcUserDetailsManager` bean** (Listing 2) in Security 6/7 samples.

Need lock/expiry flags, extra columns, or a JPA entity → implement **`UserDetailsService.loadUserByUsername`**. Query remapping is **not** Spring Data JPA.

> [!warning] Hashes in the `password` column, not raw strings
> **`DaoAuthenticationProvider`** matches with a **`PasswordEncoder`** (default **`DelegatingPasswordEncoder`**). A row of plain `password` fails against `{bcrypt}`. Store `{bcrypt}$2a$…` (or `{noop}…` only in demos). Encoding at login time does not rewrite existing rows.

> [!warning] `enableAuthorities` and `updatePassword` defaults
> If **`enableAuthorities`** is `false`, `createUser` / `updateUser` / `deleteUser` **do not** write authority rows. From **7.0**, **`updatePassword`** is a no-op unless **`setEnableUpdatePassword(true)`** (default `false` so a long hash is not stuffed into a short column).

> [!tip] Interview answer
> JDBC auth is JdbcUserDetailsManager on a DataSource, default users and authorities tables, passwords stored already encoded. I remap the two SQL queries if the schema is close; I write a UserDetailsService if the model is JPA or needs flags JDBC does not load. Embedded H2 plus withDefaultSchema is a sample — production uses a real database and migrations. This is not Spring Data JPA.
