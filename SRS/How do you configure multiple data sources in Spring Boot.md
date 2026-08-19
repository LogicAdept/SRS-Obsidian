<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Data #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Define more than one `DataSource` bean. Mark one `@Primary` so unqualified injection and auto-config still have a default. Bind each to its own prefix with `@ConfigurationProperties`.

```java
@Configuration
public class DataSourceConfig {
    @Bean
    @Primary
    @ConfigurationProperties("spring.datasource.primary")
    public DataSource primaryDataSource() {
        return DataSourceBuilder.create().build();
    }

    @Bean
    @ConfigurationProperties("spring.datasource.secondary")
    public DataSource secondaryDataSource() {
        return DataSourceBuilder.create().build();
    }
}
```

Each DataSource typically needs its own `EntityManagerFactory` / `TransactionManager` / `@EnableJpaRepositories` `entityManagerFactoryRef` if you use JPA on both.

> [!warning] Unverified traps from the dump
> - Two DataSource beans without `@Primary` blow up auto-config (`DataSource` injection is ambiguous).
> - A second DataSource alone is not enough for two JPA units — you still split EMF and transaction managers.
