<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #Java/Exceptions/Unchecked #Java/IO #SRS

# How can you avoid being forced to handle checked `IOException`?

> [!abstract] Short answer
> **You cannot skip the compiler’s catch-or-specify rule.** Either **catch** `IOException`, **declare** `throws IOException` (callers are then forced), or **catch and wrap** it in an unchecked type such as `UncheckedIOException`. Wrapping is what stops *this* method — and its callers — from needing `throws IOException`.

## Catch, specify, or wrap

`IOException` is a checked exception. If a method body can throw it, the compiler requires a handler or a `throws` clause ([[What happens if you neither catch nor declare a checked exception]], [[What are common examples of checked exceptions in Java]], [[Does throws IOException cover FileNotFoundException]]).

**`throws IOException`** is not handling. It **pushes** the obligation to every caller. That avoids a `catch` here; it does not avoid checked handling in the program.

**Wrap.** Catch `IOException` and throw `new UncheckedIOException(e)` (or another `RuntimeException` with the `IOException` as cause). The wrap is unchecked, so this method needs no `throws IOException`, and callers are not forced either ([[Does wrapping a checked exception in RuntimeException require a throws clause]], [[When should a custom exception extend RuntimeException]], [[Can you create a custom exception that extends RuntimeException]]). `UncheckedIOException` exists for this: it wraps a non-null `IOException` and `getCause()` returns that `IOException`.

A lambda whose target type has no matching `throws` cannot let `IOException` out; wrap inside the lambda ([[Can a lambda throw a checked exception]]).

`catch (Exception e)` also satisfies the obligation, but it is still handling — and it catches `RuntimeException` too ([[Does catching Exception satisfy a checked exception obligation]]). Swallowing `IOException` with an empty `catch` compiles and is not recovery.

```d2
direction: down
io: "IOException (checked)" {
  width: 280
  height: 50
}
catch: "catch — you handled it" {
  width: 280
  height: 50
}
thrw: "throws IOException\ncallers still forced" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
wrap: "throw UncheckedIOException\nno throws IOException" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
io -> catch
io -> thrw
io -> wrap
```

**Fig. 1.** Only wrapping (or not calling I/O) removes the checked obligation from this method and its callers.

```java
class Demo {
    static void specify() throws java.io.IOException {
        java.nio.file.Files.readString(java.nio.file.Path.of("x"));
    }

    static void wrap() {
        try {
            java.nio.file.Files.readString(java.nio.file.Path.of("x"));
        } catch (java.io.IOException e) {
            throw new java.io.UncheckedIOException(e);
        }
    }
}
```

**Listing 1.** `specify` still forces callers. `wrap` does not: callers see an unchecked exception. The I/O failure is not gone; it changed type.

> [!warning] Wrapping does not make I/O safe
> The failure still happens. You traded a checked type for `RuntimeException`. Use wrap when this layer cannot recover — not to hide errors.

> [!warning] There is no “sneaky” official escape
> A method that can throw `IOException` must catch or declare it. Empty `catch`, `catch (Exception)`, and wrap all still execute a handler; only wrap changes what callers must declare.

> [!tip] Interview answer
> **Catch it, declare `throws IOException`, or wrap it in `UncheckedIOException`.** `throws` only moves the requirement up. Wrapping is how this method avoids a checked `IOException` in its signature; the I/O error is still there as an unchecked cause.
