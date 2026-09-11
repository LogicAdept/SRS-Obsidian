<!--
reps: 0
priority: 0
-->
#Java/Versions/7 #SRS

# What was new in Java 7

> [!abstract] Short answer
> **Java 7 (2011) was the syntax-and-IO refresh: Project Coin small language changes — try-with-resources, the diamond operator, strings in `switch`, multi-catch, binary literals and numeric underscores — plus NIO.2 (`Path`/`Files`/`WatchService`), `ForkJoinPool` with work-stealing, `invokedynamic` bytecode, and G1 as an available collector.** It closed the "Java is verbose" gap that Scala/C# exploited, and laid runtime groundwork (invokedynamic, ForkJoin) that Java 8's lambdas and parallel streams built on.

## The feature map

Project Coin's small changes removed daily boilerplate: try-with-resources auto-closes `AutoCloseable` with proper suppression of secondary exceptions ([[What is try-with-resources]], [[How does the compiler translate try-with-resources]]); the diamond operator `new ArrayList<>()` infers type arguments; a `switch` may select on strings (equality via `equals`, so a `null` selector throws); multi-catch `catch (A | B e)` shrinks duplicated blocks; `0b1010` and `1_000_000` make literals readable. NIO.2 replaced `File` with `Path`/`Files` and added directory walking, attributes, and watch services ([[What notable features does Java NIO offer]]).

Under the hood, `invokedynamic` (JSR 292) gave the JVM a user-programmable call site — the enabling primitive lambdas used later — and `ForkJoinPool` delivered work-stealing parallelism that `parallelStream` rides today ([[What backs Java parallelStream under the hood]]). G1 shipped as an experimental collector and became default in 9 ([[What is the default garbage collector by Java version]]).

```d2
direction: down
coin: "Project Coin (language)" {
  shape: rectangle
  twr: "try-with-resources"
  dia: "diamond operator"
  sw: "strings in switch"
  mc: "multi-catch"
  lit: "binary literals, underscores"
}
lib: "Platform" {
  shape: rectangle
  nio: "NIO.2: Path, Files, WatchService"
  fjp: "ForkJoinPool, work stealing"
  indy: "invokedynamic"
  g1: "G1 collector (experimental)"
}
coin -> lib: "runtime enablers for Java 8"
```

**Fig. 1.** Language ergonomics (Coin) on top, platform machinery below — invokedynamic and ForkJoin are the bridge to Java 8's lambdas and parallel streams.

```java
import java.util.ArrayList;
import java.util.List;

public class V08_Java7 {
    public static void main(String[] args) {
        List<String> diamond = new ArrayList<>();           // diamond operator
        diamond.add("seven");

        String pick = "MONDAY";                              // strings in switch
        switch (pick) {
            case "MONDAY" -> System.out.println("switch string: day start");
            default -> System.out.println("switch string: other");
        }

        try {                                               // multi-catch (Coin)
            throw new IllegalStateException("boom");
        } catch (IllegalStateException | IllegalArgumentException e) {
            System.out.println("multi-catch: " + e.getMessage());
        }

        int mask = 0b1010_1010;                             // binary literal + underscores
        System.out.println("binary literal: " + mask);
        System.out.println("diamond list: " + diamond);
    }
}
```

**Listing 1.** Verified on JDK 21 (V08_Java7 in empirics): `switch string: day start`, `multi-catch: boom`, `binary literal: 170`, `diamond list: [seven]` — every Java 7 snippet still compiles unchanged on modern JDKs (out/V08_Java7.txt).

> [!warning] Misremembered Java 7 claims
> Three traps: the arrow-form `switch` in the listing is modern syntax — Java 7's string `switch` used the classic colon form with fall-through. Strings in `switch` compare with `equals`, so a `null` selector throws `NullPointerException` rather than skipping to `default`. And diamond with anonymous inner classes is **Java 9**, not 7 — `new Runnable() {}` with `<>` fails on 7. Finally, G1 in 7 was experimental: "G1 was the Java 7 default" is a popular falsehood ([[What is the default garbage collector by Java version]]).

> [!tip] Interview answer
> **Java 7 gave the language Coin's ergonomics — try-with-resources, diamond, string switch, multi-catch, better literals — and the platform NIO.2, ForkJoinPool, invokedynamic, and G1.** It is the "closed the verbosity gap, enabled lambdas" release: invokedynamic and work-stealing are what Java 8's streams and lambdas stand on.
