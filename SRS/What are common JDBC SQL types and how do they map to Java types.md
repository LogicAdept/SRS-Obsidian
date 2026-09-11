<!--
reps: 0
priority: 0
-->
#Java/JDBC #Databases/SQL/DataTypes #SRS

# What are common JDBC SQL types and how do they map to Java types?

> [!abstract] Short answer
> JDBC **SQL types** are the **`java.sql.Types`** / **`JDBCType`** codes (`VARCHAR`, `INTEGER`, `TIMESTAMP`, …), not the vendor’s type name. The **recommended** mapping (what `getInt` / `setInt` use) is: strings → `String`, `INTEGER` → `int`, `BIGINT` → `long`, `DECIMAL`/`NUMERIC` → `BigDecimal`, `DATE`/`TIME`/`TIMESTAMP` → `java.sql.Date`/`Time`/`Timestamp`, binaries → `byte[]`. **`getObject`** uses **wrappers** and maps `TINYINT`/`SMALLINT` to **`Integer`**, not `Byte`/`Short`. JDBC **`FLOAT`** maps to Java **`double`**.

## Common codes and the two mappings

`Types` “defines the constants that are used to identify generic SQL types, called JDBC types.” Drivers map product names onto these codes. `ResultSet.getObject` returns the **default Java object type** from the JDBC spec. Typed getters/setters follow the **recommended** Java type (`VARCHAR` → `getString`, `INTEGER` → `getInt`) ([[How are database query results processed in JDBC]]).

| JDBC type | Recommended Java | `getObject` |
| --- | --- | --- |
| `CHAR` / `VARCHAR` / `LONGVARCHAR` | `String` | `String` |
| `NCHAR` / `NVARCHAR` / `LONGNVARCHAR` | `String` (`getNString`) | `String` |
| `NUMERIC` / `DECIMAL` | `BigDecimal` | `BigDecimal` |
| `BIT` / `BOOLEAN` | `boolean` | `Boolean` |
| `TINYINT` | `byte` | **`Integer`** |
| `SMALLINT` | `short` | **`Integer`** |
| `INTEGER` | `int` | `Integer` |
| `BIGINT` | `long` | `Long` |
| `REAL` | `float` | `Float` |
| `FLOAT` / `DOUBLE` | **`double`** | `Double` |
| `BINARY` / `VARBINARY` / `LONGVARBINARY` | `byte[]` | `byte[]` |
| `DATE` / `TIME` / `TIMESTAMP` | `java.sql.Date` / `Time` / `Timestamp` | same |
| `CLOB` / `BLOB` / `ARRAY` | `Clob` / `Blob` / `Array` | same |

`setInt` sends SQL `INTEGER`; `setString` sends `VARCHAR` or `LONGVARCHAR`; `setBoolean` sends `BIT` or `BOOLEAN`. `CHAR(n)` values may be **space-padded**. Primitive getters turn SQL `NULL` into `0`/`false` — call **`wasNull()`**. `getObject` returns Java `null`.

Less common but in `Types`: `NCLOB`, `SQLXML`, `ROWID`, `DATALINK` (`java.net.URL`), `REF`, `STRUCT`, `DISTINCT` (mapping of the **base** type), `TIME_WITH_TIMEZONE` / `TIMESTAMP_WITH_TIMEZONE`, `REF_CURSOR`, and (Java 26) `JSON` / `DECFLOAT`. `OTHER` is vendor-specific via `getObject` / `setObject`.

```d2
direction: right
code: "Types.INTEGER" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}
g: "getInt → int" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
o: "getObject → Integer" {
  width: 180
  height: 55
  style.fill: "#f3e5f5"
}

code -> g
code -> o
```

**Fig. 1.** Same JDBC type, two Java shapes. Interview tables that show only `Integer` are the **`getObject`** table.

```java
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Types;

public final class CommonJdbcTypes {
    public static void bind(PreparedStatement ps, int id, String name)
            throws SQLException {
        ps.setInt(1, id);
        ps.setString(2, name);
        ps.setNull(3, Types.TIMESTAMP);
    }

    public static Integer readId(ResultSet rs) throws SQLException {
        int id = rs.getInt("id");
        return rs.wasNull() ? null : id;
    }
}
```

**Listing 1.** Recommended binds (`INTEGER`, `VARCHAR`). `setNull` needs a `Types` code. `getInt` cannot express SQL `NULL` without `wasNull()` ([[How does JDBC ResultSet behave and what configuration options exist]]).

> [!warning] `getObject` on `TINYINT` is `Integer`, not `Byte`
> Recommended: `getByte` / `setByte`. The object mapping also sends `SMALLINT` → `Integer` and `FLOAT` → `Double`. Do not treat JDBC `FLOAT` as Java `float` (`REAL` is `float`).

> [!warning] These are generic JDBC types, not PostgreSQL/`NUMBER` names
> Use `DatabaseMetaData.getTypeInfo` for what the database actually has. `java.sql.Date` is not `java.util.Date` as the column mapping. `CHAR(n)` values may arrive **space-padded** to length `n`.

> [!tip] Interview answer
> Common JDBC types live in `java.sql.Types`: `VARCHAR`→`String`, `INTEGER`→`int`, `BIGINT`→`long`, `DECIMAL`→`BigDecimal`, `TIMESTAMP`→`java.sql.Timestamp`, `BLOB`→`Blob`. `getObject` boxes primitives and maps `TINYINT`/`SMALLINT` to `Integer`. Always `wasNull()` after primitive getters.

