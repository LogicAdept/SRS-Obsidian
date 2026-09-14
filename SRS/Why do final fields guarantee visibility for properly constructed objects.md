<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Language/Modifiers/Final #SRS

# Why do final fields guarantee visibility for properly constructed objects

> [!abstract] Short answer
> **If an object is properly constructed — its reference does not escape before the constructor finishes — then any thread that reads a reference to it sees the correctly initialized values of its final fields, without any synchronization (JLS 17.5).** Final fields are "frozen" at constructor completion, and this holds even when the object is published through a data race.

This is the one safe-publication mechanism that needs no explicit edge at the read site. For ordinary fields, a racing reader may see defaults or stale values ([[What is the default value happens-before rule in the Java Memory Model]]); for final fields the JLS adds freeze semantics: the compiler and runtime may not move the final field's initialization where a later read could miss it, and the reader of a properly published reference is guaranteed to observe the constructed values. That is what makes immutable value objects — strings, boxed numbers, records, `Collections.unmodifiableList` wrappers — safe to share across threads with no locking at all, and it is the memory-model reason immutability is the recommended default for shared state ([[How would you explain immutable classes in Java]], [[Why are immutable objects valuable in concurrent code]]).

```d2
direction: right
c: "Constructor thread" {
  w: "final int a = 41;\nfinal int b = 1;" { style.fill: "#e3f2fd" }
  end: "constructor completes\n(final fields frozen)" { style.fill: "#fff3e0" }
  w -> end: "program order"
}
r: "Reader thread" {
  ref: "reads reference\n(even via data race)" { style.fill: "#f3e5f5" }
  rd: "reads a and b\n-> guaranteed 41 and 1" { style.fill: "#e8f5e9" }
  ref -> rd: "program order"
}
end -> ref: "publication (any mechanism,\nno lock required)"
```

**Fig. 1.** The freeze at constructor end: whatever mechanism publishes the reference — even a racy one — the final field values the reader observes are the constructed ones.

```java
class Range {
    final int low;      // frozen at constructor end
    final int high;

    Range(int low, int high) {
        this.low = low;
        this.high = high;
    }
}

// reader thread, with the reference obtained through any publication path:
Range r = registry.get("range");   // even without synchronization on the registry
if (r.low <= r.high) { ... }        // guaranteed the constructed values
```

**Listing 1.** Once the constructor completes without `this` escaping, every thread reading that `Range` sees `low` and `high` as set — no `volatile`, no lock, no happens-before proof needed at the read site.

> [!warning] Properly constructed is a real precondition
> Letting `this` escape during construction — registering a listener, starting a thread, storing into a static field inside the constructor — voids the guarantee for the racing publication ([[What is the thread start rule in the Java Memory Model]]). Two further limits: final applies to the *field*, not its contents — a final reference to a mutable `List` freezes the reference, not the list's elements, which still need synchronization when mutated ([[How would you explain immutable classes in Java]]); and the guarantee covers reads of the frozen values, not write-protection, since reflection or unsafe paths can technically alter final fields after construction.

> [!tip] Interview answer
> **JLS 17.5: for a properly constructed object — no this-escape before the constructor completes — every thread reading a reference to it sees fully initialized final fields without any synchronization; the values are frozen at constructor end. That is why immutable objects are thread-safe by construction. The precondition matters: escape during construction or mutable contents break the story.**
