<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Hierarchy #Java/Exceptions/Unchecked #SRS

# Does `catch (Exception)` also catch `RuntimeException`?

> [!abstract] Short answer
> **Yes.** `RuntimeException` is a direct subclass of `Exception`. `catch (Exception e)` matches every `Exception` subtype: checked types such as `IOException` **and** unchecked types such as `NullPointerException`. It still does **not** match `Error`.

## `RuntimeException` sits on the `Exception` branch

A `catch` handles a thrown object when the object's class is the catch type or a subclass of it. `RuntimeException` extends `Exception`, so it is assignment-compatible with `Exception`. `Error` does not; that is a sibling under `Throwable` ([[Does catch Exception also catch Error]], [[Is RuntimeException a subclass of Exception]]).

`catch (Exception)` is therefore **not** reserved for checked exceptions. Unchecked run-time exceptions are still `Exception`s; they are only exempt from required `throws` / `catch` ([[Can you catch an unchecked exception in Java]]).

```d2
direction: down
throwable: "Throwable" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
exc: "Exception\ncatch (Exception) starts here" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
err: "Error\nnot caught" {
  width: 220
  height: 60
  style.fill: "#ffebee"
}
rte: "RuntimeException\ncaught (unchecked)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
io: "IOException\ncaught (checked)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
npe: "NullPointerException" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
throwable -> exc
throwable -> err
exc -> rte
exc -> io
rte -> npe
```

**Fig. 1.** One `catch (Exception)` covers both the checked `Exception` subtypes and the entire `RuntimeException` tree.

```java
class Demo {
    static int parse(String s) {
        try {
            return Integer.parseInt(s);
        } catch (Exception e) {
            return 0; // NumberFormatException is a RuntimeException
        }
    }

    static void copy() {
        try {
            riskyIo();
        } catch (Exception e) {
            // IOException — and also NPE if riskyIo NPEs
        }
    }

    static void riskyIo() throws java.io.IOException {}
}
```

**Listing 1.** `catch (Exception)` is a single net for checked I/O failures and unexpected run-time exceptions. Prefer `catch (IOException)` or `catch (NumberFormatException)` when that is what you mean to handle. A broad `catch (Exception)` can still satisfy a checked `throws` obligation for types under `Exception` — [[Does catching Exception satisfy a checked exception obligation]] — while also catching NPE.

> [!warning] A handler meant for I/O can swallow an NPE
> `try { readFile(); } catch (Exception e) { log(e); }` will log a `NullPointerException` from a bug in `readFile` the same way it logs `IOException`. The program then continues as if I/O failed. Catch the most specific type you intend to recover from.

> [!warning] `catch (RuntimeException)` is the narrower unchecked net
> If you want only the run-time branch, catch `RuntimeException` (or a more specific subtype). That still misses checked `IOException` **and** still misses `Error`. `catch (Exception)` is the blunt tool that folds checked and run-time together.

> [!tip] Interview answer
> **Yes — `RuntimeException` extends `Exception`, so `catch (Exception e)` catches NPE and friends as well as `IOException`. That is why a wide `Exception` handler is blunt: it is not “checked only.” It still does not catch `Error`; that takes `Throwable` or `Error`.**
