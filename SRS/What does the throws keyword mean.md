<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS

# What does the `throws` keyword mean?

> [!abstract] Short answer
> **`throws`** in a method or constructor signature **declares** the checked exceptions that the code may **propagate** instead of catching — it is part of the method's **contract**. Per JLS §11.2, the compiler performs **compile-time checking**: every caller must either **`catch`** those exceptions or declare them onward in its own `throws` clause. Only **checked** exceptions force this; "the unchecked exception classes are the run-time exception classes and the error classes" (JLS §11.1.1), and they never require declaration. On **overriding**, JLS §8.4.8.3 is strict: an override "may not be declared to throw **more checked exceptions** than the overridden ... method" — it may declare fewer or narrower ones. Declaring is not throwing: the keyword that actually raises an exception is `throw`, covered in [[Which keyword throws an exception in Java]].

## What the clause does and does not promise

A `throws` list is a **permission statement**, not a prediction. The method *may* throw each listed type or any **subclass** of it; it may also run to completion without throwing anything. Three consequences follow from the specification:

* **Checked-only enforcement.** The checked set is "all exception classes other than the unchecked exception classes" (JLS §11.1.1) — everything under `Throwable` except `RuntimeException` and `Error` subtrees. Listing unchecked types is legal but meaningless noise; callers owe them no handling.
* **Caller obligations.** The JLS §11.2 example rule cuts both ways: a catch clause is a compile-time error if it claims a checked exception the `try` block cannot actually throw, and a call is a compile-time error if the callee's checked exception is neither caught nor redeclared. `throws` is how checked exceptions travel up the call chain without `try` blocks at every level.
* **Overriding narrows, never widens.** JLS §8.4.8.3: an override "may not be declared to throw more checked exceptions than the overridden or hidden method". The override may declare a **subclass** of the declared type or drop entries entirely — that is why code holding a *supertype* reference can trust only the supertype's declaration. The related trap of *adding* checked exceptions to an override lives in [[Can you override a RuntimeException throws clause with a checked exception]].

```java
import java.io.FileNotFoundException;
import java.io.IOException;

class Parser {
    // Declares two checked types; callers must catch or declare.
    java.util.List<String> read(String path) throws IOException, java.text.ParseException {
        if (!path.endsWith(".txt")) {
            throw new java.text.ParseException("unsupported format", 0);
        }
        return java.nio.file.Files.readAllLines(java.nio.file.Path.of(path));
    }
}

class CsvParser extends Parser {
    @Override
    java.util.List<String> read(String path) throws FileNotFoundException { // narrowed: OK
        try {
            return super.read(path); // super declares IOException + ParseException
        } catch (java.text.ParseException e) {
            throw new IllegalStateException("bad format", e);
        } catch (IOException e) {   // body must not leak broader checked types
            if (e instanceof FileNotFoundException fnfe) throw fnfe;
            throw new java.io.UncheckedIOException(e);
        }
    }
}

// class BadParser extends Parser {
//     @Override
//     java.util.List<String> read(String path) throws Exception { } // compile error:
//     // "read(String) in BadParser cannot override read(String) in Parser;
//     //  overridden method does not throw java.lang.Exception"
// }
```

**Listing 1.** Declaration defines the contract; an override may narrow it (`FileNotFoundException` is a subclass of `IOException`) but widening to `Exception` fails to compile.

```d2
direction: right
call: "caller invokes read(path)" {style.fill: "#e3f2fd"}
decl: "read throws IOException" {style.fill: "#fff3e0"}
choice: "compiler checks caller" {style.fill: "#f0f0f0"}
catch: "catch (IOException)" {style.fill: "#e8f5e9"}
prop: "declare throws IOException\nin caller's signature" {style.fill: "#fff8e1"}
uncheck: "RuntimeException / Error:\nno declaration required" {style.fill: "#ffebee"}
call -> decl -> choice
choice -> catch
choice -> prop
choice -> uncheck
```

**Fig. 1.** The checked-exception contract: the compiler gives the caller two lawful exits — handle or redeclare — and stays out of unchecked types entirely.

## Why the distinction exists

Checked exceptions encode **recoverable, foreseeable failures** — missing files, dropped connections, bad user data — into the type system, so the API author forces the caller to acknowledge them. Unchecked exceptions encode **programming errors** and JVM-level failures (`NullPointerException`, `OutOfMemoryError`) that scattering `throws` clauses cannot meaningfully fix. The `throws` clause is therefore a design tool as much as a language rule: a method whose signature lists five checked types is a design smell asking for narrower exceptions or wrapping. Where checked exceptions land in the hierarchy is in [[Do checked exceptions inherit Throwable directly]], and the classification of `Error` subtrees in [[Are Error subclasses checked or unchecked]].

> [!warning] `throws` never throws anything
> A signature declaring `throws IOException` without a single `throw` inside compiles fine — and a method throwing `IOException` **without** declaring it (and without catching) is a compile error. But the reverse trap is the popular one: `throw` throws an object, `throws` declares a possibility; confusing them (`throw new IOException(...)` vs `void f() throws IOException`) is a compile-time mistake, while believing a declaration *guarantees* an exception will occur is a design misunderstanding. Also remember that unchecked exceptions need no `throws` — `RuntimeException` propagates through any signature invisibly.

> [!tip] Interview answer
> **`throws` declares in the method's signature which checked exceptions it may propagate — it's a compiler-enforced contract: callers must catch them or declare them onward, per JLS 11.2. Unchecked exceptions — RuntimeException and Error subtrees — are exempt. On overriding, the rule is narrowing only: an override may declare fewer or more specific checked exceptions but never more than the overridden method, JLS 8.4.8.3. And keep the vocabulary straight: throw raises an exception, throws declares the possibility.**
