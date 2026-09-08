<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Bytecode #SRS

# Which languages besides Java run on the JVM?

> [!abstract] Short answer
> Any language whose compiler emits valid class files: the JVM has no idea Java exists — it executes bytecode. In practice the mainstream choices are Kotlin, Scala, Apache Groovy, and Clojure; each compiles to the same class file format and reuses the JVM's memory management, JIT, and libraries.

## Why it works at all

The class file format is the public contract of the platform: the specification states that any language with functionality expressible in terms of a valid class file can be hosted by the JVM. A JVM language therefore ships a compiler (or interpreter) that maps its constructs onto bytecode — objects, methods, and dynamic invocation where needed — and everything below the class file boundary is shared: the garbage collector, the JIT tiers, the thread model, and the entire Java class library are consumed as-is.

```d2
direction: right
kt: "Kotlin\nstatically typed" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
sc: "Scala\nstatically typed" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
gr: "Groovy\ndynamic + static" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
cl: "Clojure\nLisp dialect" {
  width: 190
  height: 80
  style.fill: "#e3f2fd"
}
cf: "class files\n(one binary contract)" {
  width: 240
  height: 90
  style.fill: "#fff3e0"
}
jvm: "JVM\nGC · JIT · Java libraries" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
kt -> cf
sc -> cf
gr -> cf
cl -> cf
cf -> jvm
```

**Fig. 1.** Four languages, one binary format. Interoperability happens at the bytecode level, so a Kotlin class can extend a Java class and vice versa.

## The four you should name

Kotlin is an open-source statically typed language that targets the JVM (and other platforms) and is designed for Java interoperability. Scala positions itself on the JVM runtime with strong static typing and interoperable access to Java libraries. Apache Groovy calls itself a multi-faceted language for the JVM, usable both dynamically and with static compilation. Clojure is a Lisp dialect designed as a hosted language on the JVM. All four call Java methods directly, and all four are called from Java through their compiled classes.

```java
// Nothing JVM-specific is needed to host another language:
//   kotlinc hello.kt -include-runtime -d hello.jar   // Kotlin compiles to class files
//   java -jar hello.jar                              // a regular JVM runs it
// The JVM sees ordinary class files — no "Kotlin mode" exists.
```

**Listing 1.** From the JVM's point of view there is nothing to enable: the language compiler produces the same bytecode artifact.

> [!warning] Sharing bytecode does not mean sharing semantics
> Language features that are not JVM concepts get implemented *inside* each compiler, and that shows at runtime. Kotlin's null safety is a compile-time discipline — a Java caller can still pass `null` into Kotlin code and trigger the runtime check. Scala and Clojure bring their own collection hierarchies instead of using `java.util` everywhere. And when a language needs JVM changes, it waits for the platform: features like `invokedynamic` unlocked dynamic language performance only after the JVM added them. See [[Is Java a compiled or interpreted language]] for the pipeline and [[What is the JVM class constant pool]] for what lives inside a class file.

For the machine these languages ride on, see [[What is the JVM]]; for the portability mechanism that makes one class file run everywhere, [[Why is Java described as platform independent]].

> [!tip] Interview answer
> The JVM hosts any language that compiles to valid class files — that is what the class file format is for. The mainstream ones are Kotlin, Scala, Groovy, and Clojure: their compilers emit bytecode and they reuse the JVM's GC, JIT, and Java libraries, calling Java and being called from Java. Just remember the boundary: language-level guarantees like Kotlin null safety live in the compiler, not in the JVM, so cross-language calls can still violate them.
