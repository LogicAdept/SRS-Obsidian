<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How do you call a stored procedure from Java?

> [!abstract] Short answer
> Use **`Connection.prepareCall`** to get a **`CallableStatement`**, pass JDBC **call-escape** SQL (`{call name(?)}` or `{? = call name(?)}`), **`setXxx` IN** values, **`registerOutParameter` every OUT** (including a function return) **before** execute, then **`execute`** (or `executeQuery` / `executeUpdate` when the result shape is a single set or a count). Drain **result sets and update counts first**, then **`getXxx` OUT** values. `CallableStatement` extends `PreparedStatement`; use the **no-arg** execute methods.

## JDBC call escape and `prepareCall`

JDBC’s portable way to invoke a stored procedure is the **stored-procedure escape** on a `CallableStatement` from `prepareCall`. Two forms:

```text
{?= call procedure-name[(arg1, arg2, ...)]}
{call procedure-name[(arg1, arg2, ...)]}
```

**Listing 1.** Conceptual JDBC call escapes (Java SE 26 `CallableStatement`). The `{?= …}` result parameter is an **OUT** parameter and must be registered. Other parameters are IN, OUT, or both. Indexes are **1-based**.

`DatabaseMetaData.supportsStoredProcedures()` reports whether the database supports calls that use this escape. `prepareCall` is optimized for procedure calls; some drivers send the text at prepare time, others wait until execute — that only changes **which method** may throw `SQLException`. Named `setXxx` / `registerOutParameter(String, …)` exist from JDBC 3 / Java 1.4 when the driver supports named parameters.

```d2
direction: right
prep: "prepareCall\nescape SQL" {
  width: 200
  height: 75
  style.fill: "#fff3e0"
}
bind: "setXxx IN\nregisterOutParameter" {
  width: 250
  height: 75
  style.fill: "#e3f2fd"
}
run: "execute / executeQuery" {
  width: 220
  height: 75
  style.fill: "#e8f5e9"
}
out: "drain ResultSets\nthen getXxx OUT" {
  width: 240
  height: 75
  style.fill: "#f3e5f5"
}

prep -> bind -> run -> out
```

**Fig. 1.** Register OUT **before** execute. Read OUT **after** result sets and update counts ([[How do execute, executeQuery, and executeUpdate differ in JDBC]]).

## Bind, register, execute, read

IN values use `PreparedStatement` setters (`setInt`, `setString`, …). **All OUT parameters must be registered** with `registerOutParameter(index, sqlType)` (or by name) **before** the procedure runs. The JDBC type you register picks the `getXxx` you must use afterward (`Types.INTEGER` → `getInt`, vendor-specific → `Types.OTHER` and `getObject`). For `NUMERIC` / `DECIMAL`, use the overload with **scale**. An INOUT parameter is **set** and **registered**.

A `CallableStatement` may return **one or several** `ResultSet`s; walk them with `getResultSet` / `getMoreResults` inherited from `Statement` ([[How are database query results processed in JDBC]]). Then read OUT parameters with `getXxx`. After a primitive getter, `wasNull()` tells you if that OUT was SQL `NULL`.

```java
import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Types;

public final class CallStoredProcedure {
    public static int plus(Connection con, int a, int b) throws SQLException {
        try (CallableStatement cs = con.prepareCall("{? = call plus(?, ?)}")) {
            cs.registerOutParameter(1, Types.INTEGER);
            cs.setInt(2, a);
            cs.setInt(3, b);
            cs.execute();
            int value = cs.getInt(1);
            if (cs.wasNull()) {
                throw new SQLException("plus returned SQL NULL");
            }
            return value;
        }
    }

    public static void namesInDept(Connection con, int deptId) throws SQLException {
        try (CallableStatement cs = con.prepareCall("{call names_in_dept(?)}")) {
            cs.setInt(1, deptId);
            boolean isResultSet = cs.execute();
            while (true) {
                if (isResultSet) {
                    try (ResultSet rs = cs.getResultSet()) {
                        while (rs.next()) {
                            rs.getString(1);
                        }
                    }
                } else if (cs.getUpdateCount() == -1) {
                    break;
                }
                isResultSet = cs.getMoreResults();
            }
        }
    }
}
```

**Listing 2.** Function-style return (`{? = call …}`) vs a procedure that yields a result set. `executeQuery(String)` on this object **throws** — SQL is already in `prepareCall` ([[How do JDBC interface types such as Statement and PreparedStatement differ]]).

Spring’s `SimpleJdbcCall` / `JdbcTemplate` is a wrapper over the same JDBC types ([[How do you call stored procedures in Spring JDBC]], [[What is SimpleJdbcCall]]), not a second protocol. If you do not know the signature, `DatabaseMetaData.getProcedures` / `getProcedureColumns` describe procedures (you may still lack **execute** permission). A procedure with **only IN** still belongs on **`prepareCall`** — do not pick `Statement` / `PreparedStatement` / `CallableStatement` by parameter count.

> [!warning] Do not pick `Statement` / `PreparedStatement` / `CallableStatement` by parameter count
> JDBC’s procedure API is **`CallableStatement`**. IN setters are inherited. OUT registration exists only there. A no-arg procedure is still `prepareCall`, not `Statement`.

> [!warning] Register OUT before execute; read OUT after result sets
> Missing `registerOutParameter` is illegal. For portability, process **every** `ResultSet` and update count **before** `getXxx` on OUT parameters. `wasNull()` is only meaningful **after** a getter.

> [!warning] Escape support is a database capability
> `supportsStoredProcedures()` is specifically “calls that use the stored procedure **escape syntax**,” not “the server has procedures.” Native `CALL` / `EXEC` strings are vendor SQL; the portable JDBC form is `{call …}`.

> [!warning] `CallableStatement` is not a `Statement` you pass SQL into at execute time
> Use no-arg `execute` / `executeQuery` / `executeUpdate`. The inherited `String` overloads throw. Concatenating arguments into the call string bypasses IN binding the same way concatenating into `Statement` SQL does.

> [!tip] Interview answer
> From Java you call a stored procedure with `prepareCall` and JDBC `{call name(?)}` or `{? = call name(?)}` on a `CallableStatement`. Set IN parameters, register every OUT parameter before execute, run it, consume result sets, then get OUT values. It extends `PreparedStatement`, so use the no-arg execute methods.

## See also

- [[What JDBC statement types exist]]
- [[How do you call stored procedures in Spring JDBC]]
- [[What is SimpleJdbcCall]]
- [[Why must JDBC and IO resources be closed explicitly]]
