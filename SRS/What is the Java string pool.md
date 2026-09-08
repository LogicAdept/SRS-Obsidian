<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory/Heap #SRS

# What is the Java string pool?

> [!abstract] Short answer
> The string pool is the JVM's table of **unique `String` instances**, "maintained privately by the class `String`" (the `intern()` javadoc). **All literals and string-valued constant expressions are interned**: `"a"` in two classes yields one shared object (JLS 3.10.5). It exists because `String` is immutable, so instances can be shared like **flyweight** objects, saving memory and making `==` meaningful for pooled strings. Since **JDK 7** the pool lives **on the heap** (before that, in the permanent generation) — [[How do string literals enter the Java string pool]], [[Which memory region holds the string pool in Java]].

## A table of references, not a special storage

The pool (HotSpot's **string table**) is a hash table of references to ordinary heap `String` objects — the objects themselves are normal, GC-managed instances. Literal resolution and `intern()` both consult this table: if an equal string is present, that instance is reused; otherwise the string is added ([[What does the String intern method do in Java]]). A stock JDK 21 hello-world finishes with roughly **2 700 entries** already in the table (`-XX:+PrintStringTableStatistics`), so "the pool is some rarely used cache" is off by orders of magnitude — [[Is the Java string pool empty when a JAR application starts]].

```java
public class Pool {
    public static void main(String[] args) {
        String a = "srs";
        String b = new String("srs");      // forced fresh heap object
        String c = "sr" + "s";             // constant expression → interned
        System.out.println(a == b);        // false: new bypasses the pool
        System.out.println(a == c);        // true:  same pooled instance
        System.out.println(a == b.intern()); // true: b's canonical = a
    }
}
```

**Listing 1.** Literals and compile-time constants share one pooled instance; `new String` always builds a separate object whose `intern()` is the pooled one. Verified on JDK 21.

```d2
direction: right
src: "Class file literals\n\"srs\" in A and B" {
  width: 250
  height: 66
  style.fill: "#e3f2fd"
}
tbl: "String table\n(hash of references)" {
  width: 230
  height: 70
  style.fill: "#fff8e1"
}
heap: "Heap" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
  s: "String \"srs\"\none instance" {
    width: 180
    height: 44
  }
}
src -> tbl: "resolve / intern()"
tbl -> heap.s: "one shared ref"
```

**Fig. 1.** The string table maps equal contents to a single heap instance; classes and runtime code all get the same reference back.

> [!warning] The pool deduplicates interned strings, not all strings
> `new String("x")` never returns a pooled instance — the pool is consulted only for literals, constant expressions, and explicit `intern()`. Concatenation with variables (`prefix + "x"`) runs at runtime and produces a fresh object too. Also, comparing *interned* strings with `==` works, but doing it for arbitrary strings is a bug factory: equal contents, different instances — [[Why is java.lang.String immutable and final]].

> [!tip] Interview answer
> It's the JVM's table of unique string instances — the mechanism behind JLS 3.10.5: every literal and compile-time constant resolves to one shared object. It's a hash table of references to ordinary heap strings (in the heap since JDK 7, in PermGen before), populated as classes resolve literals and when code calls `intern()`. Because strings are immutable, sharing is safe, which is what makes the pool a classic flyweight cache.
