<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Spring/Data #Java/Spring/Boot/Properties #SRS

# How do you configure multiple data sources in Spring Boot?

> [!abstract] Short answer
> Register one `DataSource` bean per database. Keep a single default for auto-config (`@Primary` or Boot’s auto-configured primary) and mark additional beans with `@Qualifier` and `defaultCandidate = false`. For JPA on both, add a separate `EntityManagerFactory`, `JpaTransactionManager`, and `@EnableJpaRepositories` per persistence unit.

## Multiple `DataSource` beans

Spring Boot auto-config expects exactly one injectable `DataSource` by type. Define extra pools as named beans bound to their own property prefix.

```java
@Configuration(proxyBeanMethods = false)
class DataSourcesConfiguration {

  @Bean
  @Primary
  @ConfigurationProperties("spring.datasource")
  DataSourceProperties primaryDataSourceProperties() {
    return new DataSourceProperties();
  }

  @Bean
  @Primary
  @ConfigurationProperties("spring.datasource.configuration")
  HikariDataSource primaryDataSource(DataSourceProperties props) {
    return props.initializeDataSourceBuilder()
        .type(HikariDataSource.class).build();
  }

  @Bean(defaultCandidate = false)
  @Qualifier("secondary")
  @ConfigurationProperties("app.datasource")
  HikariDataSource secondaryDataSource() {
    return DataSourceBuilder.create()
        .type(HikariDataSource.class).build();
  }
}
```

**Listing 1.** Primary pool stays the default; secondary uses its own prefix and `@Qualifier("secondary")` (Spring Boot “Configure Two DataSources”).

Inject the secondary pool only where qualified: `@Qualifier("secondary") DataSource secondary`. Without `@Primary` / a single default candidate, startup fails with ambiguous `DataSource` injection.

```d2
direction: down
props: "application.yml\nspring.datasource.*\napp.datasource.*" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
primary: "@Primary DataSource\nauto-config + JDBC/JPA default" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
secondary: "@Qualifier second\nDataSource (defaultCandidate=false)" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
jpa: "Optional second EMF +\nTransactionManager + repositories" {
  width: 300
  height: 80
  style.fill: "#f3e5f5"
}

props -> primary
props -> secondary
secondary -> jpa
```

**Fig. 1.** Property prefixes map to beans; JPA needs a full stack per extra database.

## JPA and Spring Data on both databases

A second `DataSource` alone does not give you two JPA units. Spring Boot’s how-to: **one `LocalContainerEntityManagerFactoryBean` (or `EntityManagerFactory`) per datasource**, each with its own `JpaTransactionManager`, and repository scanning split with `@EnableJpaRepositories`:

```java
@EnableJpaRepositories(
    basePackageClasses = Order.class,
    entityManagerFactoryRef = "entityManagerFactory",
    transactionManagerRef = "transactionManager")
class PrimaryJpaConfig {}

@EnableJpaRepositories(
    basePackageClasses = Customer.class,
    entityManagerFactoryRef = "secondEntityManagerFactory",
    transactionManagerRef = "secondTransactionManager")
class SecondaryJpaConfig {}
```

**Listing 2.** Route repositories to the correct persistence unit by package and bean refs.

Use `EntityManagerFactoryBuilder` (from Boot auto-config) for secondary factories so `spring.jpa.*` vendor settings are retained. Mark secondary JPA beans `defaultCandidate = false` so they do not displace the primary auto-configured ones.

> [!warning] Two datasources ≠ one transaction
> Each `JpaTransactionManager` coordinates one database. A method that writes to both needs distributed transactions (JTA) or explicit two-phase orchestration — not a single `@Transactional` boundary by default.

See [[How do you connect a Spring Boot application to a database]] and [[What is Spring Data JPA]].

> [!tip] Interview answer
> I declare multiple `DataSource` beans with separate `@ConfigurationProperties` prefixes, mark one `@Primary`, and qualify the rest. For JPA I configure an `EntityManagerFactory` and `JpaTransactionManager` per database and split `@EnableJpaRepositories` by package with `entityManagerFactoryRef`. A second datasource bean alone is not enough for two JPA persistence units.
