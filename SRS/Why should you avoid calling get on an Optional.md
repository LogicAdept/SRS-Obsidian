<!--
reps: 0
priority: 0
-->
#Java/Language/Optional #Java/Exceptions/Unchecked #SRS

# Why should you avoid calling `get` on an `Optional`?

> [!abstract] Short answer
> **`get()` throws `NoSuchElementException` when the `Optional` is empty.** Using it without a present-check only swaps a possible NPE for another unchecked exception. Prefer `orElse`, `orElseGet`, `orElseThrow`, `map`, or `ifPresent`. If absence must fail, prefer **`orElseThrow()`** over `get()`.

## Empty is not `null`, and `get()` is not a default unwrap

`Optional.get()` returns the value if one is present; otherwise it throws `NoSuchElementException` — **not** `NullPointerException` ([[What is NoSuchElementException]], [[What is NullPointerException]], [[How do you prevent a NullPointerException]]).

`Optional` exists so absence is explicit. Blind `find(id).get()` treats “no user” as a crash, the same family of mistake as dereferencing `null`. `isPresent()` then `get()` is still that crash, with extra lines.

The API’s preferred alternative to `get()` is **`orElseThrow()`** (same `NoSuchElementException` if empty, clearer “I mean to fail”). A supplier overload throws a type you choose ([[What does orElseThrow do on Optional]]). `orElse(default)` / `orElseGet(...)` supply a substitute. `ifPresent` / `map` keep the empty case in the pipeline ([[How would you explain java.util.Optional]], [[Why should a method that returns Optional never return null]], [[What are Optional.ofNullable and Optional.empty]]).

`get()` is unchecked: no `throws`. You may catch `NoSuchElementException`; that does not make `get()` a good unwrap ([[Can you catch an unchecked exception in Java]]).

```d2
direction: down
empty: "Optional.empty().get()" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
nsee: NoSuchElementException {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
throw: "orElseThrow()" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
else: "orElse / orElseGet / ifPresent" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
empty -> nsee
throw -> nsee
```

**Fig. 1.** Empty `get()` and no-arg `orElseThrow()` both throw `NoSuchElementException`. The latter names the intent.

```java
import java.util.Optional;

class Demo {
    static String blindGet(Optional<String> u) {
        return u.get();
    }

    static String failLoud(Optional<String> u) {
        return u.orElseThrow();
    }

    static String defaulted(Optional<String> u) {
        return u.orElse("anonymous");
    }
}
```

**Listing 1.** `blindGet` and `failLoud` both throw `NoSuchElementException` on empty. Prefer `failLoud` when absence is a defect. `defaulted` does not throw. None of these needs `throws`.

> [!warning] Empty `get()` is not NPE
> Interview traps mix “optional was null” with empty. `Optional` itself should not be `null`. Empty `get()` is `NoSuchElementException`.

> [!warning] `isPresent()` then `get()` is still `get()`
> The check documents intent; a race of logic (or a missed branch) still throws. `orElseThrow` / `orElse` make the empty path obvious.

> [!tip] Interview answer
> **Avoid `Optional.get()` because an empty box throws `NoSuchElementException`, not a handled absence.** That is the same class of bug as an NPE, with a different type. Use `orElse`, `orElseGet`, `ifPresent`, or `orElseThrow()` if you mean to fail.
