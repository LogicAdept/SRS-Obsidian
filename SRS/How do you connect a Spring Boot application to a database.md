<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Data #Java/JDBC #SRS

# How do you connect a Spring Boot application to a database?

> [!abstract] Short answer
> Add a data starter (`spring-boot-starter-data-jpa` or `spring-boot-starter-jdbc`), set **`spring.datasource.url`** (and credentials) in config, and let Boot auto-configure a **`DataSource`**. Access data through **`JdbcTemplate`** / **`JdbcClient`** or a **`JpaRepository`** — no manual connection wiring in application code.

## Dependencies and configuration

Spring Boot connects when the JDBC stack is on the classpath and datasource properties are present. For a real database, you must set at least the URL; otherwise Boot may fall back to an **embedded H2/HSQL/Derby** if those drivers are present.

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/myapp
spring.datasource.username=app
spring.datasource.password=secret

spring.jpa.hibernate.ddl-auto=validate
```

**Listing 1.** Production-style JDBC URL + credentials; JPA DDL only where appropriate (Spring Boot SQL databases reference).

```java
@SpringBootApplication
class Application {}

@RestController
class UserController {

  private final UserRepository users;

  UserController(UserRepository users) {
    this.users = users;
  }

  @GetMapping("/users/{id}")
  User find(@PathVariable Long id) {
    return users.findById(id).orElseThrow();
  }
}

interface UserRepository extends JpaRepository<User, Long> {}
```

**Listing 2.** After auto-config: declare a repository (or inject `JdbcTemplate`) — Boot creates the proxy and pool.

```d2
direction: right
starter: "spring-boot-starter-\ndata-jpa / jdbc" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
props: "spring.datasource.*" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
auto: "DataSource +\nJdbcTemplate / EMF" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
app: "Repository or\nJdbcTemplate" {
  width: 200
  height: 70
  style.fill: "#f3e5f5"
}

starter -> auto
props -> auto
auto -> app
```

**Fig. 1.** Starters + properties trigger auto-configuration; your code uses the abstractions, not raw `DriverManager`.

With **`spring-boot-starter-data-jpa`**, Boot also configures JPA/Hibernate and scans for repository interfaces under the main application package. **`@EnableJpaRepositories`** is only needed for non-default base packages. A custom `@Bean DataSource` replaces auto-configured datasource setup.

> [!warning] `create-drop` and raw SQL in controllers
> `spring.jpa.hibernate.ddl-auto=create-drop` is for dev/tests, not production schema management. Injecting `JdbcTemplate` only to run string-concatenated SQL in a controller bypasses repositories, transactions, and parameter binding — prefer repositories or parameterized JDBC.

See [[How do you configure multiple data sources in Spring Boot]], [[What is Spring Data JPA]], and [[What is a CrudRepository]].

> [!tip] Interview answer
> I add `spring-boot-starter-data-jpa` or `spring-boot-starter-jdbc`, set `spring.datasource.url` and credentials, and Boot auto-configures the pool. Then I use `JpaRepository` or `JdbcTemplate`. Defining my own `DataSource` bean opts out of that auto-config. Without a URL, Boot may wire an embedded database instead.
