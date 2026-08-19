<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Both simplify Spring JDBC operations. The dump distinction is parameter style: `JdbcTemplate` uses positional `?` placeholders; `NamedParameterJdbcTemplate` uses named parameters so SQL stays readable when many binds exist.

Positional placeholders are called error-prone when the parameter list is long because order must match.

> [!warning] Unverified traps from the dump
> - NamedParameterJdbcTemplate is described as wrapping/delegating to JdbcTemplate, not as a second independent connection stack.
> - You can still get it wrong: names must match the SQL tokens, even if order no longer matters.

