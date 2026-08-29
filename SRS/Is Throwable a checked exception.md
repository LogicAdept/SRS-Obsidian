<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/Hierarchy #SRS

# Is `Throwable` a checked exception?

> [!abstract] Short answer
> **Yes.** The checked exception classes are `Throwable` and all of its subclasses **except** `RuntimeException` and `Error` (and those two families). `throws Throwable` is a checked declaration: callers must catch or declare it. The informal rule “`Exception` except `RuntimeException`” is incomplete — it leaves `Throwable` itself out.

## Checked means “not the unchecked families”

Every throwable is an instance of `Throwable`. The **unchecked** classes are only the run-time exception classes (`RuntimeException` and subclasses) and the error classes (`Error` and subclasses). Everything else on the `Throwable` tree is checked — including **`Throwable` itself** and `Exception` ([[What is the difference between checked and unchecked exceptions]], [[Are Error subclasses checked or unchecked]], [[Is RuntimeException a subclass of Exception]]).

That is why `throw new Throwable()` (or a method declared `throws Throwable`) forces the caller to catch or declare, just like `IOException` ([[How would you explain the throws clause for checked exceptions]], [[What happens if you neither catch nor declare a checked exception]]). You cannot throw a non-`Throwable` ([[Can you throw an object that is not a Throwable]]).

Typical *new* checked types still extend `Exception` rather than `Throwable` directly. `IOException` sits under `Exception`, not as a direct child of `Throwable` ([[Do checked exceptions inherit Throwable directly]]).

```d2
direction: down
t: "Throwable\n(checked class)" {
  width: 260
  height: 60
  style.fill: "#e8f5e9"
}
ex: "Exception\n(checked class)" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
err: "Error\n(unchecked)" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}
rte: "RuntimeException\n(unchecked)" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}
io: "IOException\n(checked)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
t -> ex
t -> err
ex -> rte
ex -> io
```

**Fig. 1.** `Throwable` is a checked class. Unchecked types are the `Error` and `RuntimeException` subtrees only.

```java
class Demo {
    static void declare() throws Throwable {
        throw new Throwable();
    }

    static void caller() throws Throwable {
        declare();
    }

    static void catchAll() {
        try {
            int n = 1;
        } catch (Throwable t) {
            System.out.println(t);
        }
    }
}
```

**Listing 1.** `declare` / `caller` need `throws Throwable` (or a `catch`) because `Throwable` is checked. `catch (Throwable t)` is legal even when the `try` body throws no checked type: `Throwable` is a superclass of `Exception`, and the clause also covers `Error` and `RuntimeException` ([[Can you catch Throwable]], [[Does catching Exception satisfy a checked exception obligation]]).

> [!warning] “Checked = `Exception` minus `RuntimeException`” omits `Throwable`
> That slogan matches everyday APIs (`IOException`) but is not the full definition. `Throwable` itself is checked. `Error` is unchecked even though it inherits `Throwable` ([[Why is Error a sibling of Exception rather than a subclass]]).

> [!warning] `catch (Throwable t)` is not a checked-only net
> It compiles on a `try` that throws nothing checked, and it also catches `Error`. That is why `catch (Exception e)` exists as the “recoverable” idiom: `Exception` is a sibling of `Error`, not a parent ([[Does catch Exception also catch Error]]).

> [!tip] Interview answer
> **Yes — checked classes are `Throwable` and its subclasses except `RuntimeException` and `Error`.** `throws Throwable` must be caught or declared. The shortcut “subclasses of `Exception` except runtime” forgets `Throwable` itself.
