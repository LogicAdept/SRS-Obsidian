<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview Q&A: the Spring `StoredProcedure` class calls a database stored procedure from a Spring app. You encapsulate the procedure, define input and output parameters, handle exception conditions, and execute it without treating the procedure as ad-hoc SQL in every DAO method.

> [!warning] Unverified traps from the dump
> - Climb’s stored-procedure answer does not mention this class; it mentions `SimpleJdbcCall` and `JdbcTemplate` `execute`/`call` instead.

