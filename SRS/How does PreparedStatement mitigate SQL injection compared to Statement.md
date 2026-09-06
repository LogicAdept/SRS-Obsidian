<!--
reps: 0
priority: 0
-->
#Java/JDBC #Problems/Persistence #Security/AppSec/Injection #SRS

# How does PreparedStatement mitigate SQL injection compared to Statement?

> [!abstract] Short answer
> **`Statement.executeQuery(String)`** (and the other `String` overloads) send **one SQL string**. If you **concatenate** client text into that string, the engine can treat it as **SQL**, which is SQL injection. **`PreparedStatement`** is created with SQL that may contain **`?` IN markers**; you bind values with **`setXxx`**. Those values are sent as **typed parameter content** (for example `setString` → SQL `VARCHAR`), **not** as more SQL text. That is the mitigation: the statement shape is fixed at prepare; user data cannot change the parse.

## Concatenated SQL vs bound parameters

`Statement` is “the object used for executing a **static** SQL statement.” `executeQuery(String sql)` takes “an SQL statement to be sent to the database, typically a static SQL `SELECT`.” Whatever you put in `sql` is the command. Building it with `+` from request fields is the classic injection bug: quotes, comments, and extra clauses become **code** ([[How would you explain SQL injection attacks and defenses]]).

`Connection.prepareStatement(String sql)` creates a `PreparedStatement` “for sending **parameterized** SQL statements.” The SQL (with or without IN parameters) is stored on the object. `setString` / `setInt` / … fill **1-based** `?` markers. The driver **converts** the Java value to the matching SQL type **when it sends it to the database**. Execute with the **no-arg** `executeQuery` / `executeUpdate` / `execute` — the `String` overloads are illegal on a prepared object ([[How do JDBC interface types such as Statement and PreparedStatement differ]], [[How do execute, executeQuery, and executeUpdate differ in JDBC]]).

Oracle’s JDBC tutorial states the security claim directly: injection exploits **unvalidated string literals concatenated into dynamically built SQL**; prepared statements **always treat client-supplied data as parameter content and never as part of an SQL statement**.

```d2
direction: right
stmt: "Statement\nexecuteQuery(sql)\nsql includes user text" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
ps: "PreparedStatement\nSQL + ? at prepare\nsetXxx then execute()" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}

stmt -> ps: "bind, do not concatenate"
```

**Fig. 1.** Mitigation is **not** the class name. It is **placeholders + setters** versus **string assembly**.

```java
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public final class NameLookup {
    public static String byName(Connection con, String name) throws SQLException {
        try (PreparedStatement ps = con.prepareStatement(
                "SELECT id FROM person WHERE name = ?")) {
            ps.setString(1, name);
            try (ResultSet rs = ps.executeQuery()) {
                return rs.next() ? rs.getString(1) : null;
            }
        }
    }
}
```

**Listing 1.** `name` is a `VARCHAR` bind, including quotes and SQL-looking text. Do **not** write `"… WHERE name = '" + name + "'"`. Closing the statement still closes the set ([[How do you close a database connection properly]]).

Precompilation is a **driver optimization** (`prepareStatement` may send SQL early, or wait until execute). That changes **which call** throws `SQLException`. The injection defense is the **parameter contract**, not whether the driver precompiled.

> [!warning] Concatenating into `prepareStatement` SQL is still injection
> `PreparedStatement` only protects values bound through **`?` + `setXxx`**. Building the SQL string with user input (table names, `ORDER BY` columns, extra `WHERE` fragments) is the same bug as `Statement`. Identifiers are **not** IN parameters.

> [!warning] `Statement` `String` execute methods send whatever you concatenate
> There is no bind API on plain `Statement`. If the value must come from outside the program, use a prepared (or callable) object and setters.

> [!tip] Interview answer
> `Statement` runs a full SQL string; concatenating user input lets that input become SQL. `PreparedStatement` fixes the SQL with `?` markers and binds values with `setXxx`, so the driver sends them as typed data, not as more statement text. That is how JDBC mitigates SQL injection — only if you actually use placeholders, not if you concatenate into the SQL you pass to `prepareStatement`.

## See also

- [[How do JDBC interface types such as Statement and PreparedStatement differ]]
- [[What is the difference between PreparedStatement and Statement in JDBC]]
- [[How would you explain SQL injection attacks and defenses]]
