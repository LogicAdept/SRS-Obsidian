<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Java Code Geeks: Spring DAO support is meant to make JDBC, Hibernate, or JDO usable the same way, so you can switch persistence technologies more easily and avoid catching technology-specific exceptions.

DEBAGanov: Spring DAO gives convenient data access for JDBC/Hibernate and names support superclasses: `JdbcDaoSupport`, `HibernateDaoSupport`, `JdoDaoSupport`, `JpaDaoSupport`.

> [!warning] Unverified traps from the dump
> - `JdbcDaoSupport` is legacy-style in many codebases; dumps still list it. Constructor-injected `JdbcTemplate` is what the exam-notes repository example actually uses.
> - Switching JDBC to Hibernate is not a one-annotation change just because DAO support exists.

