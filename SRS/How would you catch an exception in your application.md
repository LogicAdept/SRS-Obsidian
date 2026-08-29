<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# How would you catch an exception in your application?

> [!abstract] Short answer
> **Put a `try` around the call and a `catch` whose type is that exception or a superclass.** The **first** matching clause runs. Catch the **specific** types you can recover from. `catch (Exception e)` also takes `RuntimeException` and misses `Error`. `catch (Throwable t)` takes `Error` too.

## A `catch` is a type test on the thrown object

After `try { … }`, each `catch (Type e)` is tried left to right. The clause runs if the thrown object is an instance of `Type` (or of a subclass). Only **one** clause executes for a given throw ([[How many catch blocks execute for one thrown exception]], [[How do you handle exceptions in Java applications]], [[How should you throw and handle exceptions in Java]]).

Put the **more specific** type first. `catch (IOException e)` then `catch (FileNotFoundException e)` is unreachable. `catch (FileNotFoundException e)` then `catch (IOException e)` is the legal order ([[What is an unreachable catch block error]]).

Several types that share one body: `catch (IOException | SQLException e)` ([[Can one catch block handle multiple exception types in Java]]).

You **may** catch unchecked exceptions the same way; they just do not require `catch` or `throws` ([[Can you catch an unchecked exception in Java]], [[Does catch Exception also catch RuntimeException]]).

`catch (Exception e)` does **not** catch `Error`. `catch (Throwable t)` does ([[Does catch Exception also catch Error]], [[Can you catch Throwable]]). Prefer not to catch `Error` as recovery.

A `try` with only `finally` does **not** catch anything; the exception still leaves after cleanup ([[Can you try-finally without catch]]). Try-with-resources may add `catch` after the resource list.

```d2
direction: down
tryb: "try { work }" {
  width: 240
  height: 50
}
spec: "catch (SpecificEx e)" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
broad: "catch (Exception e)" {
  width: 280
  height: 50
  style.fill: "#fff8e1"
}
miss: "Error still uncaught" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
tryb -> spec
tryb -> broad
broad -> miss
```

**Fig. 1.** First matching `catch` wins. `Exception` is not the whole `Throwable` tree.

```java
class Demo {
    static int parse(String s) {
        try {
            return Integer.parseInt(s);
        } catch (NumberFormatException e) {
            return 0;
        }
    }
}
```

**Listing 1.** Catch the type you can handle. `catch (Exception e)` here would also hide bugs that throw `RuntimeException` for other reasons.

> [!warning] Order is a compile-time rule
> Parent then child is an unreachable catch. Multi-catch forbids parent and child in the same `|` list.

> [!warning] Catch-all is not “how you catch in an application”
> `catch (Exception)` / `catch (Throwable)` compiles and often fails the interview. Catch what you can fix; let the rest propagate or wrap with a cause.

> [!tip] Interview answer
> **Wrap the call in `try` and `catch` the specific exception type — first matching block wins, more specific types first.** You can multi-catch with `|`. Do not default to `catch (Exception)` or `Throwable`; those also take runtime failures, and `Throwable` takes `Error`.
