<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory/Heap #SRS

# How do string literals enter the Java string pool?

> [!abstract] Short answer
> Through **class file constant-pool entries and resolution**. The compiler writes each literal as a `CONSTANT_String_info` entry in the class's constant pool ([[What is the JVM class constant pool]]). When the code first uses it (`ldc`), the JVM **resolves** the symbolic reference: it looks for an equal string in the string table and reuses it, or interns a new one — JLS 3.10.5 says every literal "always refers to the same instance of class String", interned "as if by `String.intern`". The same literal in two different classes therefore resolves to **one** instance — [[What is the Java string pool]], [[What does the String intern method do in Java]].

## Compile time, then lazily at first use

1. **Compile time** — `javac` stores `"srs"` in the class's constant pool. **Constant expressions** (`"sr" + "s"`, `final String F = "s" + "r"`) are **folded by the compiler** into a single literal — no runtime concatenation happens.
2. **Resolution (lazy)** — the entry is a *symbolic* reference until the instruction that uses it executes; only then does the JVM canonicalize the string into the table. Unloaded or unused literals cost nothing at runtime.
3. **Runtime concatenation is different** — `prefix + "s"` with a non-constant `prefix` runs `StringConcatFactory`-based code and yields a **fresh** object; only an explicit `intern()` puts it in the pool.

```java
public class Entry {
    static final String F = "sr" + "s";   // folded at compile time

    public static void main(String[] args) {
        String a = "srs";                 // CONSTANT_String_info
        String b = F;                     // same folded literal
        String c = "s".repeat(3);         // runtime-built, NOT pooled
        System.out.println(a == b);       // true  — one constant
        System.out.println(a == c);       // false — fresh instance
        System.out.println(a == c.intern()); // true — canonicalized
    }
}
```

**Listing 1.** `a` and `b` reference the identical pooled instance because the compiler folded `F`; `repeat(3)` builds a runtime string that needs `intern()` to join the pool. Verified on JDK 21.

```d2
direction: down
src: "javac: literal →\nCONSTANT_String_info in class file" {
  width: 320
  height: 66
  style.fill: "#e3f2fd"
}
ldc: "first execution of ldc\n(lazy resolution)" {
  width: 300
  height: 56
  style.fill: "#fff8e1"
}
tbl: "String table\nequal contents?" {
  width: 230
  height: 60
  style.fill: "#fce4ec"
}
reuse: "reuse pooled instance" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
add: "intern a new one\nand add to table" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
src -> ldc -> tbl
tbl -> reuse: "yes"
tbl -> add: "no"
```

**Fig. 1.** A literal enters the pool when its constant-pool entry is resolved at first use — reused if equal contents are already pooled, interned otherwise.

> [!warning] "Loaded into the pool at class load" is imprecise
> The JVM is allowed to defer resolution until the entry is actually used, so a class full of literals does not populate the pool merely by being loaded. And the flip side of sharing: interning means one instance per content **globally** — mutation is impossible only because `String` is immutable ([[Why is java.lang.String immutable and final]]). Do not claim literals are "copied into the heap at startup"; they enter through resolution, class by class.

> [!tip] Interview answer
> Literals get into the pool in two steps: the compiler records them as constant-pool entries in the class file, and the JVM canonicalizes the entry at first use, sharing or interning the instance in the string table — JLS 3.10.5 guarantees every literal always refers to the same instance. Compile-time constant expressions are folded before this, so `"sr"+"s"` is just another literal; runtime-built strings only enter via `intern()`.
