<!--
reps: 0
priority: 0
-->
#Java/JVM/Memory/Heap #Java/String #SRS

# Which memory region holds strings in Java?

> [!abstract] Short answer
> Every `String` **instance** (literal, `new String`, concatenation, `intern` result) is a **heap object**, plus its **payload array**. Literals and constant expressions are **interned**: they share unique heap instances via a private **pool of strings**. The **run-time constant pool** in the **method area** stores **references** to those instances, not the characters. Since JDK 7 interned strings are **not** in PermGen — [[Which memory region holds objects in Java]], [[What is the JVM class constant pool]].

## Heap objects; a table of pointers

JLS: at run time a **string literal** is a **reference** to a `String` instance. Literals and string-valued **constant expressions** are interned “as if” by `String.intern`, so they **always** denote the **same** instance. Loading a class **may** create that object unless an equal sequence was interned already. A `+` that is **not** a constant expression **always** creates a **new** `String`.

`String.intern`: the class maintains a private **pool** (initially empty). If an equal string is already there, that instance is returned; otherwise **this** object is added and returned. `s.intern() == t.intern()` iff `s.equals(t)`.

JVMS: a `CONSTANT_String` becomes a run-time **string constant** — a **reference** to an interned `String`, derived by intern-or-create. That reference lives in the per-class **run-time constant pool** (method area). The `String` itself is still a class instance → **heap**. HotSpot moved interned strings **out of PermGen onto the Java heap** (JEP 122); Metaspace does **not** hold them — [[What is Metaspace and how does it differ from PermGen]].

A local `String s` holds the **reference** in a **frame**. `new String("x")` allocates a **second** heap object; `"x"` stays the interned one.

```java
public final class WhereStringsLive {
    public static void main(String[] args) {
        String lit = "hello";
        String copy = new String("hello");
        String interned = copy.intern();
        System.out.println(lit == interned);
        System.out.println(lit == copy);
    }
}
```

**Listing 1.** `lit == interned` is `true` (same pooled instance). `lit == copy` is `false` (`new` made another heap `String`). Both objects, and their `byte[]` payloads, live on the **Java heap**.

```d2
direction: down
rcp: "Run-time constant pool\n(method area): references" {
  width: 320
  height: 50
  style.fill: "#fff8e1"
}
pool: "String intern table\n(pointers to unique instances)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
heap: "Java heap: String + payload array" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
rcp -> heap
pool -> heap
```

**Fig. 1.** The “string pool” is a **lookup table** of heap references, not a PermGen/Metaspace region that stores characters.

> [!warning] Interned strings are heap objects
> Answering “strings live in PermGen / Metaspace / the constant pool” mixes the **pointer** with the **instance**. Character data is on the **heap** (`-Xmx`). A huge intern table still pressures the **Java heap**.

> [!warning] `new String("…")` is not interned by default
> Only literals, compile-time constant concatenations, and an explicit `intern()` share identity. Runtime `+` and `StringBuilder` produce **new** heap strings. `==` on those is the wrong test — use `equals`.

> [!tip] Interview answer
> String objects and their character arrays live on the Java heap, including interned literals. The constant pool and intern table only hold references to those objects. PermGen used to store interned strings; Metaspace does not.
