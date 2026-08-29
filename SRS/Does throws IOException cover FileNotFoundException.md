<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# Does `throws IOException` cover `FileNotFoundException`?

> [!abstract] Short answer
> **Yes.** `FileNotFoundException` extends `IOException`. A method body may throw `FileNotFoundException` if `throws` names `IOException` (or a further supertype such as `Exception`). Callers then catch or declare `IOException`. The reverse is false: `throws FileNotFoundException` does **not** cover a thrown `IOException`.

## Subclass in the body, supertype in `throws`

A method or constructor must not be able to throw a checked class `E` unless `E` is a subclass of some class in `throws`. `FileNotFoundException` is a subclass of `IOException`, so `E` is covered. That is the same subtype rule as `catch (Exception)` covering `IOException` ([[Does catching Exception satisfy a checked exception obligation]], [[How would you explain the throws clause for checked exceptions]]).

A caller of `m()` that declares `throws IOException` must catch or declare `IOException`. They need not name `FileNotFoundException`. A `catch (IOException e)` also matches a thrown `FileNotFoundException`.

```d2
direction: down
io: "IOException" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
fnf: "FileNotFoundException" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
ok: "throws IOException\ncovers a thrown FNF" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
bad: "throws FileNotFoundException\ndoes not cover thrown IOException" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}
io -> fnf
io -> ok
fnf -> bad
```

**Fig. 1.** Coverage is one way: the `throws` type must be `E` or a **supertype** of `E`. See [[What happens if you neither catch nor declare a checked exception]].

```java
import java.io.FileNotFoundException;
import java.io.IOException;

class Demo {
    static void read() throws IOException {
        throw new FileNotFoundException("missing");
    }

    static void tooNarrow() throws FileNotFoundException {
        throw new IOException("io"); // compile-time error
    }
}
```

**Listing 1.** `read` is legal. `tooNarrow` is not: `IOException` is not a subclass of `FileNotFoundException`.

An override may **narrow** checked `throws` (parent `throws IOException`, child `throws FileNotFoundException`) but must not **widen** them (parent `throws FileNotFoundException`, child `throws IOException`) — [[What happens if an override declares a broader checked exception than the parent]].

> [!warning] Catch order is the opposite mnemonic
> If you catch both types, `FileNotFoundException` must appear **before** `IOException`. A preceding `catch (IOException)` already handles the subclass, so the child `catch` is unreachable ([[In what order should catch blocks appear for IOException and FileNotFoundException]]). `throws` wants the supertype; `catch` lists want the subtype first.

> [!warning] `throws IOException` is a wider caller contract
> Callers must be prepared for any `IOException`, not only “file not found.” If the method can only fail that way, declaring `throws FileNotFoundException` is the tighter API. Both are legal when the body only throws the subclass.

> [!tip] Interview answer
> **Yes — `FileNotFoundException` extends `IOException`, so `throws IOException` covers throwing it, and callers catch `IOException`. `throws FileNotFoundException` does not cover throwing a plain `IOException`. In `catch` lists, put the subclass first or the second catch will not compile.**
