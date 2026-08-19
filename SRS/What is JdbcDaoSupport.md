<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

DEBAGanov lists `JdbcDaoSupport` among Spring DAO convenience superclasses (`JdbcDaoSupport`, `HibernateDaoSupport`, `JdoDaoSupport`, `JpaDaoSupport`) so JDBC DAOs share a common support base.

The same note says `HibernateDaoSupport` exposes `getHibernateTemplate()` and wraps checked Hibernate exceptions as runtime exceptions. The JDBC analogue is the JDBC support class in that list.

> [!warning] Unverified traps from the dump
> - The dump does not show `getJdbcTemplate()` sample code for `JdbcDaoSupport`.
> - Exam notes inject `JdbcTemplate` into a repository without extending `JdbcDaoSupport`.

