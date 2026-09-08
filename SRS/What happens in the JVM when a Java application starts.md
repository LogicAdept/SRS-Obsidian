<!--
reps: 0
priority: 0
-->
#Java/JVM #SRS

# What happens in the JVM when a Java application starts?

> [!abstract] Short answer
> The launcher starts a JVM, the JVM loads the initial class you named on the command line, links it, initializes it, and invokes its `public static void main(String[])` — and that single invocation drives all further execution. Everything the application later does happens on threads created from that call.

## The sequence

Per the JVM specification, startup is: create the initial class or interface (the launcher tells the JVM which one — for example the class named on the command line, or the `Main-Class` in a JAR manifest), then **link** it, then **initialize** it, then call the `main` method. The launcher itself describes the same contract: `java` starts the JVM, loads the specified class, and calls its main method, which must be `public static void main(String[])`. When `main` returns (or a `System.exit` fires), the JVM runs shutdown hooks and terminates.

```d2
direction: down
cmd: "java [options] MainClass" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
jvm: "JVM created\n(bootstrap + application loaders ready)" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
load: "load MainClass\n(binary name → class file)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
link: "link\nverify · prepare · resolve" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
init: "initialize\n<clinit> runs" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
main: "invoke main(String[])\nexecution continues from here" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
cmd -> jvm
jvm -> load
load -> link
link -> init
init -> main
```

**Fig. 1.** Startup order fixed by the specification: load, link, initialize, then `main`. Initialization is where static state appears before your first line runs.

```java
public class Main {
    static { System.out.println("static init before main"); }

    public static void main(String[] args) {
        System.out.println("main, args = " + args.length);
    }
}
// java -cp classes Main a b  → loads Main, links, runs <clinit>, then main
```

**Listing 1.** The static initializer executes during the initialization step — before `main` executes.

> [!warning] The class named on the command line is not loaded alone
> Two startup facts trip people up. First, initialization of the initial class runs its static block *before* `main`, so an exception there surfaces as `ExceptionInInitializerError` and the application dies without reaching `main` (see [[How would you explain OutOfMemoryError]] for how JVM-level errors surface). Second, the JVM loads dozens of platform classes before yours — the loader log (`-Xlog:class+load`) shows JDK classes flowing from the shared archive and your classes from the class path. A missing main class, wrong classpath, or a `main` with the wrong signature all fail *at startup*, with different errors.

Termination also belongs to the startup story: after `main` returns, the JVM waits for non-daemon threads, runs shutdown hooks, and exits — see [[What is a JVM shutdown hook]] and [[Can you register a shutdown hook after shutdown has begun]] for that side. For what the engine starts doing once `main` runs, see [[What is the execution engine of the JVM]]; for how the class was found, [[What is the Java classpath]].

> [!tip] Interview answer
> The launcher creates a JVM, which loads the initial class from the command line, links it — verify, prepare, resolve — initializes it, so static initializers run first, and then invokes public static void main(String[]). From that point all execution is driven by main. Startup failures usually mean classpath or main-signature problems, and they happen before your first application statement.
