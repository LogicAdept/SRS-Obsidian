<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/JDK #Java/JRE #SRS

# What is the difference between the JVM the JRE and the JDK?

> [!abstract] Short answer
> They nest: the JVM executes bytecode; the JRE is that JVM plus the class libraries needed to *run* a program; the JDK is the JRE plus development tools — the compiler `javac`, `jar`, `javadoc`, `jcmd`, `jlink` — needed to *build* one. Since JDK 11, Oracle ships only the JDK and no longer offers a separate JRE download.

## The three layers

The **JVM** is the engine: it loads class files, manages memory, and executes bytecode. By itself it is not enough to run a real program, because `java.lang.String`, collections, and IO all live in the class libraries. The **JRE** (Java Runtime Environment) packages the JVM with those platform libraries — exactly what a machine needs to *run* compiled Java, and nothing to compile it. The **JDK** (Java Development Kit) adds the toolchain on top of the JRE: the `javac` compiler, the `jar` archiver, `javadoc`, the `jdb` debugger, diagnostic and packaging tools.

```d2
direction: right
jdk: "JDK\ndevelopment tools\njavac · jar · javadoc · jcmd · jlink" {
  width: 300
  height: 120
  style.fill: "#e3f2fd"
}
jre: "JRE\nplatform class libraries" {
  width: 260
  height: 110
  style.fill: "#fff3e0"
}
jvm: "JVM\nexecutes bytecode" {
  width: 200
  height: 100
  style.fill: "#e8f5e9"
}
jdk -> jre
jre -> jvm
```

**Fig. 1.** Containment, not comparison: every JRE contains a JVM, and every JDK contains a JRE. A class file is produced by the JDK layer and consumed by the JVM layer.

## Who needs what

A server that only *runs* a compiled application needs the runtime layer, not the compiler. A developer writing code needs the JDK, because sources must be compiled by `javac` before any JVM can execute them. The JVM/JRE/JDK distinction is about capability, not version: all three exist for the same release and execute the same class files.

```java
// What a JDK adds to the runtime (a real toolchain, all in the same image):
//   javac App.java            compile source into class files
//   jar --create --file app.jar -C classes .   package compiled classes
//   java -jar app.jar         run — this part needs only the runtime layer
//   jlink --add-modules java.base --output runtime   build a custom runtime
```

**Listing 1.** Compile-and-package steps require the JDK; the final `java -jar` runs on any JRE.

> [!warning] "Install the JRE" is outdated advice for modern Java
> Since JDK 11 the separate JRE and Server JRE downloads are gone — only the JDK is offered, and custom runtimes are built with `jlink` from modules. On Java 8 this answer was "download the JRE for servers"; on Java 17/21 the practical answer is "install a JDK, or ship a `jlink`/container runtime". Quoting the Java 8 setup in a modern interview is a red flag.

The classic trap inside the trio is the compiler: `java` runs bytecode while `javac` produces it, and mixing them up makes "run with only a JRE" impossible to answer. See [[Can you run a compiled Java application with only a JRE installed]] for that boundary, [[What is the Java Development Kit]] for the tool list, and [[What is the Java Runtime Environment]] for what exactly the runtime layer contains.

> [!tip] Interview answer
> The JVM is the virtual machine that executes bytecode. The JRE is the JVM plus the class libraries — everything needed to run a compiled application. The JDK is the JRE plus development tools such as javac, jar, and jlink — everything needed to develop one. They nest inside each other, and since Java 11 there is no separate JRE distribution: only the JDK, with jlink for building custom runtimes.
