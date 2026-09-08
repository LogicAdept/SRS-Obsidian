<!--
reps: 0
priority: 0
-->
#Java/Language #Java/JVM #SRS

# How would you explain distinctive traits of the Java programming language?

> [!abstract] Short answer
> The language is **general-purpose, concurrent, class-based, and object-oriented**, **strongly and statically typed**, and **normally compiled to machine-independent bytecode**. It hides the machine: **automatic storage management**, **bounds-checked** arrays, **fixed-size primitives** on every implementation, and **`boolean`** (not “nonzero `int`”) in control flow. Related to C and C++ but organized differently: no `goto`, no `free`/`delete`, no unchecked indexing. The VM that runs the `class` files is the platform story: [[How would you explain distinctive traits of the Java platform]].

## What the language is, versus C, versus the VM

**Typing.** Every variable and expression has a compile-time type; that type limits values and operations ([[How would you explain static typing in Java]], [[What does strong typing mean in Java]]). Casts on references are checked at run time. Primitive widths (`int`, IEEE 754 floats, `boolean`, `char`) are the same on every host; primitive values do not share state ([[How would you explain Java primitive data types]]).

**Objects.** Classes use **single inheritance** up to `Object`. Interfaces give multiple inheritance of type. Instance methods run with `this`. Arrays are objects and are bounds-checked. It is class-based OO with primitives that are not objects ([[What does it mean that Java is object oriented]], [[Why is Java described as not purely object oriented]]).

**Safety and structure.** Unreachable objects may be reclaimed; there is no language-level `free`. `if` / `while` / `for` conditions are `boolean` or `Boolean` ([[Why cannot Java logical operators be applied to integers]]). Methods declare **checked** exceptions the compiler tracks. `synchronized` methods and statements are the basic monitor API; the language also defines a **memory model**. Packages (and modules) name and hide members. No `goto`; labeled `break` / `continue` instead.

**Compilation.** Compile time translates programs into a machine-independent bytecode representation. Run time loads, links, and initializes classes, may generate native code, and executes. That bytecode format is defined by the JVM specification — other languages can target it ([[Which programming languages besides Java compile to JVM bytecode]], [[How does the JVM help Java bytecode run across operating systems]]). JDK vs JRE: [[What is the difference between the JDK and the JRE]].

```d2
direction: down
lang: "source: typed, class-based, concurrent" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
bc: "compile to bytecode\n(class file)" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
hide: "no free, no unchecked []\nboolean in if, fixed primitives" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
lang -> bc
lang -> hide
```

**Fig. 1.** Distinctive as a **language**: what you may write, and that compilation yields portable bytecode rather than a host `exe`.

```java
class Test {
    public static void main(String[] args) {
        for (int i = 0; i < args.length; i++) {
            System.out.print(i == 0 ? args[i] : " " + args[i]);
        }
        System.out.println();
    }
}
```

**Listing 1.** Typical shape: a class, a `main`, a bounds-checked loop, `String` as a class. Same source is valid on every Java SE implementation.

Enums and records are restricted class forms. Generics parameterize classes and methods by **reference** types. `var` only infers a compile-time type. Those are still this language; they are not a second, dynamic Java.

> [!warning] “Interpreted” is not the language’s identity
> Bytecode may be interpreted, JIT-compiled, or both. The language fact is **compilation to a `class` file**, not “Java has no compiler.” Do not cite green threads or a particular collector as a language trait — those are VM implementations ([[How would you explain distinctive traits of the Java platform]]).

> [!warning] Familiar-to-C is not C
> Tokens look like C. `if (n)`, `n || m` on ints, pointer arithmetic, and `free` are **gone** on purpose so more errors are compile-time or specified. Answering “it’s like C++ without pointers” skips the actual list: class-based OO, boolean conditions, GC, checked exceptions, and bytecode.

> [!tip] Interview answer
> **Java is a class-based, concurrent, strongly and statically typed language that compiles to portable bytecode and hides the machine — GC, checked array indexes, fixed primitive sizes, `boolean` in `if`.** It resembles C in spelling, not in memory model. The JVM is how those `class` files run, not a second syntax.
