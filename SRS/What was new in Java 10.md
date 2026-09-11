<!--
reps: 0
priority: 0
-->
#Java/Versions/10 #SRS

# What was new in Java 10

> [!abstract] Short answer
> **Java 10 (March 2018, first six-month feature release) is small but structural: `var` local-variable type inference (JEP 286), the unified GC interface (JEP 304), parallel full GC for G1 (JEP 307), Application Class-Data Sharing (JEP 310), thread-local handshakes (JEP 312), an experimental Java-based JIT Graal (JEP 317), and time-based release versioning (JEP 322), plus API odds like `Optional.orElseThrow()`, `Collectors.toUnmodifiableList/Set/Map`, container awareness, and the deprecation of `Optional.get`.** [[What is the var keyword in Java]] is the only syntax change in the whole release.

## The one syntax change, the runtime shifts

`var` infers the static type of a local variable from its standalone initializer; it is a reserved type name, not a keyword, and it stops at locals — fields, parameters, and return types keep explicit types. The JVM half of the release matters for tuning interviews: **JEP 304** cleaned the collector source layout so alternate collectors plug in without HotSpot surgery; **JEP 307** made G1 full GCs parallel — before 10, a G1 full GC was single-threaded and could stall a busy heap for seconds; **JEP 310** lets an application record its own class metadata into a shared archive (`-XX:ArchiveClassesAtExit`, `-XX:SharedArchiveFile=`) to cut startup and footprint; **JEP 312** added per-thread safepoint callbacks (handshakes) — machinery later collectors and biased-locking revocation lean on.

Container awareness landed here too (not a JEP): `UseContainerSupport` on by default means the JVM reads cgroup limits, so the default heap follows the container budget and `-XX:MaxRAMPercentage` becomes the tuning knob — backported to 8u191, which is why "8 in containers" changed mid-life.

```java
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

public class V27_Java10 {
    public static void main(String[] args) {
        var names = List.of("ada", "grace", "linus");      // JEP 286: element type inferred
        var filtered = names.stream()
                .filter(n -> n.length() > 3)
                .collect(Collectors.toUnmodifiableList()); // new JDK 10 collector
        System.out.println(filtered + " class=" + filtered.getClass().getSimpleName());
        Optional<String> empty = Optional.empty();
        try { empty.orElseThrow(); }                       // JDK 10 zero-arg alias
        catch (java.util.NoSuchElementException e) {
            System.out.println("orElseThrow() -> NoSuchElementException");
        }
        var d = LocalDate.of(2018, 3, 20);                 // JDK 10 GA date
        System.out.println("inferred " + d + " as " + d.getClass().getName());
    }
}
```

**Listing 1.** Verified on JDK 21 (V27_Java10 in empirics): `[grace, linus] class=List12`, `orElseThrow() -> NoSuchElementException`, `inferred 2018-03-20 as java.time.LocalDate` (out/V27_Java10.txt).

```d2
direction: right
lang: "var (JEP 286)" { width: 150; height: 70 }
gc: "GC interface +\nparallel G1 full GC\n(304, 307)" { width: 200; height: 90 }
cds: "AppCDS\n(310)" { width: 120; height: 90 }
hands: "Handshakes\n(312)" { width: 140; height: 90 }
ver: "Time-based\nversioning (322)" { width: 180; height: 90 }
lang -> gc -> cds -> hands -> ver: ""
```

**Fig. 1.** Java 10 in five pillars: one language change, the rest runtime and process plumbing that later releases build on.

> [!warning] A feature release, not a support line
> Java 10 stopped receiving updates when 11 shipped — production answers never name 10 as a support target. And since 10, `Optional.get()` is deprecated: reaching for it in new code is a smell ([[What changed in Optional after Java 8]]).

> [!tip] Interview answer
> **Java 10 is "var plus plumbing": `var` (286) is the only language change; the GC interface (304) and parallel G1 full GC (307) made collectors pluggable and faster; AppCDS (310) cut startup; handshakes (312) made per-thread safepoint callbacks possible; and time-based versioning (322) started the numbering we still use.** I also mention container awareness landing here, backported to 8u191.
