<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Climb: `JdbcTemplate` is thread-safe once configured, so several threads can use the same instance without a dump-described corruption problem on the template itself.

> [!warning] Unverified traps from the dump
> - Thread-safe template is not the same as a thread-safe `DataSource` or a shared mutable `RowMapper` with fields.
> - Configure it once (typically as a Spring singleton bean) in the dumps’ mental model.

