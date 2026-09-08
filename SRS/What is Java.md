<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Language #SRS

# What is Java?

> [!abstract] Short answer
> **Java is a programming language and a platform.** The language is **general-purpose, concurrent, class-based, object-oriented**, and **strongly and statically typed**, normally compiled to **bytecode**. The platform is the **Java Virtual Machine** plus the **Java SE libraries** that run those `class` files on any host that has a JVM. Designed at **Sun Microsystems** (James Gosling); first appearance **23 May 1995**; **Oracle** has stewarded it since **2010**. Specs go through the **Java Community Process**. Language traits: [[How would you explain distinctive traits of the Java programming language]]. Platform: [[How would you explain distinctive traits of the Java platform]]. JVM: [[What is the JVM]].

## Language, bytecode, platform

**Language.** You write classes (and interfaces); objects are class instances and arrays; instance methods have `this` ([[What does it mean that Java is object oriented]]). Types are known at compile time and constrain values and operators ([[How would you explain static typing in Java]], [[What does strong typing mean in Java]]). Primitives are not objects ([[Why is Java described as not purely object oriented]]).

**Compilation.** `javac` (or another compiler) emits a machine-independent `class` file. A JVM **loads, links, initializes**, and executes that file — optionally compiling further to native code. The same binaries run wherever a compatible JVM exists ([[What is the JVM]], [[Why is Java described as platform independent]]). Tools vs runtime: [[What is the difference between the JVM the JRE and the JDK]]. Entry: [[How would you explain the Java main method entry point]].

**Who specifies and who ships.** The JCP (from **8 December 1998**) is the process for Java **technical specifications**. **OpenJDK** is the open-source implementation of the Java Platform (GPLv2 with the Classpath Exception). Oracle also ships JDK builds from that code under Oracle’s own license. The **Java** trademark is Oracle’s. “Java is GPL” as a blanket sentence is false: the **language spec** is not a GPL program; **OpenJDK** is.

```d2
direction: down
src: ".java language" {
  width: 180
  height: 40
  style.fill: "#e3f2fd"
}
cls: "class file bytecode" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
vm: "JVM + SE libraries" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
src -> cls
cls -> vm
```

**Fig. 1.** “Java” in an interview is usually all three: source language, portable binary, implementing VM and libraries.

```java
class Test {
    public static void main(String[] args) {
        System.out.println("Hello, world.");
    }
}
```

**Listing 1.** Language surface: a class and `main`. After `javac Test.java`, `java Test` is the platform running the `class` file.

Oak began as an embedded language; the specified language was retargeted at the Internet. Today Java SE is used for services, libraries, and desktop/server programs. **Android** apps may be written in the Java *language* but run on Android’s runtime (historically Dalvik / ART), not a Java SE JVM — do not list “Android” as a Java SE deployment.

> [!warning] Language is not the JVM, and OpenJDK is not the trademark
> A Kotlin `class` file is not “Java source.” A JVM without the SE libraries is not the Java SE platform. Oracle owns the name **Java**; OpenJDK is the GPL+CE implementation. Oracle JDK and OpenJDK builds can share a codebase and differ in license.

> [!warning] Dump popularity and “everything is GPL”
> Oracle has called Java widely used (2020: “3 billion devices,” “12 million developers” — marketing counts, not a spec). It is not automatically “the default enterprise stack.” Enterprise APIs (Jakarta EE, Spring) sit **on** Java SE; they are not the language. SQLJ / JDO / a particular HTTP client are libraries, not “what Java is.”

> [!tip] Interview answer
> **Java is both a class-based, statically typed language and the JVM-plus-libraries platform that runs its bytecode.** Sun shipped it in 1995; Oracle stewards it; JCP writes the specs; OpenJDK is the GPL+Classpath implementation. You compile to `class` files so the same program can run on any compatible VM — that is not the same thing as “Android is Java SE.”
