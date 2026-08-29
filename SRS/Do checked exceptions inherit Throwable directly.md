<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Checked #SRS

# Do checked exceptions inherit `Throwable` directly?

> [!abstract] Short answer
> **No — not as a group, and not as the definition of “checked.”** The only *direct* subclasses of `Throwable` are `Exception` and `Error`. `Exception` is checked; `Error` is not. Usual checked types such as `IOException` and `SQLException` extend `Exception`, so they inherit `Throwable` **through** `Exception`. Checked versus unchecked is which **subtrees** you exclude, not how many hops from `Throwable`.

## Direct children versus the checked set

`Throwable` is a class, a direct subclass of `Object`. Its two direct subclasses are `Exception` and `Error`. `RuntimeException` is a direct subclass of `Exception`, not of `Throwable`. See [[What sits at the root of every Java exception]] and [[Is RuntimeException a subclass of Exception]].

The checked classes are `Throwable` and every subclass **except** the run-time exception classes (`RuntimeException` and its subclasses) and the error classes (`Error` and its subclasses). Hop count is irrelevant: `IOException` is as checked as `Exception`. `NullPointerException` is unchecked even though it is several levels below `Throwable`.

```d2
direction: down
throwable: "Throwable\n(checked as a class)" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
error: "Error\nunchecked" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
exc: "Exception\nchecked" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
rte: "RuntimeException\nunchecked" {
  width: 260
  height: 60
  style.fill: "#ffebee"
}
io: "IOException, SQLException\nchecked (not direct)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
throwable -> error
throwable -> exc
exc -> rte
exc -> io
```

**Fig. 1.** Direct inheritance from `Throwable` is only `Exception` and `Error`. Typical checked API types sit under `Exception`. [[Why is Error a sibling of Exception rather than a subclass]], [[Are Error subclasses checked or unchecked]].

`Exception` **does** extend `Throwable` directly, and it is checked. The platform API states that `Exception` and its subclasses that are not also `RuntimeException` subclasses are checked. That describes the `Exception` branch; the language rule also treats `Throwable` itself as checked ([[Is Throwable a checked exception]], [[What is the difference between Throwable and Exception]]).

```java
class Demo {
    static void io() throws java.io.IOException {
        throw new java.io.IOException("disk");
    }

    static void sql() throws java.sql.SQLException {
        throw new java.sql.SQLException("db");
    }
}
```

**Listing 1.** `IOException` and `SQLException` extend `Exception`. They require `throws` or `catch` because they are checked, not because they are direct children of `Throwable`.

> [!warning] “Checked = direct children of Throwable except RuntimeException and Error”
> That sentence is a popular mix-up. `RuntimeException` is **not** a direct child of `Throwable`. `IOException` is **not** a direct child of `Throwable`. The real cut is: exclude the `RuntimeException` tree and the `Error` tree; everything else under `Throwable` is checked.

> [!warning] A custom `extends Throwable` is still checked
> `class Weird extends Throwable {}` *does* inherit `Throwable` directly and is checked (`catch (Exception)` misses it). That is legal and unusual; convention is to extend `Exception` or `RuntimeException` ([[Can you throw an object that is not a Throwable]]). Do not treat “direct subclass of Throwable” as a synonym for “checked.”

> [!tip] Interview answer
> **No. Checked exceptions are not “the types that extend Throwable directly.” `Exception` and `Error` are the direct subclasses of `Throwable`; `IOException` and `SQLException` extend `Exception`. Checked means every `Throwable` except the `RuntimeException` and `Error` trees — depth in the tree does not matter.**
