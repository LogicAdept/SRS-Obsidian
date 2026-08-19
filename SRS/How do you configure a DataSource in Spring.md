<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps say you define a `DataSource` bean in XML or `@Configuration` Java config, with URL, username, and password. A GitHub Spring interview dump uses `org.springframework.jdbc.datasource.DriverManagerDataSource` and sets `driverClassName`, `url`, `username`, and `password`.

in28minutes shows a pooled variant: `com.mchange.v2.c3p0.ComboPooledDataSource` with `driverClass`, `jdbcUrl`, `user`, `password`, and `destroy-method="close"`, values taken from properties.

Interview lists also say you can add connection-pooling settings on that bean. A `@Bean` returning `DataSourceBuilder.create().url(...).username(...).password(...).build()` appears in a 2026 JDBC/JPA question dump.

> [!warning] Unverified traps from the dump
> - `DriverManagerDataSource` in dumps is a simple helper, not a production pool. HikariCP is a different card (`What is HikariCP in Spring Boot`).
> - Boot auto-config of a DataSource from `application.properties` is not the same as this explicit Framework bean.

