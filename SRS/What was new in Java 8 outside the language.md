<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #SRS

# What was new in Java 8 outside the language

> [!abstract] Short answer
> **Beyond lambdas and default methods, Java 8 rebuilt the platform's libraries and memory model: the `java.time` API (JSR-310), `CompletableFuture`, Stream and `Optional`, `Spliterator`, `Base64`, Nashorn (JEP 174), repeating and type-use annotations — and in the JVM, Metaspace replacing PermGen plus treeified `HashMap` bins.** The interview point: name the library/runtime half of the release, not only the syntax ([[What major language features arrived in Java 8]]).

## Libraries and runtime

`java.time` replaced mutable `Date`/`Calendar` with immutable ISO-8601 types ([[What is the java.time API and why did it replace Date and Calendar]]). `CompletableFuture` composable async pipelines arrived (`supplyAsync`/`thenCompose`/`allOf`) ([[What is CompletableFuture]]). Streams gave the aggregation vocabulary; `Optional` gave absence a type; `Spliterator` powered parallel traversal ([[What is Spliterator]]). `java.util.Base64` ended the `sun.misc` hack. Nashorn shipped as the ES 5.1 engine with `jjs` ([[What is Nashorn]], [[What is jjs]]) — later removed in 15.

The JVM changed shape too: **PermGen died** and class metadata moved to native-memory Metaspace, sized by `-XX:MaxMetaspaceSize` instead of fixed Perm bounds ([[What is Metaspace and how does it differ from PermGen]]). `HashMap` got treeified bins (JEP 180): a crowded bucket becomes a red-black tree, capping worst-case lookup at O(log n) ([[How does HashMap handle collisions]]). `ConcurrentHashMap` was rewritten to CAS+`synchronized` bins ([[How would you explain ConcurrentHashMap Java 8]]).

```d2
direction: down
lib: "Libraries" {
  shape: rectangle
  time: "java.time (JSR-310)"
  cf: "CompletableFuture"
  so: "Stream, Optional, Spliterator"
  b64: "Base64, Nashorn + jjs"
}
jvm: "JVM / runtime" {
  shape: rectangle
  meta: "Metaspace replaces PermGen"
  tree: "HashMap treeified bins (JEP 180)"
  chm: "ConcurrentHashMap CAS rewrite"
}
```

**Fig. 1.** Java 8's non-language half: an immutable, composable library layer above; memory and concurrency rework inside the JVM below.

```java
import java.time.LocalDate;
import java.util.Base64;
import java.util.concurrent.CompletableFuture;

public class V09_Java8Outside {
    public static void main(String[] args) throws Exception {
        System.out.println("base64: " + Base64.getEncoder().encodeToString("j8".getBytes()));
        System.out.println("completableFuture: " + CompletableFuture.completedFuture("done").get());
        System.out.println("localDate: " + LocalDate.of(2014, 3, 18)); // Java 8 GA date
    }
}
```

**Listing 1.** Verified on JDK 21 (V09_Java8Outside in empirics): `base64: ajg=`, `completableFuture: done`, `localDate: 2014-03-18` — the library additions that are still the everyday API surface a decade later (out/V09_Java8Outside.txt).

> [!warning] "Java 8 = lambdas and streams" is a half-answer
> Two follow-up traps: naming `Date`-related APIs as new (java.time is new; `Date`/`Calendar` are the legacy being replaced), and claiming `parallelStream` was new in 8 without being able to say what runs it — `ForkJoinPool.commonPool` arrived with the release ([[What backs Java parallelStream under the hood]]). Also, Metaspace did **not** make class metadata collectable garbage-free: classloaders still leak, the ceiling just moved to native memory instead of a PermGen OOM — usually.

> [!tip] Interview answer
> **Java 8 outside the language: java.time, CompletableFuture, Streams/Optional/Spliterator, Base64, Nashorn — and in the JVM, Metaspace replacing PermGen plus HashMap treeified bins and the ConcurrentHashMap rewrite.** It is a platform rebuild, not just syntax sugar; the memory and hash-table changes are the follow-up answers interviewers fish for.
