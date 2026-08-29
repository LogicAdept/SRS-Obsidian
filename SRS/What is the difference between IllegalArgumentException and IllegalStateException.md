<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS

# What is the difference between `IllegalArgumentException` and `IllegalStateException`?

> [!abstract] Short answer
> **`IllegalArgumentException` means this call’s argument is illegal.** **`IllegalStateException` means the object (or environment) is not in a state where this operation is allowed — even if the arguments look fine.** Both are unchecked `RuntimeException`s, and they are **siblings**, not parent and child.

## Bad argument versus wrong time

`IllegalArgumentException` is thrown to indicate a method received an illegal or inappropriate argument (wrong value or range: `age < 0`). `NumberFormatException` is a subclass of it ([[What is NumberFormatException]], [[Should you throw NullPointerException or IllegalArgumentException for a null argument]]).

`IllegalStateException` signals that a method was invoked at an illegal or inappropriate **time**: the Java environment or the application is not in an appropriate state for the requested operation. `Iterator.remove()` before `next()` (or twice after one `next()`) is the collections example. A full bounded `Queue.add` is the same idea: the argument may be legal, the queue cannot accept it now.

Heuristic that matches those APIs: if a **different argument** could have made this call succeed, prefer `IllegalArgumentException`. If **no argument** would help because the object is in the wrong state, prefer `IllegalStateException`. Prefer these two built-ins over a custom type for those two cases ([[What is RuntimeException]], [[Why should you not use assert to validate public method arguments]]).

A forbidden `null` argument is still `NullPointerException` in JDK style, not IAE ([[What is NullPointerException]], [[What does Objects.requireNonNull do]]).

```d2
direction: down
rte: RuntimeException {
  width: 240
  height: 40
}
iae: IllegalArgumentException {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
ise: IllegalStateException {
  width: 260
  height: 40
  style.fill: "#ffebee"
}
nfe: NumberFormatException {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
rte -> iae
rte -> ise
iae -> nfe
```

**Fig. 1.** Both are unchecked; `IllegalStateException` does not extend `IllegalArgumentException`.

```java
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

class Demo {
    static void requireNonNegative(int age) {
        if (age < 0) {
            throw new IllegalArgumentException("age");
        }
    }

    static void removeWithoutNext() {
        Iterator<String> it = new ArrayList<>(List.of("a")).iterator();
        it.remove();
    }
}
```

**Listing 1.** `requireNonNegative(-1)` throws `IllegalArgumentException`. `removeWithoutNext` throws `IllegalStateException`. Neither method needs `throws` ([[Must you declare RuntimeException in a throws clause]], [[Can you catch an unchecked exception in Java]]).

> [!warning] `catch (IllegalArgumentException)` does not catch `IllegalStateException`
> They are siblings under `RuntimeException`. A handler written for “bad arguments” misses “wrong state.” `NumberFormatException` *is* an IAE.

> [!warning] `Iterator.remove()` is state, not an argument
> There is no bad index to pass. You called `remove` at the wrong time. That is `IllegalStateException`, not IAE.

> [!tip] Interview answer
> **`IllegalArgumentException` is a bad argument; `IllegalStateException` is a bad time for this object.** If another value could have worked, use IAE. If nothing you pass would help, use ISE. They are sibling unchecked exceptions — catching IAE does not catch ISE.
