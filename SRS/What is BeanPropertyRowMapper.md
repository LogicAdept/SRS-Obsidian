<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview dumps use `new BeanPropertyRowMapper<>(User.class)` or `new BeanPropertyRowMapper(Todo.class)` as the `RowMapper` passed to `JdbcTemplate.query`, so column values are copied onto bean properties instead of a handwritten `mapRow`.

in28minutes places that one-liner next to a full custom `RowMapper` implementation as the two Spring JDBC mapping styles.

> [!warning] Unverified traps from the dump
> - The dumps do not spell the column-to-property naming rules. If names do not line up, the custom `RowMapper` in the same dump is the fallback they actually show.
> - This is not JPA `@Entity` mapping. Domain classes in Spring JDBC notes are typically not annotated.

