<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Exceptions/Checked #SRS

# Must you declare `RuntimeException` in a `throws` clause?

> [!abstract] Short answer
> **No.** `RuntimeException` and its subclasses are unchecked: they need not appear in `throws` and need not be caught. You *may* write `throws RuntimeException` (or `throws NullPointerException`); the compiler does not require it. A checked type such as `IOException` must still be caught or declared.

## Unchecked types are exempt from `throws`

`RuntimeException` extends `Exception` but is an unchecked exception class. Unchecked exceptions do not have to be declared in a method or constructor `throws` clause even if they propagate out of the body ([[What is RuntimeException]], [[Is RuntimeException a subclass of Exception]], [[What is the difference between checked and unchecked exceptions]]).

`Error` is the other unchecked family; it is likewise optional in `throws` ([[Are Error subclasses checked or unchecked]]). Wrapping a checked exception in `new RuntimeException(cause)` also needs no `throws` for the wrapper ([[Does wrapping a checked exception in RuntimeException require a throws clause]]).

You can still list unchecked types in `throws`. That is documentation for callers; it does not change whether the exception can be thrown, and it does not replace a missing checked type ([[How would you explain the throws clause for checked exceptions]], [[Must every caller catch exceptions declared in a throws clause]]).

```d2
direction: down
rte: "throw new RuntimeException()" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
opt: "throws optional" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
io: "throw new IOException()" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
req: "catch or throws required" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
rte -> opt
io -> req
```

**Fig. 1.** Unchecked `throws` is optional. Checked `throws` is not.

```java
import java.io.IOException;

class Demo {
    static void unchecked() {
        throw new RuntimeException("x");
    }

    static void listed() throws NullPointerException {
        throw new NullPointerException();
    }

    static void stillChecked() throws RuntimeException {
        throw new IOException("io"); // compile-time error
    }
}
```

**Listing 1.** `unchecked` and `listed` compile. `stillChecked` does not: `throws RuntimeException` does not cover `IOException` ([[What happens if you neither catch nor declare a checked exception]]). You may catch an unchecked exception if you want to ([[Can you catch an unchecked exception in Java]]). An override must not add a **checked** `throws` the parent lacks ([[Can you override a RuntimeException throws clause with a checked exception]]).

> [!warning] `throws NullPointerException` does not prevent an NPE
> The clause names a type the method is allowed to propagate. It is not a filter and not a promise that the body will not throw. The NPE still happens at run time.

> [!warning] Unchecked `throws` does not discharge a checked obligation
> A method that can throw `IOException` still needs `throws IOException` (or a checked supertype) or a `catch`. Listing only `RuntimeException` leaves that hole.

> [!tip] Interview answer
> **No — you do not have to declare `RuntimeException` (or NPE, IAE, …) in `throws`.** You may list them anyway. Checked exceptions such as `IOException` still must be caught or declared; an unchecked `throws` does not cover them.
