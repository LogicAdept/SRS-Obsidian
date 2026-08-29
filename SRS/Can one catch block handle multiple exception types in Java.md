<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# Can one catch block handle multiple exception types in Java?

> [!abstract] Short answer
> **Yes, since Java SE 7:** `catch (IOException | SQLException e)`. One handler, several alternatives separated by `|`. The parameter is **implicitly `final`** — you cannot assign to it. Alternatives must not be parent and child of each other.

## Multi-catch is a union of alternatives

A uni-`catch` names one type. A multi-`catch` names a **union**: `catch (A | B e)`. The handler runs if the thrown object is an instance of any alternative. The parameter’s declared type is the **least upper bound** of those types (often a shared parent such as `Exception`).

Use it when the **same** body is correct for every alternative. That avoids duplicating the handler and reduces the urge to write a catch-all `catch (Exception e)` ([[Does catching Exception satisfy a checked exception obligation]], [[Does catch Exception also catch RuntimeException]]).

The multi-catch parameter is implicitly `final` if you do not write `final`. Assignment to `e` in the block is a compile-time error. That is **not** the same as uni-catch “effectively final”: the language treats the multi-catch parameter as final by declaration.

It is a compile-time error if one alternative is a **subtype** of another (`FileNotFoundException | IOException`). Use `catch (IOException e)` instead. That union error is not the same diagnostic as an unreachable **second** `catch` after a parent clause ([[Why can multi-catch exception types not share a parent-child relationship]], [[What is an unreachable catch block error]]).

Only **one** `catch` clause runs for a given throw, whether it is uni- or multi-catch ([[How many catch blocks execute for one thrown exception]]).

```d2
direction: down
tryb: "try { ... }" {
  width: 240
  height: 50
}
multi: "catch (IOException | SQLException e)" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}
one: "one handler body\ne implicitly final" {
  width: 300
  height: 70
}
tryb -> multi -> one
```

**Fig. 1.** One `catch` clause can list several types with `|`.

```java
class Demo {
    static void sameHandler(boolean io) {
        try {
            if (io) {
                throw new java.io.IOException();
            } else {
                throw new java.sql.SQLException();
            }
        } catch (java.io.IOException | java.sql.SQLException e) {
            System.err.println(e.getClass().getName());
            // e = null;  // compile-time error: implicitly final
        }
    }
}
```

**Listing 1.** Multi-catch since Java SE 7. `e` cannot be reassigned. `catch (FileNotFoundException | IOException e)` does not compile.

> [!warning] Implicitly `final`, not merely “effectively final”
> You cannot assign to a multi-catch parameter. Uni-catch parameters are not implicitly `final` unless you write `final` or never assign.

> [!warning] `|` is not a substitute for `catch (Exception e)`
> List only types that share the same recovery. Parent-and-child in one union is illegal. `catch (Exception e)` also takes `RuntimeException`; that is a single type, not multi-catch.

> [!tip] Interview answer
> **Yes — `catch (A | B e)` since Java 7.** One block, several types, parameter implicitly `final`. Do not put a parent and a child in the same `|` list. If the handling differs, use separate `catch` clauses (child first).
