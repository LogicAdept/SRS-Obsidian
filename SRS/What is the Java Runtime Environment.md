<!--
reps: 0
priority: 0
-->
#Java/JRE #Java/JDK #SRS

# What is the Java Runtime Environment?

> [!abstract] Short answer
> The JRE is the runtime half of Java: a JVM plus the platform class libraries — everything needed to execute already-compiled bytecode, and nothing needed to produce it (no `javac`, no build tools). Since JDK 11 it is no longer shipped as a separate product; runtimes today are either the JDK itself or custom images built with `jlink`.

## What it contains

The JRE bundles two things that cannot run a program separately. The **JVM** provides execution: class loading, memory management, garbage collection, JIT compilation, threads. The **platform class libraries** provide the API surface programs actually call — `java.lang`, `java.util`, IO, networking. Without the libraries the JVM has no `String` to hand you; without the JVM the libraries are just bytecode on disk. What the bundle deliberately lacks is the development side: no compiler, no archiver, no `jlink`.

```d2
direction: right
jre: "JRE" {
  width: 140
  height: 70
  style.fill: "#e3f2fd"
}
jvm: "JVM\nclass loading · GC · JIT · threads" {
  width: 320
  height: 100
  style.fill: "#e8f5e9"
}
lib: "platform class libraries\njava.lang · java.util · IO · net" {
  width: 340
  height: 100
  style.fill: "#fff3e0"
}
nojavac: "not included: javac, jar, jlink" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}
jre -> jvm
jre -> lib
jre -> nojavac: absent by design
```

**Fig. 1.** Runtime = execution engine plus the libraries the code calls; the developer toolchain is out of scope.

```java
// Inside a JRE-only runtime, running works and compiling does not:
//   java -jar app.jar          ✓ the JVM loads bytecode and runs it
//   javac App.java             ✗ javac is a JDK tool, not part of the runtime
//   java App.java              ✗ source-file mode invokes the compiler internally
```

**Listing 1.** The boundary in one screen: bytecode in, behavior out; sources need the JDK.

## From product to component

Historically the JRE was the deployment product: servers installed a JRE, developers a JDK. As of JDK 11, Oracle stopped offering the separate JRE and Server JRE downloads — only the JDK is shipped, and `jlink` assembles per-application runtimes from modules. The term survives as a *conceptual* layer inside every JDK: when a JDK runs your code, it acts as the JRE. This is why modern deployment talk says "a runtime" or "a jlink image" rather than "a JRE install".

> [!warning] "JRE = JVM" is the classic conflation
> The JVM alone cannot run an application: `new ArrayList<>()` requires the collections library, and even `System.out` is a library type. Whenever an answer equates the two, correct it to "the JRE wraps the JVM in the platform libraries". The inverse conflation also fails today: there is no JRE *installer* to reason about on Java 17/21 — see [[What is the difference between the JVM the JRE and the JDK]] for the nesting.

For the kit that contains this layer, see [[What is the Java Development Kit]]; for the concrete "can it run this" boundary, [[Can you run a compiled Java application with only a JRE installed]]; for the machine at its core, [[What is the JVM]].

> [!tip] Interview answer
> The JRE is the runtime environment: the JVM plus the platform class libraries, enough to execute compiled bytecode but without any development tools. Since Java 11 it is not a separate download anymore — only the JDK ships, and per-app runtimes are built with jlink — so today JRE is mostly a conceptual layer: the part of the JDK that runs your code.
