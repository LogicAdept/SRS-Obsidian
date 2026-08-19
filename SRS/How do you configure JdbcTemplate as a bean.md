<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A Spring JDBC Q&A says Java config is a `@Configuration` class that declares `DataSource`, `JdbcTemplate`, and related JDBC components as `@Bean` methods.

An exam-notes page constructs `JdbcTemplate` as `new JdbcTemplate(dataSource)` and constructor-injects that template into a repository bean. The same page says a typical JDBC setup is three beans: `dataSource`, `jdbcTemplate`, and the repository.

> [!warning] Unverified traps from the dump
> - Spring Boot with `spring-jdbc` is described elsewhere as creating `JdbcTemplate` for you; this card is the explicit Framework wiring dumps show.
> - Do not confuse this with Spring Data JPA, which those notes say does not need a `JdbcTemplate` bean.

