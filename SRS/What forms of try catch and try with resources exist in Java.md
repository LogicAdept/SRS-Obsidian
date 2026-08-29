<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #Java/IO #SRS

# What forms of try catch and try with resources exist in Java?

> [!abstract] Short answer
> **A `try` statement is `try` + (`catch`s and/or `finally`), or a try-with-resources that may add `catch`/`finally`.** Legal shapes: `try-catch`, `try-finally`, `try-catch-finally`, multi-`catch`, basic TWR, and extended TWR. A bare `try { }` with no `catch`, `finally`, or resource list is illegal.

## Four non-resource forms, then TWR

A non-resource `try` must be followed by at least one `catch`, a `finally`, or both. You may have several `catch` clauses and **at most one** `finally`. Nothing may sit between those parts ([[How would you explain try-catch-finally]], [[Can you try-finally without catch]], [[Can a try statement have more than one finally block]], [[Can you place statements between try catch and finally]]).

**Multi-`catch`** is still one clause: `catch (A | B e)`. The parameter is implicitly `final`. Alternatives cannot be subclasses of each other ([[Can one catch block handle multiple exception types in Java]]).

**Try-with-resources** is `try (` resources `)` plus a block. Resources are `AutoCloseable`. A **basic** TWR has no `catch` or `finally` of yours; that is the one legal `try` without those clauses ([[Can a try block exist without catch and finally]], [[Can a try block exist without a catch in Java]], [[What is try-with-resources]]). An **extended** TWR may still have `catch` and/or `finally`; those run **after** automatic close.

Resources may be declared in the header, or (since Java 9) an existing `final` / effectively final variable.

```d2
direction: down
try: "try" {
  width: 220
  height: 50
}
plain: "catch and/or finally" {
  width: 300
  height: 50
}
twr: "(resources) then optional\ncatch / finally" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
try -> plain
try -> twr
```

**Fig. 1.** Two families: ordinary `try`, and `try` with a resource specification.

```java
class Demo {
    static void forms() throws java.io.IOException {
        try {
            throw new java.io.IOException("a");
        } catch (java.io.FileNotFoundException e) {
            System.out.println("fnf");
        } catch (java.io.IOException e) {
            System.out.println("io");
        } finally {
            System.out.println("done");
        }

        try (java.io.StringReader r = new java.io.StringReader("x")) {
            r.read();
        }
    }
}
```

**Listing 1.** `try-catch-finally` with two `catch`es, then a basic try-with-resources (no `catch`/`finally`).

> [!warning] `try { }` alone does not compile
> Empty parentheses `try ()` is not a resource list either. You need a real resource, or `catch`/`finally`.

> [!warning] Extended TWR is not a second `finally` for `close`
> Your `finally` runs after automatic close. A throw from that `finally` still replaces the pending result, unlike a failing `close` that is suppressed on a body exception.

> [!tip] Interview answer
> **Ordinary `try` comes in catch, finally, or both — including several `catch`es and multi-`catch`.** Try-with-resources adds a resource list and may omit `catch`/`finally`, or keep them as the extended form. You cannot write a `try` with no handler, no `finally`, and no resources.
