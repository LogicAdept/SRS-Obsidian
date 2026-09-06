<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How does JDBC ResultSet behave and what configuration options exist?

> [!abstract] Short answer
> A **`ResultSet`** is a table with a **cursor** that starts **before** the first row. You walk it with **`next()`** and read columns with **1-based `getXxx`**. The **default** set is **`TYPE_FORWARD_ONLY`** and **`CONCUR_READ_ONLY`**: one forward pass, not updatable. You configure **type**, **concurrency**, and **holdability** on `createStatement` / `prepareStatement`; **fetch size** and **fetch direction** are **hints**. Drivers may not implement every combination — ask **`DatabaseMetaData.supportsResultSetType` / `supportsResultSetConcurrency`**.

## Default cursor behavior

`ResultSet` “maintains a cursor pointing to its current row.” Initially the cursor is **before** the first row. `next()` advances it; `false` means **after the last row**, and getters that need a current row throw `SQLException`. On `TYPE_FORWARD_ONLY`, a **further** `next()` after that is **vendor-specified** (`false` or `SQLException`).

Columns are numbered from **1**. Labels are case-insensitive; duplicate names return the **first** match. For portability, read columns **left to right** and **once** per row. Primitive getters turn SQL `NULL` into `0`/`false` — call **`wasNull()`** after the getter ([[How are database query results processed in JDBC]]).

The generating `Statement` **auto-closes** the current `ResultSet` on `close`, re-execute, or `getMoreResults`. Default: **one** open `ResultSet` per `Statement` ([[What is JDBC ResultSet]]).

## Configuration: type, concurrency, holdability, fetch

`Connection.createStatement()` (and default `prepareStatement`) produce **`TYPE_FORWARD_ONLY`** + **`CONCUR_READ_ONLY`**. Overloads take type, concurrency, and (Java 1.4+) holdability. `SQLFeatureNotSupportedException` if the driver rejects the combo.

| Knob | Constants | Meaning |
| --- | --- | --- |
| **Type** | `TYPE_FORWARD_ONLY` | Cursor **only forward**; `absolute` / `relative` / `previous` throw |
| | `TYPE_SCROLL_INSENSITIVE` | Scrollable; **generally not** sensitive to underlying data changes |
| | `TYPE_SCROLL_SENSITIVE` | Scrollable; **generally** sensitive to those changes |
| **Concurrency** | `CONCUR_READ_ONLY` | May **not** be updated |
| | `CONCUR_UPDATABLE` | May be updated (`updateXxx` / `updateRow` / insert row) |
| **Holdability** | `HOLD_CURSORS_OVER_COMMIT` | Stay open across **commit** |
| | `CLOSE_CURSORS_AT_COMMIT` | Closed on **commit** |

Default holdability is **`DatabaseMetaData.getResultSetHoldability()`**. Probe support with `supportsResultSetType(type)` and `supportsResultSetConcurrency(type, concurrency)` ([[How would you explain ResultSet types scrolling and concurrency modes]]).

**Fetch direction** (`FETCH_FORWARD` / `FETCH_REVERSE` / `FETCH_UNKNOWN`) is a **hint**. Initial value comes from the `Statement`. On `TYPE_FORWARD_ONLY`, only **`FETCH_FORWARD`** is legal. **Fetch size** is a hint for how many rows to pull when more are needed; **`0`** means the driver **ignores** it and guesses. Default fetch size comes from the `Statement`; both may be changed later (`rows >= 0`).

Scrollable sets: `absolute(1)` ≡ `first()`, `absolute(-1)` ≡ `last()`, `absolute(0)` ≡ before first. `relative(1)` ≡ `next()`.

```d2
direction: right
def: "default\nFORWARD_ONLY\nREAD_ONLY" {
  width: 200
  height: 80
  style.fill: "#fff3e0"
}
scroll: "SCROLL_INSENSITIVE\nor SENSITIVE" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
upd: "CONCUR_UPDATABLE" {
  width: 200
  height: 80
  style.fill: "#e8f5e9"
}

def -> scroll
scroll -> upd
```

**Fig. 1.** Default is one-way read-only. Scrolling and updates are extra `createStatement` arguments, not ResultSet defaults.

```java
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public final class ResultSetConfig {
    public static Statement scrollable(Connection con) throws SQLException {
        return con.createStatement(
                ResultSet.TYPE_SCROLL_INSENSITIVE,
                ResultSet.CONCUR_READ_ONLY);
    }
}
```

**Listing 1.** Request a scrollable, read-only set. Holdability uses the three-argument `createStatement` if you need it. Closing the `Statement` still closes the `ResultSet` ([[How do you close a database connection properly]]).

> [!warning] `next()` before getters; default sets are one-pass
> The cursor starts **before** row 1. A default `TYPE_FORWARD_ONLY` set cannot be rewound. `absolute` on that type throws `SQLException`.

> [!warning] Type and concurrency are requests, not guarantees
> Unsupported combinations throw **`SQLFeatureNotSupportedException`** (or fail at execute). Check metadata. Fetch size **0** is not “no rows” — the driver **ignores** the hint.

> [!warning] Re-execute or `getMoreResults` destroys the current set
> Holdability is about **commit**, not about keeping a set after the statement runs again. `Blob`/`Clob` from the set are **not** closed by `ResultSet.close()`.

> [!tip] Interview answer
> A ResultSet is a cursor that starts before the first row; you loop `next()` and `getXxx`. Defaults are forward-only and read-only. You can ask for scrollable and/or updatable sets, and hold-over-commit vs close-at-commit, plus fetch-size hints. The driver may refuse a combination; `DatabaseMetaData` tells you what exists.

## See also

- [[How do execute, executeQuery, and executeUpdate differ in JDBC]]
- [[What are database cursors in JDBC and SQL]]
- [[How would you explain ResultSet types scrolling and concurrency modes]]
