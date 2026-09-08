<!--
reps: 0
priority: 0
-->
#Java/Exceptions/TryCatch #SRS

# How do you order catch blocks for `FileNotFoundException` and `IOException`?

> [!abstract] Short answer
> **Subclass first, superclass after**: `FileNotFoundException` **extends** `IOException` (java.io, Java SE 21), so `catch (FileNotFoundException e)` must precede `catch (IOException e)`. The reverse order makes the subclass block **unreachable** — JLS §14.20 requires that there be "no earlier catch block A ... such that the type of C's parameter is the same as, or a subclass of, the type of A's parameter" — so it is a **compile-time error**, not a silent bug. Exactly **one** `catch` block ever runs: the **first** whose parameter matches the thrown exception. If both types need identical handling, the correct tool is a single `catch (IOException e)` — a multi-catch listing both is also a compile-time error because "a union of types" may not contain a subtype of another alternative (JLS §14.20). Single-catch mechanics live in [[Can one catch block handle multiple exception types in Java]].

## Why the compiler enforces the order

`catch` clauses are tested **top-down** at runtime: when an exception propagates out of the `try` block, the JVM selects the first clause whose parameter is a supertype of the thrown class, runs its block, and skips the rest. Without the reachability rule, `catch (IOException e)` placed first would match every `FileNotFoundException` too, and the `FileNotFoundException` block below it could **never** execute — dead code that can only be a mistake. The JLS freezes this intuition into a static rule, and the JLS §11.2.3 discussion shows the same failure mode for multi-catch: "the second catch clause below would cause a compile-time error because exception analysis determines that `SubclassOfFoo` is already caught by the first catch clause: `catch (Foo f) {...} catch (Bar | SubclassOfFoo e) {...}`."

```java
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Path;

class ConfigLoader {
    String readName(Path path) {
        try (var in = new java.io.FileInputStream(path.toFile())) { // throws FNFE
            return new String(in.readAllBytes()).lines().findFirst().orElse("");
        } catch (FileNotFoundException e) {          // most specific FIRST
            return "missing: " + path;               // e.g. create default file
        } catch (IOException e) {                    // superclass LAST
            throw new java.io.UncheckedIOException(e); // read errors, encoding, ...
        }
    }

    void bothSame(Path path) {
        try (var in = new java.io.FileInputStream(path.toFile())) {
            in.readAllBytes();
        } catch (IOException e) {
            // identical handling for BOTH: just catch the common supertype.
            // catch (FileNotFoundException | IOException e) would NOT compile:
            // a union of types may not contain a subtype of another alternative.
        }
    }
}
```

**Listing 1.** Specific-then-general ordering with distinct handlers; and the legal way to share handling — catch the supertype alone, because a subtype-plus-superclass multi-catch is rejected by the compiler.

```d2
direction: right
thrown: "IOException thrown" {style.fill: "#fff3e0"}
c1: "catch (FileNotFoundException)" {
  style.fill: "#e8f5e9"
}
c2: "catch (IOException)" {style.fill: "#e8f5e9"}
fnfe: "is FNFE? -> run this block,\nskip the rest" {style.fill: "#e3f2fd"}
ioe: "other IOException ->\nrun this block" {style.fill: "#e3f2fd"}
bad: "reversed order:\nblock unreachable ->\ncompile error" {style.fill: "#b71c1c"}
thrown -> c1
c1 -> fnfe
c1 -> c2
c2 -> ioe
c2 -> bad
```

**Fig. 1.** Top-down matching: the first compatible parameter wins and the remaining blocks are skipped — which is exactly why unreachable ones are rejected at compile time.

## How this scales beyond two types

The rule is total order by specificity: with `catch (FileNotFoundException)`, then `catch (IOException)`, then `catch (Exception)`, each level catches only what slipped through the narrower ones. Two practical corollaries keep real code honest. First, a broad **`catch (Exception e)` placed first is legal but poisons everything after it**: any subsequent block for a checked subclass of `Exception` becomes unreachable and fails compilation — so broad clauses belong **last**, if at all. Second, multi-catch (`catch (A | B e)`) is for **sibling** types with identical handling; the parameter's declared type is then the union's *least upper bound*, so the body must be written against the common supertype's API. The declaration side of the same contract — which types may even appear in `catch` or `throws` — is in [[What does the throws keyword mean]], and the `try`/`catch`/`finally` frame around it in [[Can a try block exist without a catch in Java]].

> [!warning] "It compiles if I catch `Exception` first" — it does not
> A common claim in interviews: *catch `Exception` first and you lose nothing*. In fact `catch (Exception e) { }` followed by `catch (IOException e) { }` is a **compile-time error** ("exception IOException has already been caught") because the second block is unreachable by JLS §14.20. The reverse mistake is equally fatal in review: putting `IOException` before `FileNotFoundException` compiles into a block that can never run — the compiler stops you only because the types are statically related; with *unrelated* types and a bug in your matching logic, no such help arrives.

> [!tip] Interview answer
> **FileNotFoundException extends IOException, so the subclass goes first — catch blocks are matched top-down and the first compatible one runs, exactly one. Reversed order makes the subclass block unreachable, which is a compile-time error under JLS 14.20's reachability rule, not a runtime surprise. If both types need the same handling, catch the supertype alone: a multi-catch listing both is also rejected, since a union of types can't contain a subtype of another alternative. Broad Exception clauses always go last — or better, never.**
