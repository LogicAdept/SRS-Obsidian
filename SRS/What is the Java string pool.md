<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory #SRS

# What is the Java string pool

> [!abstract] Short answer
> **The string pool is `String`’s private intern table: at most one interned instance per distinct character sequence (`equals`).** Literals and compile-time string constants are interned when their class is created. Anything else enters only if you call `intern()`. The interned object is an ordinary heap `String`. The table is **not** the per-class `constant_pool`. `==` on two interned equal strings is identity; `equals` is what the pool uses to match.

## One canonical `String` per sequence

The pool starts empty and is maintained by `String`. `intern()` returns the pooled instance if one `equals` this string; otherwise **this** object is added and returned. For any live interned `s` and `t`, `s.intern() == t.intern()` iff `s.equals(t)` ([[What does the String intern method do in Java]]).

How values get there:

- **Literals and text blocks**, and **constant** concatenations (`"Hel"+"lo"`). The class file stores `CONSTANT_String` → Utf8. At **class creation** the VM derives a string constant: reuse an already interned instance or `new String` then `intern` ([[How do string literals enter the Java string pool]]). `ldc` then pushes that reference.
- **Explicit `intern()`** of a computed string (the same table).

Not in the pool automatically: `new String("x")` (the extra copy), run-time `+`, `StringBuilder.toString()`, scanner input.

Do not confuse three structures. The **class-file `constant_pool`** holds Utf8 bytes. The **run-time constant pool** (method area) holds a *reference* to the interned instance. The **intern pool** is the JVM-wide canonical set of those instances ([[What is the JVM class constant pool]], [[Which memory region holds the string pool in Java]]).

HotSpot keeps interned objects on the **Java heap** (not PermGen after Java 7). The native string table holds **weak handles**, so an interned string with no other refs can be collected; literals stay alive with their loaded class ([[How long do strings live in the Java string pool]]). Do not intern secrets or unbounded unique untrusted text ([[How would you explain security implications of string interning and the string pool]]).

```d2
direction: down
src: "Literal / constant concat / intern()" {
  width: 300
  height: 45
}
cf: "Class file CONSTANT_String\n(not the intern pool)" {
  width: 280
  height: 50
}
pool: "String intern pool\none instance per equals sequence" {
  width: 300
  height: 50
}
heap: "Interned String objects\nJava heap; table does not pin" {
  width: 300
  height: 50
}

src -> cf: "compile literals"
src -> pool: "intern() / class creation"
cf -> pool: "resolve CONSTANT_String"
pool -> heap
```

**Fig. 1.** Intern pool = canonical `String` instances. Class-file constants are how literals are *named*, not a second copy of the pool.

```java
public class StringPoolExplainDemo {
    static void demo(String runtime) {
        String a = "Hello";
        String b = "Hel" + "lo";           // compile-time → interned
        String c = "Hel" + runtime;        // run-time → new String
        String d = new String("Hello");    // extra copy; literal still interned
        boolean literals = a == b;         // true
        boolean runtimeDistinct = a == c;  // false when runtime is "lo"
        boolean interned = a == c.intern();
        boolean copyDistinct = a == d;     // false
    }
}
```

**Listing 1.** The pool is identity for interned content. Runtime concat and `new String` stay outside until `intern()`.

> [!warning] Pool ≠ class constant pool, and intern ≠ forever
> `javap`’s `CONSTANT_String` list is per class, not the intern table. Two equal literals are the same instance; two equal `new String(...)` results are not. The pool does not keep interned objects alive by itself on HotSpot. A literal is interned once per class creation — the pool does not make every `String` construction slower. Interning every unique log line wastes heap; it does not encrypt.

> [!tip] Interview answer
> **The string pool is String’s intern table: unique interned instance per `equals` sequence.** Literals and constant concatenations go in at class load; other strings only via `intern()`. It is not the class-file constant pool. Interned objects live on the heap and last while reachable, not “until the JVM dies” as a PermGen myth.
