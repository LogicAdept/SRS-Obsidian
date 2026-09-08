<!--
reps: 0
priority: 0
-->
#Java/JVM #Java/Language #SRS

# What is Java?

> [!abstract] Short answer
> Java is two things sold under one name: a statically typed, class-based, object-oriented programming language, and the platform it targets — the JVM with its runtime libraries. The language was developed at Sun Microsystems and released in 1995; Sun's core assets went to Oracle in 2010, and the reference implementation, OpenJDK, is developed in the open under the GNU GPL with the Classpath Exception.

## Language and platform

The language half is the syntax you write: classes, interfaces, records, generics, a compile-time type system, and a standard library API. The platform half is what executes it: `javac` compiles `.java` sources into `.class` bytecode, and a JVM — HotSpot in OpenJDK builds — loads and runs that bytecode with managed memory and JIT compilation. Keeping the two apart answers most "what is Java" follow-ups: the language defines what programs may express; the platform defines how they run and how fast.

```d2
direction: right
lang: "Java the language\nsyntax · typing · javac compiles it" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
cf: "class files\nbytecode" {
  width: 190
  height: 80
  style.fill: "#fff3e0"
}
plat: "Java the platform\nJVM · GC · JIT · standard libraries" {
  width: 320
  height: 90
  style.fill: "#e8f5e9"
}
lang -> cf
cf -> plat
```

**Fig. 1.** Java as language plus platform: sources compile to bytecode, and the platform runs the bytecode.

## Governance and releases

The platform moves on a predictable six-month release train, with long-term-support (LTS) releases — 8, 11, 17, 21 — chosen for production lifetimes. Language and library changes go through the JEP process and, where a language standard is needed, the JCP. OpenJDK is the canonical implementation; vendors build certified distributions from it, which is why "Java" can mean a version, a distribution, or the platform as a whole.

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Java " + System.getProperty("java.version")
            + " on " + System.getProperty("java.vm.name"));
    }
}
// javac Hello.java && java Hello
// → Java 21.0.12 on OpenJDK 64-Bit Server VM
```

**Listing 1.** One artifact, both halves: the code you wrote (language) executed by an implementation (platform).

> [!warning] "Java" gets blamed for things that belong to other layers
> Three mix-ups recur in interviews. "Java is slow" describes a 1990s interpreter story, not the platform — today's throughput comes from JIT-compiled native code; see [[Is Java a compiled or interpreted language]]. "Java is verbose" is often a statement about pre-8 idiom, while the language ships records, lambdas, and pattern matching in modern releases. And JavaScript has nothing to do with Java — the similar name is a 1995 marketing decision, not a technical relationship. Judge each claim against the version you actually run; see [[How would you explain distinctive traits of the Java platform]].

For the machine under the platform, see [[What is the JVM]]; for why one binary runs everywhere, [[Why is Java described as platform independent]]; for when Java is a sensible choice, [[Why should you use Java]].

> [!tip] Interview answer
> Java is a statically typed, object-oriented programming language plus the platform that runs it. Sun Microsystems released it in 1995, Oracle owns it now, and OpenJDK is the open-source reference implementation. The language compiles to bytecode; the JVM executes it with garbage collection and JIT compilation — and the two halves move on a six-month release train with LTS milestones.
