<!--
reps: 0
priority: 0
-->
#Java/Testing/Testcontainers #SRS

# How would you explain Testcontainers

> [!abstract] Short answer
> **Testcontainers throws away the fake-database compromise: your tests boot real PostgreSQL, Kafka, Redis — whatever the dependency is — in Docker containers, started and torn down by the test itself.** The test connects to a real server on a random mapped port, so SQL dialects, drivers and protocol behavior are the production ones, not a Java reimplementation.

## What the library actually does

A container object (`PostgreSQLContainer`, `KafkaContainer`, `GenericContainer`) describes an image plus ports and waits-for-ready rules. The JUnit 5 extension (`@Testcontainers` on the class, `@Container` on the field) starts the container before tests and stops it after, so every run gets a fresh, clean service.

```d2
direction: right
dep: "JUnit 5 extension\n@Testcontainers / @Container" {
  width: 290
  height: 90
  style.fill: "#e3f2fd"
}
docker: "Docker daemon\npulls the image once" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
c: "PostgreSQLContainer\npostgres:16-alpine" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
m: "Random mapped port\ngetJdbcUrl() / getHost()\ngetMappedPort(...)" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
t: "Test asserts against\nthe real server" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
dep -> c
dep -> docker
c -> m
m -> t
```

**Fig. 1.** The extension drives the Docker lifecycle; the test asks the container object for real connection coordinates.

```java
@Testcontainers
class ContainerQuickstartTest {

    @Container
    private static final PostgreSQLContainer<?> POSTGRES =
            new PostgreSQLContainer<>("postgres:16-alpine");

    @Test
    void realDatabaseIsReachable() throws Exception {
        try (var cn = DriverManager.getConnection(
                POSTGRES.getJdbcUrl(), POSTGRES.getUsername(), POSTGRES.getPassword());
             ResultSet rs = cn.createStatement()
                     .executeQuery("select version()")) {
            rs.next();
            String version = rs.getString(1);
            System.out.println(version.split(",")[0]);
            assertTrue(version.contains("PostgreSQL"));
        }
    }
}
```

**Listing 1.** The canonical shape from the Testcontainers JUnit 5 quickstart. This listing is **conceptual here**: it compiles on JDK 21 (checked against Testcontainers 1.19.7), but this sandbox has no Docker daemon, so no run output is quoted — the printed line would be the server's `select version()` answer.

## Why not H2

The usual cheap trick is swapping the production database for an in-memory one in tests. H2 speaks a dialect close to, but not equal to, PostgreSQL: JSON operators, locking behavior, transaction isolation quirks, and vendor functions differ, so green H2 tests can hide red production SQL — especially migrations. With Testcontainers the migration runner (Flyway/Liquibase) executes against the real engine, the real driver is on the classpath, and serialization or constraint bugs surface in CI, not on Friday night. The price is Docker: the daemon must exist wherever tests run, and image pulls make the first run slow. Connection details come from the container, never hardcoded — the quickstart's own tip is to use `getHost()` because `localhost` breaks in CI.

> [!warning] Static @Container shares one container across all tests
> A `static` `@Container` field starts once per class and keeps one database for every test method — leftover rows from one test leak into the next unless you clean up or re-seed. A non-static field starts a fresh container per test: isolated, but slow. Real projects pick one deliberately: per-class containers plus transactional rollbacks or cleanup scripts, and reusable-container setups to cut startup time. And no Docker daemon means every Testcontainers test fails fast with "Could not find a valid Docker environment" — the common first-run surprise in locked-down CI. For the config the container might need in a Spring context, see [[What is DynamicPropertySource]]; for keeping the test data tidy, [[What is a test fixture in JUnit]].

> [!tip] Interview answer
> **Testcontainers runs test dependencies as real Docker containers managed by JUnit: annotate a container field, and the extension starts it before and removes it after the tests. The test connects through getJdbcUrl or getHost and getMappedPort — a real PostgreSQL, not an H2 imitation — so dialects, migrations and protocol behavior are production-true. Cost: you need Docker available, and startup time is managed with per-class or reusable containers.**

