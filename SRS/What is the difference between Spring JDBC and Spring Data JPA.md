<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/Spring/Data/JPA #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Exam notes:

- JDBC repositories are classes with method bodies. Spring Data JPA repositories are interfaces; methods often need no implementation.
- JDBC needs a `JdbcTemplate` bean, often constructor-injected. Spring Data JPA does not; operations follow method names.
- JDBC domain classes are not annotated; mapping lives in repository callbacks. JPA uses `@Entity`, `@Table`, `@Id`, and the rest of ORM.
- Custom SQL in JDBC is a string in the Java method. Custom SQL in Spring Data JPA is `@Query` on the interface method.

You can still use JDBC in Boot or JPA on plain Framework; the course just taught them in those contexts. Both styles can return domain objects without the caller mapping `ResultSet` by hand (JDBC via `RowMapper`; walking `ResultSet` with `ResultSetExtractor` is called exceptional).

> [!warning] Unverified traps from the dump
> - This is not “JDBC vs Hibernate”; JPA repositories versus `JdbcTemplate` DAOs is the split those notes actually make.

