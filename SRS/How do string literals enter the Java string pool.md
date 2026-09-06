<!--
reps: 0
priority: 0
-->
#Java/String #Java/JVM/Memory #SRS

# How do string literals enter the Java string pool

> [!abstract] Short answer
> **They are interned when their class is created, not when `javac` finishes and not when the line of code runs.** The compiler writes a `CONSTANT_String` (Utf8 payload) into the class file. Loading that class builds the run-time constant pool: if `String.intern` has already seen that Unicode sequence, the constant is a reference to the existing interned instance; otherwise the VM allocates a `String` and intern()s it into `String`’s private pool. Compile-time constant concatenations are treated as literals. Run-time `+` and `new String(...)` do not enter the pool unless you intern them.

## Class file first, intern pool at class creation

A string literal (and a text block) is a reference to a `String` that **always denotes the same instance**. Sharing is intern: unique instance per distinct sequence of code points, as if `String.intern` ran. The same rule covers **string-valued constant expressions** — `"Hel"+"lo"`, `"The integer " + Long.MAX_VALUE`, a concatenation that uses only literals, text blocks, and `static final` constant variables.

That is not a compile-time heap. `javac` records the characters as a **`CONSTANT_String_info`** in the class-file `constant_pool`. That table is **not** the intern pool ([[What is the JVM class constant pool]]).

When the VM **creates** the class, it constructs the **run-time** constant pool from that table. A `CONSTANT_String` is a **static** constant (no later resolution step):

1. Look at the code points in the Utf8 payload.
2. If `intern` has already been invoked on a `String` with that sequence, the constant is a reference to **that** instance.
3. Otherwise create a new `String` with those code points, then invoke `intern` on it.

`ldc` / `ldc_w` then push that interned reference. Literals in the same class, other classes, or other packages all land in **one** intern pool, so `"Hello" == Other.hello` is true when both are literals. Bootstrap and JDK classes fill the pool the same way as they are created; the pool is specified as **initially empty**, then grows as classes appear — not as a scan of every string in a JAR at JVM start ([[What is the Java string pool]]).

`String.intern` is the same table for hand-built strings: if the pool already has an `equals` match, return that instance; else add **this** object and return it ([[What does the String intern method do in Java]]).

```d2
direction: down
src: "Source\n\"Hello\" or \"Hel\"+\"lo\"" {
  width: 280
  height: 50
}
cf: "Class file constant_pool\nCONSTANT_String → Utf8" {
  width: 300
  height: 50
}
create: "Class creation\nderive string constant" {
  width: 280
  height: 50
}
hit: "intern already saw\nthis code-point sequence?" {
  width: 280
  height: 55
}
reuse: "Reuse interned String" {
  width: 240
  height: 45
}
alloc: "new String, then intern()" {
  width: 240
  height: 45
}
pool: "String intern pool\n(private to String)" {
  width: 280
  height: 50
}
ldc: "ldc / ldc_w\npush interned reference" {
  width: 280
  height: 50
}

src -> cf: "compile"
cf -> create: "load / create class"
create -> hit
hit -> reuse: "yes"
hit -> alloc: "no"
reuse -> pool
alloc -> pool
pool -> ldc
```

**Fig. 1.** Compile time only stores characters. Intern happens while the run-time constant pool is built. `ldc` does not intern a second time.

```java
public class LiteralPoolDemo {
    static final String LO = "lo"; // constant variable

    public static void main(String[] args) {
        String hello = "Hello";
        String lo = "lo";
        System.out.println(hello == "Hello");             // true — same interned instance
        System.out.println(hello == ("Hel" + "lo"));      // true — compile-time constant
        System.out.println(hello == ("Hel" + LO));        // true — constant variable
        System.out.println(hello == ("Hel" + lo));        // false — run-time concatenation
        System.out.println(hello == ("Hel" + lo).intern()); // true
        System.out.println(hello == new String("Hello")); // false — extra copy
    }
}
```

**Listing 1.** Literals and constant concatenations share identity. A run-time `+` and `new String("Hello")` allocate distinct objects; `intern()` joins the pool. The `"Hello"` argument of `new String` was interned when this class was created.

> [!warning] Intern is not “any String with those characters”
> `"Hel" + lo` is **always a new** `String` when `lo` is not a constant. `new String("Hello")` is another object even though the literal `"Hello"` is already interned. `==` is identity, not `equals`. Loading a class interns its literals even if you never run the method that mentions them. Do not confuse the per-class `constant_pool` (Utf8 bytes on disk / metadata) with `String`’s intern pool (canonical `String` instances).

> [!tip] Interview answer
> **Literals (and compile-time string constants, including text blocks) enter the intern pool when the class is created.** The class file holds `CONSTANT_String`; the VM intern()s that sequence into `String`’s private pool, reusing an equal instance if one exists. Runtime concatenation and `new String(...)` stay outside until you call `intern()`.
