<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/TryCatch #SRS

# What options exist for handling checked exceptions in Java?

> [!abstract] Short answer
> **Two language options: `catch` it, or declare `throws` (the type or a superclass).** There is no legal ignore. Wrapping in `RuntimeException` (or `UncheckedIOException`) is a third *API* choice: you catch, then throw unchecked, so callers are no longer forced.

## Catch, specify, or change the type

A checked exception that a method or constructor **can throw** must be handled in that body ([[What happens if you neither catch nor declare a checked exception]], [[If calling method A will throw an exception what should you do]]).

1. **`catch` and recover** — retry, fallback, message, close a resource. Prefer the actual type, not `Exception` ([[How would you catch an exception in your application]]).
2. **`throws`** — same type or a superclass. Callers then catch or specify; they need not catch at every level ([[Must every caller catch exceptions declared in a throws clause]], [[How would you explain the throws clause for checked exceptions]], [[How do you propagate an exception up the call stack in Java]]).
3. **Wrap** — `catch` the checked type, `throw new RuntimeException(e)` or `UncheckedIOException`. The wrapper is unchecked; the cause remains. Callers of *this* method no longer see the checked type ([[Does wrapping a checked exception in RuntimeException require a throws clause]], [[How can you avoid being forced to handle checked IOException]]).

A lambda is limited by the **function type**’s `throws`, not by the enclosing method ([[Can a lambda throw a checked exception]]). Try-with-resources still exposes checked exceptions from `close()` unless you catch them.

```d2
direction: down
chk: "checked E can leave the body" {
  width: 300
  height: 50
}
opt: "options" {
  width: 240
  height: 50
}
c: "catch E" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
t: "throws E" {
  width: 240
  height: 50
}
w: "catch and wrap unchecked" {
  width: 280
  height: 50
}
chk -> opt
opt -> c
opt -> t
opt -> w
```

**Fig. 1.** The compiler’s menu is catch or `throws`. Wrapping is catch plus a new throw.

```java
class Demo {
    static String recover() {
        try {
            return java.nio.file.Files.readString(java.nio.file.Path.of("x"));
        } catch (java.io.IOException e) {
            return "";
        }
    }

    static String specify() throws java.io.IOException {
        return java.nio.file.Files.readString(java.nio.file.Path.of("x"));
    }
}
```

**Listing 1.** `recover` handles. `specify` declares. A third method with neither does not compile.

> [!warning] Empty `catch` is not an option the language wanted
> It compiles. It also hides the failure. Catch-or-specify expected a policy.

> [!warning] `throws Exception` is a blunt specify
> It is legal and it pushes `Exception` (including `RuntimeException` if callers catch that wide) onto every client.

> [!tip] Interview answer
> **For a checked exception you catch it if you can recover, or you declare `throws`.** You cannot skip both. Wrapping in an unchecked type is allowed after you catch, and it changes what *callers* must handle.
