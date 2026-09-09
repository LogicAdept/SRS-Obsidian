<!--
reps: 0
priority: 0
-->
#Java/StringBuilder #Patterns/GoF #SRS

# How would you explain which design pattern ideas appear in StringBuilder and StringBuffer

> [!abstract] Short answer
> **StringBuilder is a mutable char buffer whose `append`/`insert` methods return `this` — a fluent Builder-style chaining API — over an internal growable array.** StringBuffer is the same design with `synchronized` methods, a Decorator-by-inheritance that trades speed for thread safety. The real pattern lesson: mutable buffer + fluent construction solves the immutability cost of `String`.

## Why they exist: String immutability is expensive in loops

`String` is immutable; every `+` concatenation copies both operands. Building a 10 000-piece string with `+` in a loop is quadratic; a StringBuilder appends into one growable buffer, doubling capacity as needed, and produces the final `String` once via `toString()`.

```d2
direction: right
s: "String concat\ns = s + x\ncopy every time" {
  width: 270
  height: 100
  style.fill: "#ffebee"
}
sb: "StringBuilder\nappend into one buffer\nreturn this" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
sfx: "StringBuffer = same +\nsynchronized methods" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
s -> sb: "use in loops"
sb -> sfx: "need thread safety?"
```

**Fig. 1.** The design decision tree: immutable default, mutable builder for assembly, synchronized wrapper only for shared state.

```java
StringBuilder sb = new StringBuilder("Java");
sb.append(21).insert(0, ">>> ").reverse();
System.out.println("chain result: " + sb);
```

**Listing 1.** Verified on JDK 21:

```java
chain result: 12avaJ >>>
```

**Listing 2.** Three mutations chained: each method modified the buffer and returned `this`, which is what makes the fluent style compile — the Builder-pattern signature without a separate product class.

## The pattern ideas, named honestly

**Builder-flavored fluent construction.** The `append(...).append(...).toString()` idiom is the Builder idea — accumulate parts, produce the immutable product at the end (`toString` snapshots the buffer). It is not the GoF Builder verbatim (no separate builder/product types, no director), but the *shape* — named in interviews as "builder-like fluent API". **Encapsulated invariants over a mutable core.** The internal array is private; capacity growth is managed; `toString` copies — state machine hidden behind a small method surface. **Synchronized wrapper (StringBuffer).** StringBuffer predates StringBuilder (Java 1.0/1.2 vs Java 5) and bolts thread safety onto the same API with synchronized methods — a concrete example of gaining safety by wrapping, at a per-call monitor cost. **Interface-backed abstraction.** Both implement `CharSequence` and `Appendable`, so code written against the interface accepts either.

> [!warning] StringBuffer is almost always the wrong answer — and the builder is not thread-safe magic
> Two traps. First: "StringBuilder is not thread-safe, so I use StringBuffer" — in the overwhelming majority of real code the buffer is a local variable inside one method, which is trivially single-threaded; the synchronized StringBuffer then only adds lock overhead. It earns its place only when one buffer is genuinely mutated by several threads, and even then a shared mutable builder usually signals a design smell. Second: the fluent-chaining pattern idea does NOT extend to `String` — `str.toUpperCase().trim()` works because String methods return *new immutable strings*, not `this`; confusing the two styles leads people to mutate a StringBuilder after calling `toString()` and expect the result to change (it snapshots). Third, the classic performance claim needs its precondition: concatenation cost is quadratic in the *loop* case; a single `a + b + c` in modern Java compiles to StringBuilder-equivalent code (invokedynamic StringConcatFactory, Java 9+), so hand-optimizing one-liners is noise. The immutability side of the contrast: [[What is the Java string pool]], [[How would you explain immutable classes in Java]].

> [!tip] Interview answer
> **StringBuilder is a mutable buffer with a fluent API — append and insert return this, so calls chain, and toString produces the final immutable String: the Builder idea applied to text. It exists because String concatenation in loops copies repeatedly — quadratic versus linear. StringBuffer is the same class with synchronized methods, thread-safe but slower; for local buffers StringBuilder always wins. Both hide a growable char array behind CharSequence.**

