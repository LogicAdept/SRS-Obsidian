<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Career/Interview #SRS

# What is your view on checked exceptions in Java?

> [!abstract] Short answer
> **They are a compile-time contract: if the caller can reasonably recover, the compiler should force `catch` or `throws`.** That is a good fit for I/O, JDBC, and interruption. It is a bad fit for programmer bugs and VM failure. Extending `RuntimeException` only to skip `throws` is not a design.

## A contract, not a fashion

Checked types exist so handlers are not silently missing. The names in `throws` are part of the method contract ([[What is the difference between checked and unchecked exceptions]], [[How would you explain the throws clause for checked exceptions]], [[What are examples where checked exceptions are a good fit]]). `RuntimeException` and `Error` are exempt because declaring them would not prove much, and `Error` would clutter APIs.

The useful view in an interview:

- **Keep checked** when this layer’s caller has a real response (retry, fallback, restore interrupt).
- **Use unchecked** for impossible arguments, broken invariants, and `Error` — not because “modern code skips `throws`.”
- **Wrap** at a boundary when the outer API should not mention `IOException`, and keep the cause. That is layering, not a license to empty-`catch` ([[How can you avoid being forced to handle checked IOException]], [[When should a custom exception extend RuntimeException]], [[Can you create a custom exception that extends RuntimeException]]).

The common criticisms — noisy `throws`, interfaces that cannot add a checked type, lambdas whose function type has no `throws` — are real. They do not erase recoverability as the criterion ([[How would you explain criticisms of checked exceptions in Java]]).

```d2
direction: down
fail: "failure at this API" {
  width: 280
  height: 50
}
rec: "caller can recover?" {
  width: 280
  height: 50
}
chk: "checked + throws" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
uc: "unchecked" {
  width: 260
  height: 50
}
fail -> rec
rec -> chk: "yes"
rec -> uc: "no"
```

**Fig. 1.** The view to defend: recoverability first, not “checked is obsolete.”

```java
class Demo {
    static String load(java.nio.file.Path path) throws java.io.IOException {
        return java.nio.file.Files.readString(path);
    }
}
```

**Listing 1.** A file read is a recoverable I/O outcome. Forcing callers to notice `IOException` is the point of checked exceptions, not a defect.

> [!warning] “We wrap everything” is not a view of the language
> Wrapping deletes the catch-or-specify signal. Do it at a true boundary, with the checked type as `getCause()`, not in every method to keep signatures pretty.

> [!warning] This cue is not a SQL `VIEW`
> Interview “view” means your judgment of checked exceptions, not a database view.

> [!tip] Interview answer
> **Checked exceptions are the compiler enforcing a recovery decision.** I keep them for I/O and similar expected failures, and I use `RuntimeException` for bugs. I do not drop `throws` just to make lambdas easier. Wrapping belongs at a module edge, with the original type as the cause.
