<!--
reps: 0
priority: 0
-->
#Java/JDBC #SRS

# How would you explain ResultSet types scrolling and concurrency modes?

> [!abstract] Short answer
> A default `ResultSet` is **`TYPE_FORWARD_ONLY`** and **`CONCUR_READ_ONLY`**: one forward pass, not updatable. **Type** is cursor motion and whether the set **generally sees** underlying table changes: `TYPE_FORWARD_ONLY`, `TYPE_SCROLL_INSENSITIVE`, `TYPE_SCROLL_SENSITIVE`. **Concurrency** is whether you may update: `CONCUR_READ_ONLY` vs `CONCUR_UPDATABLE`. You request the pair on `createStatement` / `prepareStatement`. Scroll methods (`previous`, `absolute`, `relative`, `first`, `last`) **throw** on `TYPE_FORWARD_ONLY`. Drivers may refuse a combo (`SQLFeatureNotSupportedException`); probe `DatabaseMetaData.supportsResultSetType` / `supportsResultSetConcurrency`.

## Type (scrolling) vs concurrency (updates)

`ResultSet` “maintains a cursor pointing to its current row.” Default: **not updatable**, cursor **forward only**, iterate **once** first→last ([[How does JDBC ResultSet behave and what configuration options exist]]).

| Constant | What it means |
| --- | --- |
| `TYPE_FORWARD_ONLY` | Cursor **may move only forward** (`next`). `previous` / `absolute` / `relative` / `first` / `last` / `beforeFirst` / `afterLast` throw `SQLException` |
| `TYPE_SCROLL_INSENSITIVE` | Scrollable; **generally not** sensitive to changes in the underlying data |
| `TYPE_SCROLL_SENSITIVE` | Scrollable; **generally** sensitive to those changes |
| `CONCUR_READ_ONLY` | May **not** be updated (`updateXxx` / `updateRow` / `insertRow` / `deleteRow` throw) |
| `CONCUR_UPDATABLE` | May be updated |

Type and concurrency are **orthogonal**. The javadoc example is `TYPE_SCROLL_INSENSITIVE` **and** `CONCUR_UPDATABLE`: scrollable, “will not show changes made by others,” and updatable. `getType()` / `getConcurrency()` report what the creating `Statement` actually produced.

**Holdability** (`HOLD_CURSORS_OVER_COMMIT` / `CLOSE_CURSORS_AT_COMMIT`) is a third `createStatement` argument (Java 1.4), about **commit**, not scrolling.

On a scrollable set: `absolute(1)` ≡ `first()`, `absolute(-1)` ≡ `last()`, `absolute(0)` ≡ before first. `relative(1)` ≡ `next()`, `relative(-1)` ≡ `previous()`. An attempt to move past the ends leaves the cursor before first or after last. `isFirst` / `isLast` / `getRow` are **optional** on `TYPE_FORWARD_ONLY`. Fetch direction `FETCH_REVERSE` is illegal on `TYPE_FORWARD_ONLY`. After `next()` returns `false`, a further `next()` on a forward-only set is **vendor-specified** (`false` or `SQLException`).

`CONCUR_UPDATABLE`: `updateXxx` on the current row, then **`updateRow()`** to push to the database (`cancelRowUpdates` before that). Inserts use a staging **insert row**: `moveToInsertRow()`, updaters, **`insertRow()`**, `moveToCurrentRow()`. `deleteRow()` removes the current row from the set **and** the database. `refreshRow()` refetches (not on forward-only); if you call it after updaters but **before** `updateRow`, those updates are **lost**. Isolation level still applies ([[What transaction isolation levels does JDBC support]]).

```d2
direction: down
type: "Type: how the cursor moves\nFORWARD_ONLY | SCROLL_INSENSITIVE | SCROLL_SENSITIVE" {
  width: 420
  height: 70
  style.fill: "#e3f2fd"
}
conc: "Concurrency: may you write?\nREAD_ONLY | UPDATABLE" {
  width: 420
  height: 70
  style.fill: "#e8f5e9"
}

type -> conc: "requested together"
```

**Fig. 1.** Scrolling is type. Updates are concurrency. Ask for both on the `Statement`.

```java
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public final class ScrollUpdate {
    public static Statement open(Connection con) throws SQLException {
        return con.createStatement(
                ResultSet.TYPE_SCROLL_INSENSITIVE,
                ResultSet.CONCUR_UPDATABLE);
    }

    public static void renameFifth(ResultSet rs, String name) throws SQLException {
        if (!rs.absolute(5)) {
            return;
        }
        rs.updateString("NAME", name);
        rs.updateRow();
    }
}
```

**Listing 1.** Same fragment as the `ResultSet` javadoc: scroll to row 5, updater, `updateRow()`. Unsupported type/concurrency throws `SQLFeatureNotSupportedException` (or fails later). Check `supportsResultSetType` / `supportsResultSetConcurrency` ([[How do JDBC interface types such as Statement and PreparedStatement differ]]).

> [!warning] `TYPE_FORWARD_ONLY` cannot rewind
> `absolute` / `previous` throw. Default `createStatement()` is this type. You cannot “scroll” a default set.

> [!warning] Sensitive does not mean you always see concurrent writes
> `TYPE_SCROLL_SENSITIVE` is **generally** sensitive; `INSENSITIVE` is **generally** not. `refreshRow` and isolation still matter. Updaters without `updateRow()` never hit the table. `insertRow` requires the cursor on the insert row and values for non-nullable columns.

> [!tip] Interview answer
> Default ResultSets are forward-only and read-only. Type chooses scrolling: forward-only vs scroll-insensitive vs scroll-sensitive. Concurrency chooses read-only vs updatable. You pass both to `createStatement`. Scroll methods throw on forward-only; updaters throw on read-only. The driver may not support the pair you asked for.

## See also

- [[How does JDBC ResultSet behave and what configuration options exist]]
- [[How are database query results processed in JDBC]]
- [[What is JDBC ResultSet]]
