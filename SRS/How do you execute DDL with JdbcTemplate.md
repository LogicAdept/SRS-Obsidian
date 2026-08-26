<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/DataAccess #Java/JDBC #SRS

# How do you execute DDL with `JdbcTemplate`?

> [!abstract] Short answer
> Use **`jdbcTemplate.execute("create table …")`** (and other **`execute` overloads). Docs: **`execute` runs arbitrary SQL** and is **often used for DDL**. **`update`** is the **DML** path (`insert` / `update` / `delete`). A simple stored-procedure **`CALL`** in the same chapter uses **`update`**, not `execute`.

## `execute` vs `update`

Example from *Other JdbcTemplate Operations*:

```java
this.jdbcTemplate.execute(
        "create table mytable (id integer, name varchar(100))");
```

**Listing 1.** Framework DDL sample. DML: `jdbcTemplate.update("delete from t_actor where id = ?", actorId)`. Template: [[What is Spring JdbcTemplate]].

`execute` is **overloaded**: string SQL, **`ConnectionCallback`**, **`StatementCallback`**, bound arguments. Schema tools (Flyway/Liquibase) are the usual production way to version DDL; that is outside `JdbcTemplate`, not a contradiction of `execute`.

```d2
direction: right
ddl: "CREATE / ALTER / DROP" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
ex: "execute(sql)" {
  width: 160
  height: 45
  style.fill: "#fff3e0"
}
dml: "INSERT / UPDATE / DELETE" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
up: "update(sql, args)" {
  width: 180
  height: 45
  style.fill: "#fce4ec"
}

ddl -> ex
dml -> up
```

**Fig. 1.** Procedures: [[How do you call stored procedures in Spring JDBC]]. Exceptions: [[How does Spring JDBC translate SQLException]].

> [!warning] `DROP` / `TRUNCATE` destroy data
> Spring still runs the SQL. DDL in app startup is a **data-loss** risk. Prefer migrations in real systems.

> [!warning] Do not swap `update` and `execute` by habit
> `update` returns an **affected-row count** for DML. DDL is documented on **`execute`**. Simple `CALL` examples use **`update`**.

> [!tip] Interview answer
> **DDL goes through `JdbcTemplate.execute`.** `update` is for DML. Spring does not forbid DDL; it just runs the statement and still translates `SQLException`.

## See also

- [[What is Spring JdbcTemplate]]
- [[How do you call stored procedures in Spring JDBC]]
- [[How does Spring JDBC translate SQLException]]
