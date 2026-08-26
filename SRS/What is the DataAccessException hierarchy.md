<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS

# What is the `DataAccessException` hierarchy?

> [!abstract] Short answer
> **`DataAccessException`** is the **unchecked root** (`NestedRuntimeException`) of Spring’s **data-access** exceptions. User code can catch **kind of failure** (integrity, bad SQL, optimistic lock) **without** knowing JDBC vs JPA. JDBC’s checked **`SQLException`** is wrapped; the **cause is kept**. The tree is **shared** across JDBC templates and ORM — not JDBC-only. Catch a **specific subclass** or treat most as fatal (javadoc: you need not catch if errors are fatal).

## Portable types, vendor in the cause

Javadoc: react to **optimistic locking failure** without knowing JDBC is in use. DAO chapter: JDBC, JPA, and Hibernate exceptions convert into the **same** `org.springframework.dao` tree.

Examples you will actually see:

| Type | Typical meaning |
| --- | --- |
| **`DataIntegrityViolationException`** | Constraint / unique (superclass of **`DuplicateKeyException`**; docs: often catch this, not only the subclass) |
| **`BadSqlGrammarException`** | Invalid SQL (`org.springframework.jdbc`, always has `SQLException` cause) |
| **`OptimisticLockingFailureException`** | Version / optimistic lock |
| **`DataAccessResourceFailureException`** | Resource (connection) failure |
| **`EmptyResultDataAccessException` / `IncorrectResultSizeDataAccessException`** | `queryForObject` row-count mismatch |

Dump lists are **incomplete**. **`CleanupFailureDataAccessException` is `@Deprecated` since 6.0.3** (not used in core JDBC/ORM). Translation SPI: [[How does Spring JDBC translate SQLException]]. Reads: [[What is the difference between query and queryForObject in JdbcTemplate]].

```d2
direction: down
root: "DataAccessException\n(unchecked)" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
intg: "DataIntegrityViolationException" {
  width: 300
  height: 45
  style.fill: "#ffebee"
}
sql: "BadSqlGrammarException" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}

root -> intg
root -> sql
```

**Fig. 1.** Same root for [[What is Spring JDBC]] and JPA DAOs — [[What is Spring DAO support]].

> [!warning] Not a JDBC-only hierarchy
> `@Repository` translation uses the **same** types for Hibernate/`EntityManager` failures.

> [!warning] Do not catch `SQLException` on `JdbcTemplate` APIs
> Those methods throw **`DataAccessException`**. Unwrap **`getCause()`** if you need the vendor code.

> [!tip] Interview answer
> **`DataAccessException` is Spring’s unchecked data-access root so you catch “integrity” or “bad SQL” without vendor types.** `JdbcTemplate` maps `SQLException` into that tree. Lists of subclasses in interviews are samples, not the full set. `CleanupFailureDataAccessException` is deprecated unused core.

## See also

- [[How does Spring JDBC translate SQLException]]
- [[What is Spring DAO support]]
- [[What is Spring JdbcTemplate]]
- [[What is the difference between JDBC and Spring JDBC]]
- [[What is Spring JDBC]]
