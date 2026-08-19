<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Climb: Spring translates database-specific exceptions into more generic ones so code can be portable across databases, with a consistent approach across layers.

`JdbcTemplate` dumps: it catches JDBC exceptions and maps them into `org.springframework.dao`. Exam notes: Spring does not want checked exceptions, generic `SQLException`, or vendor strings in the type you catch; it throws unchecked `DataAccessException` instead and expects handling higher up without `throws` on every method.

> [!warning] Unverified traps from the dump
> - `@Repository` exception translation is the AOP/proxy story dumps attach to the stereotype; `JdbcTemplate` translation is the template story. They are related, not identical one-liners.
> - Dumps do not name `SQLExceptionTranslator` as the SPI in the interview answers used here.

