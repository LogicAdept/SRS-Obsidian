<!--
reps: 0
priority: 0
-->
#Java/JRE #Java/JDK #SRS

# Can you run a compiled Java application with only a JRE installed?

> [!abstract] Short answer
> Yes — that is exactly what a runtime is for: compiled bytecode (class files or JARs) runs on a JVM with the platform libraries, no compiler needed. The modern caveat: since JDK 11 there is no separate JRE product to install, so "only a JRE" in practice means a `jlink`-built runtime or a container image — and such a minimal runtime can also *lack* pieces (like the compiler) that `java` source-file mode would need.

## Why bytecode is enough

The runtime layer contains the JVM plus the platform class libraries. A compiled application is class files; it contains nothing the compiler is needed for at run time. Given `app.jar` with a `Main-Class` in its manifest, `java -jar app.jar` on a runtime-only install loads the initial class, links and initializes it, and calls `main` — the full startup sequence. Development tools such as `javac`, `jar`, or `javadoc` are never consulted.

```d2
direction: right
jar: "app.jar\ncompiled bytecode + manifest" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
rt: "runtime (JRE layer)\nJVM + class libraries" {
  width: 300
  height: 100
  style.fill: "#e8f5e9"
}
ok: "runs ✓" {
  width: 120
  height: 60
  style.fill: "#e8f5e9"
}
src: "App.java\nsource" {
  width: 170
  height: 70
  style.fill: "#ffebee"
}
need: "compiler missing ✗" {
  width: 230
  height: 60
  style.fill: "#ffebee"
}
jar -> rt
rt -> ok
src -> need: source-file mode
```

**Fig. 1.** Bytecode passes the runtime boundary; source code needs the compiler module, which a minimal runtime may not include.

```java
// On a runtime-only image (JVM + libraries, no JDK tools):
//   java -jar app.jar          ✓ runs — the normal deployment path
//   java -cp classes app.Main  ✓ runs — same mechanism, classpath instead of manifest
//   java App.java              ✗ source-file mode shells out to jdk.compiler,
//                                which a minimal jlink runtime does not carry
```

**Listing 1.** Compiled artifacts run; compiling on the fly is a JDK capability, not a runtime one.

## What changed with modern Java

Two facts reshape this answer. First, there is no JRE *download* anymore: since JDK 11 only the JDK ships, and trimmed runtimes are produced with `jlink` by adding exactly the modules the application needs. Second, those custom runtimes make "can it run" a per-image question: an image built without `jdk.compiler` still runs any bytecode but rejects source-file mode, and an image without the modules your app imports fails at run time with `NoClassDefFoundError` for missing library classes — build the image with the right modules. See [[What is the Java Runtime Environment]] for the layer itself and [[What is the difference between the JVM the JRE and the JDK]] for the nesting.

> [!warning] "Only a JRE" quietly narrows your toolbox
> A runtime-only install also means runtime-only diagnostics: tools like `javac` are absent, and some JDK-side utilities (`jlink`, `jpackage`) make no sense there. Point-in-time diagnostics still work from outside via attach — `jcmd`, `jfr` live in the JDK you attach *from* — but if your production image is a trimmed runtime, verify the diagnostic path before an incident, not during one. Related: [[What is a heap dump and a thread dump]] and [[How do you capture a Java thread dump]].

For what happens once the launcher starts, see [[What happens in the JVM when a Java application starts]]; for the kit that does compile, [[What is the Java Development Kit]].

> [!tip] Interview answer
> Yes — running compiled bytecode is precisely the JRE's job: the JVM plus libraries execute class files with no compiler involved. But on modern Java the answer has a twist: no separate JRE ships anymore, so the runtime is a jlink image or a container. And a minimal image can even refuse java App.java source-file mode, because compiling needs the jdk.compiler module that trimmed runtimes do not carry.
