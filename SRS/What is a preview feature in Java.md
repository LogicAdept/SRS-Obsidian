<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What is a preview feature in Java

> [!abstract] Short answer
> **A preview feature is a complete-but-impermanent language or API change shipped in a GA JDK so developers can test it before the design is frozen.** It requires the `--enable-preview` flag (matched compiler and runtime), is explicitly **not** a final part of the platform, may change between preview rounds — and may be withdrawn entirely: string templates previewed in 21 and 22 and never finalized. Finalized examples: sealed classes (17), pattern `switch` (21). Still previewing: structured concurrency (21–25).

## Mechanics and lifecycle

Language previews ship behind `--enable-preview` on both `javac` (with `--source`/`--release`) and `java`; class files carry a preview flag tied to that exact feature release, so preview bytecode compiled on 21 does not run on 22. API previews are tagged `@Deprecated(forRemoval=false)`-style **`forRemoval` preview packages** — `StructuredTaskScope` lived in `jdk.incubator.concurrent` as an incubator before becoming a preview API in 21. Each preview round (JEP per round) can adjust the design based on feedback; after one or more rounds the JEP either finalizes the feature or withdraws it.

Verified examples an interviewer may probe: `switch` expressions previewed in 12–13, finalized **14**; records previewed 14–15, finalized **16**; sealed classes previewed 15–16, finalized **17**; pattern `switch` previewed 17–20, finalized **21**; record patterns previewed 19–20, finalized **21**; string templates (430) previewed **21**, second preview (459) **22**, then **withdrawn** — never finalized ([[What are switch expressions]], [[How would you explain Java 17 21]]).

```d2
direction: right
p1: "preview 1\n(sealed: 15)" {
  width: 170
  height: 55
}
p2: "preview 2\n(sealed: 16)" {
  width: 170
  height: 55
}
fin: "final\n(sealed: 17)" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
wd: "withdrawn\n(string templates: 21–22)" {
  width: 240
  height: 65
  style.fill: "#ffcdd2"
}
p1 -> p2 -> fin
p2 -> wd
```

**Fig. 1.** Two exits from preview: finalization after one or more rounds, or withdrawal. Sealed classes needed two rounds; string templates needed zero finals — they were pulled.

```java
import java.util.concurrent.StructuredTaskScope;
import java.util.concurrent.StructuredTaskScope.Subtask;

public class V05_Preview {
    public static void main(String[] args) throws Exception {
        try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
            Subtask<String> user = scope.fork(() -> "ada");
            Subtask<Integer> karma = scope.fork(() -> 42);
            scope.join().throwIfFailed();
            System.out.println("user=" + user.get() + " karma=" + karma.get());
        }
    }
}
```

**Listing 1.** Verified on JDK 21 with `javac --release 21 --enable-preview` and `java --enable-preview` (V05_Preview in empirics): `user=ada karma=42`. `StructuredTaskScope` is a preview API in 21 — the run fails to compile without `--enable-preview`, which is the whole point of the mechanism (out/V05_Preview.txt).

> [!warning] Preview does not mean "beta quality you may ship"
> The trap directions: first, preview features **cannot go to production** on supported builds — vendors explicitly do not support them, and the bytecode is version-locked. Second, citing a preview as final is the classic interview tell — "Java 21 string templates" (withdrawn) or "Java 17 pattern switch" (still preview there) are both wrong ([[What was new in Java 21]]). Third, do not confuse preview with incubator: preview is language/API shape-testing with a flag; incubator is a whole module for API experiments ([[What is an incubator module]]).

> [!tip] Interview answer
> **Preview features are complete, flag-gated, non-final changes — compiled and run with `--enable-preview`, version-locked, unsupported in production.** They iterate across releases and end either final (sealed 17, pattern switch 21) or withdrawn (string templates 21–22). I test-drive them on the trains but never ship them.
