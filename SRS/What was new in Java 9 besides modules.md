<!--
reps: 0
priority: 0
-->
#Java/Versions/9 #SRS

# What was new in Java 9 besides modules

> [!abstract] Short answer
> **Besides JPMS, Java 9 shipped the immutable collection factories (`List.of`/`Set.of`/`Map.of`), JShell REPL, private interface methods, compact strings (JEP 254), G1 as the default collector (JEP 248), the Process API update, multi-release JARs (JEP 238), the new version-string scheme (JEP 223), and the HTTP/2 client as an incubator.** The release that took the most criticism ("modules") also changed memory layout, GC defaults, and collection ergonomics ([[What is the Java Platform Module System]]).

## The non-module headlines

Collection factories create small immutable collections in one call — value-based, null-hostile, duplicate-hostile ([[What are the collection factory methods List.of Set.of and Map.of]]). JShell gives an interactive REPL ([[What is jshell]]). Private interface methods let default methods share helpers without leaking API. Compact strings re-landed `String` storage as `byte[]` with a Latin-1/UTF-16 coder flag, cutting memory for Western text roughly by half ([[How is java.lang.String implemented under the hood]]). **G1 became the default GC**, retiring the Parallel-throughput default and foreshadowing CMS's deprecation (9) and removal (14) ([[What is the default garbage collector by Java version]]).

Platform plumbing: JEP 223 made versions single-numbered; multi-release JARs let one artifact ship Java 8 and Java 9+ class variants; `ProcessHandle` turned process management from a platform hack into an API; JEP 260 encapsulated most internal APIs with a transition scheme; the HTTP/2 client incubated here before standardizing in 11 ([[What is the java.net.http HttpClient]]).

```d2
direction: down
api: "APIs" {
  shape: rectangle
  col: "List.of / Set.of / Map.of"
  js: "JShell"
  pim: "private interface methods"
  ph: "ProcessHandle"
}
run: "Runtime / platform" {
  shape: rectangle
  cs: "compact strings (byte[] + coder)"
  g1: "G1 default GC"
  ver: "JEP 223 version scheme"
  mrj: "multi-release JARs"
}
```

**Fig. 1.** Java 9's non-module half: developer-facing APIs above, runtime rework below — G1 default and compact strings are the memory-story pair.

```java
import java.util.List;
import java.util.Map;
import java.util.Set;

public class V12_Java9Besides {
    interface Log {
        default void info(String m) { log("INFO", m); }
        private void log(String lvl, String m) {    // private interface method (Java 9)
            System.out.println(lvl + ": " + m);
        }
    }

    static class C implements Log {}

    public static void main(String[] args) {
        System.out.println("List.of: " + List.of("a", "b"));
        System.out.println("Set.of: " + Set.of(1, 2, 3));
        System.out.println("Map.of: " + Map.of("k", 1));
        new C().info("private interface method");
        System.out.println("pid: " + ProcessHandle.current().pid());
    }
}
```

**Listing 1.** Verified on JDK 21 (V12_Java9Besides in empirics): `List.of: [a, b]`, `Set.of: [3, 2, 1]`, `Map.of: {k=1}`, `INFO: private interface method`, `pid: 20977` — factories, private interface default helpers, and ProcessHandle in one run (out/V12_Java9Besides.txt).

> [!warning] Default-GC and API-maturity traps
> "G1 became default in 9" is correct; claiming CMS was removed in 9 is not — CMS was **deprecated** in 9 (JEP 291) and **removed in 14** (JEP 363). The HTTP client in 9 is an **incubator** module — code against `jdk.incubator.http` does not compile on 11, where it moved to `java.net.http` ([[What is an incubator module]]). And `Set.of` iteration order is unspecified — `[3, 2, 1]` in the listing is not a contract ([[What does Set.of return and what happens with duplicates]]).

> [!tip] Interview answer
> **Java 9 beyond modules: immutable collection factories, JShell, private interface methods, compact strings, G1 as default GC, multi-release JARs, ProcessHandle, and the HTTP client in incubation.** The memorable pair is memory: compact strings halves Latin-1 string storage, G1 rewrites GC defaults — both shape tuning conversations to this day.
