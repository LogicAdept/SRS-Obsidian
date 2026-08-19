<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring JDBC dumps: JDBC throws checked `SQLException` with vendor/database details. Spring instead throws `DataAccessException`, an unchecked `RuntimeException`, as the parent of more specific types that describe the problem without embedding database-product messaging.

Exam notes list example subtypes: `DataAccessResourceFailureException`, `CleanupFailureDataAccessException`, `OptimisticLockingFailureException`, `DataIntegrityViolationException`, `BadSqlGrammarException`.

Interview text: catch the type you need in a structured hierarchy rather than a single generic JDBC error.

> [!warning] Unverified traps from the dump
> - The same hierarchy is also how dumps describe `@Repository` wrapping persistence exceptions — not JDBC-only.
> - Subtype lists in tutorials are incomplete; dumps say “there are more”.

