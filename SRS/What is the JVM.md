<!--
reps: 0
priority: 0
-->
#Java/JVM #SRS

# What is the JVM?

> [!abstract] Short answer
> The JVM is the abstract computing machine that actually runs a Java program: it loads class files, manages run-time memory, and executes bytecode through an interpreter plus JIT compilers. It is defined by a specification, not by any single product, and it is tied to the class file format, not to the Java language itself.

## What the machine consists of

The JVM specification describes three cooperating parts. The **class loading subsystem** locates and defines classes from class files. The **run-time data areas** (heap, per-thread stacks, method area, pc registers, native method stacks) hold everything the program manipulates. The **execution engine** interprets and compiles bytecode into CPU work. The spec also requires enough JVM support for the class libraries: reflection, `ClassLoader`, `Thread`, and `java.lang.ref` cannot be implemented without it.

```d2
direction: down
classfile: "class files\n(Java, Kotlin, Scala, …)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
loader: "Class loading subsystem\nload → link → initialize" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
areas: "Run-time data areas\nheap · stacks · method area · pc" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
engine: "Execution engine\ninterpreter + JIT → native code" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
os: "Host OS and hardware" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
classfile -> loader
loader -> areas
areas -> engine
engine -> os
```

**Fig. 1.** A JVM turns class files into running code on one specific host. The class file format and the instruction set are the public contract; everything inside may be implemented freely.

## Specification, not a product

The JVM is an *abstract* machine: the specification fixes observable behavior — the class file format and the semantics of the instruction set — while leaving the implementation free. HotSpot, OpenJDK builds, GraalVM, and J9 are all implementations of the same contract. The spec explicitly says the JVM is not inherently interpreted; an implementation may compile instructions straight to CPU code. Implementation details such as which JIT tiers exist, how threads map to OS threads, or how the heap is laid out belong to the product, not the contract.

> [!warning] "The JVM knows Java"
> The JVM has no idea what Java source code looks like. It only knows a binary format, the class file, and it will host *any* language whose semantics can be expressed in valid class files. Saying "the JVM is a Java interpreter" is wrong on both ends: it does not speak Java, and it does not merely interpret — HotSpot compiles hot code to native.

## What it does for the programmer

Three responsibilities make the JVM the cornerstone of the platform. It gives **hardware and operating-system independence**: the same class files run wherever a JVM exists. It provides **memory management**: objects are allocated on a managed heap and reclaimed by the garbage collector, so there is no manual `free`. It enforces **structural constraints** on loaded code, which is the basis for running untrusted bytecode safely. For the follow-up "where does it end": native libraries, file paths, and everything below the JVM interface stay platform-specific. See [[Why is Java described as platform independent]].

```java
// The JVM the process runs on, from inside the program:
System.out.println(System.getProperty("java.vm.name"));    // OpenJDK 64-Bit Server VM
System.out.println(System.getProperty("java.vm.version")); // e.g. 21.0.12+13
```

**Listing 1.** `java.vm.*` properties identify the implementation currently executing the code.

> [!tip] Interview answer
> The JVM is the specification-defined virtual machine that executes Java programs: it loads and verifies class files, provides the run-time data areas and garbage collection, and executes bytecode with an interpreter plus JIT compilers. It is implementation-independent — HotSpot is one implementation — and it is tied to the class file format rather than to the Java language, which is why other languages can target it.

For the surrounding products, see [[What is the difference between the JVM the JRE and the JDK]]; for memory internals, [[What JVM runtime memory regions exist]].
