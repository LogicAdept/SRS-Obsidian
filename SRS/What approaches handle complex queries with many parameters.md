<!--
reps: 0
priority: 0
-->
#Databases/SQL #Java/JDBC #Java/Spring/Framework/DataAccess #SRS

# What approaches handle complex queries with many parameters?

> [!abstract] Short answer
> Bind **values**; do not concatenate them into SQL. Core JDBC uses **positional `?`** on **`PreparedStatement`** (`setXxx`, 1-based). With **many** parameters that indexing gets brittle — use **named** binds where the API has them: Spring **`NamedParameterJdbcTemplate`** / **`JdbcClient`** (`:name` + `SqlParameterSource` / `Map`), JPA/Hibernate **`:name`** (`Query.setParameter(name, value)`), **`CallableStatement.setXxx(parameterName, …)`** for procedures. For **many optional predicates**, build the SQL/Criteria **structure** in code and still **bind** every value. Hibernate: named parameters “tend to be easier to read” when there are several.

## Positional JDBC vs named layers

`PreparedStatement` stores one SQL string with **`?` IN markers**. Setters take a **1-based index**. That is the JDBC way to pass many values without SQL injection ([[How does PreparedStatement mitigate SQL injection compared to Statement]], [[How do JDBC interface types such as Statement and PreparedStatement differ]]). There is **no** `:name` syntax in `java.sql.PreparedStatement`.

`CallableStatement` still documents parameters “by number, with the first parameter being 1,” and also has **`setString(String parameterName, …)`** (and the rest) for **named** procedure parameters.

Spring JDBC adds names **on top of** JDBC: `NamedParameterJdbcTemplate` wraps `JdbcTemplate` so SQL can use `:first_name` instead of only `'?'`. Values come from a **`Map`**, **`MapSqlParameterSource`**, or **`BeanPropertySqlParameterSource`** (JavaBean properties → names). As of 6.1, **`JdbcClient`** is the fluent API for named **or** indexed binds ([[What is NamedParameterJdbcTemplate]], [[How do you use NamedParameterJdbcTemplate with SqlParameterSource]], [[What is the difference between JdbcTemplate and NamedParameterJdbcTemplate]]).

Jakarta Persistence `Query.setParameter(String name, Object value)` binds a **named** parameter. Hibernate: ordinal `?1` exists, but **named** is the readability choice when a query has **multiple** parameters. Never concatenate user input into HQL ([[What advantages does Hibernate provide over plain JDBC]]).

**Criteria** (JPA) builds predicates in Java when the **shape** of the query is the complexity (optional filters), not only the count of binds ([[What is the JPA Criteria API]]).

| Approach | Where | How you pass many values |
| --- | --- | --- |
| `PreparedStatement` `?` | JDBC | `setXxx(1…)`; you count indexes |
| `CallableStatement` names | JDBC procedures | `setXxx("p_name", …)` plus ordinal |
| `NamedParameterJdbcTemplate` / `JdbcClient` | Spring JDBC | `:name` + map/bean |
| JPQL/HQL `:name` | JPA / Hibernate | `setParameter("name", value)` |
| Criteria | JPA | `ParameterExpression` / `setParameter`; dynamic `WHERE` |

```d2
direction: down
bad: "String + user text" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}
pos: "JDBC ? + setXxx(i)" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
named: ":name + setParameter / Spring map" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

bad -> pos: "bind"
pos -> named: "many params"
```

**Fig. 1.** Safety is binding. Names are for **keeping indexes straight** when the SQL is large.

```java
import org.springframework.jdbc.core.namedparam.MapSqlParameterSource;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;

public final class ManyParams {
    public static int count(NamedParameterJdbcTemplate jdbc, String first, String last) {
        return jdbc.queryForObject(
                "SELECT count(*) FROM t_actor WHERE first_name = :firstName AND last_name = :lastName",
                new MapSqlParameterSource()
                        .addValue("firstName", first)
                        .addValue("lastName", last),
                Integer.class);
    }
}
```

**Listing 1.** Spring named binds (official `NamedParameterJdbcTemplate` example shape). The driver still receives positional `?` after Spring rewrites. Same idea in JPA: `"… WHERE title LIKE :pattern"` then `setParameter("pattern", value)`.

For a **variable-length `IN` list**, add one placeholder **per** element (or a vendor array bind). Do not splice the list into the SQL as literals.

> [!warning] Core JDBC has no `:named` on `PreparedStatement`
> Names are Spring, JPA/HQL, or `CallableStatement` name overloads. Concatenating values is still injection even inside a “dynamic WHERE” builder.

> [!warning] Off-by-one on `?` is the many-parameter bug
> Indexes are **1-based**. Reordering columns without renaming binds is why named parameters exist. `BeanPropertySqlParameterSource` only helps if SQL names **match** bean properties.

> [!tip] Interview answer
> Use a prepared statement and bind every value — never concatenate. JDBC itself is positional `?` with 1-based setters, which gets messy with many parameters. Prefer named parameters: Spring `:name` with `NamedParameterJdbcTemplate` or `JdbcClient`, JPA/Hibernate `:name` with `setParameter`, and named setters on `CallableStatement` for procedures. For optional filters, compose the query in code and still bind.

