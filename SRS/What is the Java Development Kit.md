<!--
reps: 0
priority: 0
-->
#Java/JDK #SRS

# What is the Java Development Kit?

> [!abstract] Short answer
> The JDK is the complete development kit for Java: a compiler (`javac`), the toolchain around it (`jar`, `javadoc`, `jdb`, `jcmd`, `jlink`, `jpackage`), and a full runtime — JVM plus class libraries — to execute what you build. Since JDK 11 it is also the only thing Oracle ships: there is no separate JRE download anymore.

## What is inside

The JDK is organized as a runtime plus development tools on top. The runtime half is a JVM and the platform libraries — everything needed to run compiled bytecode. The tools half converts sources into artifacts: `javac` compiles `.java` to class files, `jar` packages them (with a manifest), `javadoc` generates API documentation from source comments, `jdb` debugs, `jcmd` and `jfr` diagnose and profile a running JVM, `jlink` assembles custom runtimes from modules, and `jpackage` produces installers. One JDK install therefore both builds and runs applications.

```d2
direction: right
src: "App.java" {
  width: 160
  height: 70
  style.fill: "#e3f2fd"
}
tools: "JDK tools\njavac · jar · javadoc · jlink" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
rt: "runtime layer\nJVM + class libraries" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
diag: "diagnostics\njcmd · jfr · jdb" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
out: "runnable app" {
  width: 170
  height: 60
  style.fill: "#e8f5e9"
}
src -> tools
tools -> out
out -> rt
rt -> diag: attach
```

**Fig. 1.** Tools turn sources into artifacts; the runtime layer executes them; diagnostic tools attach to the running JVM.

```java
// The daily tool loop, all from one JDK install:
//   javac -d classes src/App.java            compile sources to class files
//   jar --create --file app.jar -C classes . package them
//   java -jar app.jar                        run (runtime layer)
//   jcmd <pid> Thread.print                  diagnose the running process
//   jlink --add-modules java.base --output rt  build a minimal custom runtime
```

**Listing 1.** Compile, package, run, diagnose, shrink — five commands that outline the JDK's job.

## One product since Java 11

Before JDK 11, Oracle shipped the JDK for development and separate JRE/Server JRE downloads for deployment. That ended with JDK 11: the release notes state that only the JDK is offered, and custom runtimes are built with `jlink` from modules instead of installing a one-size JRE. The conceptual JRE layer (JVM plus libraries) still exists inside the kit — the term describes a component, not a downloadable product.

> [!warning] "JDK vs JRE" as a deployment decision is obsolete
> Answering "servers get the JRE, developers get the JDK" dates you to Java 8. On modern releases a server image is either a full JDK, a `jlink`-built runtime with just the modules the app needs, or a container with exactly that. Also do not confuse the kit with a distribution: OpenJDK builds, Oracle JDK, Temurin, and Corretto are all JDKs built from the same source — see [[What is the difference between the JVM the JRE and the JDK]].

For what the runtime layer contains, see [[What is the Java Runtime Environment]]; for the search path the launcher tools share, [[What is the Java classpath]]; for the diagnostics half, [[What is profiling in Java]].

> [!tip] Interview answer
> The JDK is the development kit: javac, jar, javadoc, jlink, jpackage, plus diagnostic tools like jcmd and jfr, all sitting on top of a complete runtime — JVM and class libraries. Since Java 11 it is the only distribution: no separate JRE download, and custom runtimes are assembled with jlink. So one install builds, runs, and diagnoses Java applications.
