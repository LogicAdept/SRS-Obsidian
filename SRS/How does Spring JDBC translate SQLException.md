<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# How does Spring JDBC translate `SQLException`?

> [!abstract] Short answer
> **`JdbcTemplate` does not propagate `SQLException`.** An **`SQLExceptionTranslator`** maps it to **`org.springframework.dao.DataAccessException`** (unchecked, technology-agnostic). As of Framework **6.0**, the **default** translator is **`SQLExceptionSubclassTranslator`** (JDBC 4 subclasses + **`SQLState`** fallback). Vendor error-code XML (`sql-error-codes.xml` + **`SQLErrorCodeSQLExceptionTranslator`**) is **opt-in / more precise**, not the 6.0 default. **`@Repository`** AOP translation is a **second** path for code that is not already going through the template.

## Template SPI vs stereotype

Spring *Using SQLExceptionTranslator*: used behind **`JdbcTemplate`** and **`JdbcTransactionManager`**. Implementations: generic (**SQLState**) or vendor codes (Oracle, …).

**6.0 default:** `SQLExceptionSubclassTranslator` — usually enough; no vendor file required. **`SQLErrorCodeSQLExceptionTranslator`** applies when **`sql-error-codes.xml`** is on the classpath root (or you set it). Match order for that class: subclass custom → `customSqlExceptionTranslator` → `CustomSQLErrorCodesTranslation` list → error codes → fallback subclass/SQLState translators.

```java
jdbcTemplate.setExceptionTranslator(new CustomSQLErrorCodesTranslator());
```

**Listing 1.** Conceptual — docs pass a custom translator into the template used for that DAO. Hierarchy: [[What is the DataAccessException hierarchy]]. Template: [[What is Spring JdbcTemplate]].

DAO support: **`@Repository`** + exception-translation post-processor wraps persistence exceptions for **JPA/Hibernate/JDBC DAOs** that might otherwise leak vendor types — [[What is Spring DAO support]]. `JdbcTemplate` already translates; the annotation still matters for **component scan** and for **non-template** code.

```d2
direction: down
sql: "SQLException" {
  width: 180
  height: 45
  style.fill: "#ffebee"
}
tr: "SQLExceptionTranslator" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
dae: "DataAccessException" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

sql -> tr -> dae
```

**Fig. 1.** Callers catch `DuplicateKeyException` / `BadSqlGrammarException`, not `ORA-00001`. Portable DAOs: [[What is the difference between JDBC and Spring JDBC]].

> [!warning] Checked `SQLException` is gone on the template API
> Methods throw **`DataAccessException`**. Do not declare `throws SQLException` on a `JdbcTemplate` DAO.

> [!warning] 6.0 default is not error-code XML
> Interview answers that only name `sql-error-codes.xml` describe the **precise vendor** translator, not today’s default.

> [!tip] Interview answer
> **`JdbcTemplate` catches `SQLException` and throws `DataAccessException` via `SQLExceptionTranslator`.** Default since 6.0 is subclass/SQLState translation. Vendor codes are optional. `@Repository` is extra translation/scan, not a substitute for the template.

## See also

- [[What is the DataAccessException hierarchy]]
- [[What is Spring JdbcTemplate]]
- [[What is Spring DAO support]]
- [[What is Spring JDBC]]
