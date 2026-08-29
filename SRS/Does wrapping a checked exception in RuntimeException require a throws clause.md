<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Checked #SRS

# Does wrapping a checked exception in `RuntimeException` require a `throws` clause?

> [!abstract] Short answer
> **No.** Compile-time checking looks at the type you **throw**, not at `getCause()`. `throw new RuntimeException(checked)` throws an unchecked type, so the method need not declare `throws`. The original checked exception is only the cause.

## The thrown type is the wrapper

`RuntimeException` and its subclasses are unchecked: they need not appear in `throws` even if they propagate out of the method ([[Must you declare RuntimeException in a throws clause]], [[What is RuntimeException]]). A `throw` of `new RuntimeException(...)` therefore does not create a checked-exception obligation ([[How would you explain the throws clause for checked exceptions]]).

Wrapping is the documented way to keep a lower-layer checked failure (for example `IOException`) without declaring it: store it as the cause on an unchecked wrapper. Callers catch `RuntimeException` (or `Exception`), not the nested type.

```d2
direction: down
body: "catch IOException" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
wrap: "throw new RuntimeException(ex)" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
out: "method needs no throws" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
miss: "catch (IOException) at the caller\ndoes not match the wrapper" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
body -> wrap
wrap -> out
wrap -> miss
```

**Fig. 1.** The compiler tracks the wrapper. The checked object rides along as cause only.

```java
import java.io.IOException;

class Demo {
    static void wrap() {
        try {
            throw new IOException("disk");
        } catch (IOException ex) {
            throw new RuntimeException("I/O failed", ex);
        }
    }

    static void stillChecked() {
        throw new IOException("disk"); // compile-time error
    }
}
```

**Listing 1.** `wrap` compiles with no `throws`. `stillChecked` does not: the thrown type is still checked ([[What happens if you neither catch nor declare a checked exception]]).

`RuntimeException(Throwable cause)` is the wrapper constructor; `getCause()` returns the original throwable.

> [!warning] Callers catching the checked type miss the wrapper
> `catch (IOException e)` does **not** match `RuntimeException`. The nested `IOException` is visible only after unwrapping `getCause()` (and checking its type). A caller that only handles the checked type will not see the failure as that type.

> [!warning] Wrapping is not the same as throwing the checked object
> If the `throw` expression has a checked type, you still catch or declare it. Putting a checked exception in a cause chain does not change that. Unchecked casts that rethrow a checked exception as if it were unchecked are a different, unsafe trick — not this constructor pattern.

> [!tip] Interview answer
> **No — the compiler checks the thrown type, not the cause. `throw new RuntimeException(ex)` is unchecked, so no `throws` is required. Callers catch the wrapper; they see the original checked exception only through `getCause()`.**
