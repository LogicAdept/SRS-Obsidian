<!--
reps: 0
priority: 0
-->
#Java/Versions/14 #SRS

# What was new in Java 14

> [!abstract] Short answer
> **Java 14 (March 2020) finalized switch expressions (JEP 361), shipped helpful NullPointerException messages (358), previewed records (359) and instanceof patterns (305), re-previewed text blocks (368), removed the CMS collector (363), added JFR event streaming (349), and removed Pack200 (367). It also deprecated the Parallel-Scavenge + SerialOld combination (366) and the Solaris/SPARC ports (362).**

## The first "modern Java" shape appears

Switch expressions went final here: arrow labels, `yield`, exhaustiveness for enum selectors — the template for everything pattern-based that followed ([[What are switch expressions]]). Helpful NPEs (358) changed `NullPointerException.getMessage()` from `null` to a sentence naming the exact null variable and failed operation — enabled by default from 15 ([[What is a helpful NullPointerException]]). Records and instanceof patterns previewed in 14 and standardized in 16 — version-precise wording matters: "records arrived in 14" is a preview claim, not a final one ([[In which Java version were records standardized]]). JFR event streaming (349) let the same process read its own recording live instead of parsing a dump afterward — the foundation for in-app telemetry loops.

On the removal side, CMS — deprecated in 9 (JEP 291) — was deleted outright (363), and Pack200 (367) went with it. The release set the cleanup rhythm the removal cards follow ([[What was removed or deprecated in Java 17]]).

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;

public class V30_CmsRemoved14 {
    public static void main(String[] args) throws Exception {
        var jdk = System.getProperty("java.home") + "/bin/java";
        var p = new ProcessBuilder(List.of(jdk, "-XX:+UseConcMarkSweepGC", "-version"))
                .redirectErrorStream(true).start();
        String out;
        try (var r = new BufferedReader(new InputStreamReader(p.getInputStream()))) {
            out = r.lines().collect(java.util.stream.Collectors.joining(" | "));
        }
        System.out.println("exit=" + p.waitFor());
        System.out.println("output=" + out);
    }
}
```

**Listing 1.** Verified on JDK 21 (V30_CmsRemoved14 in empirics): `exit=1`, `output=Unrecognized VM option 'UseConcMarkSweepGC' | Error: Could not create the Java Virtual Machine. | Error: A fatal exception has occurred. Program will exit.` (out/V30_CmsRemoved14.txt) — a JVM built after 14 refuses the CMS flag outright.

```d2
direction: right
final: "switch expressions FINAL (361)\nHelpful NPE (358)" { style.fill: "#e8f5e9"; width: 280; height: 80 }
prev: "records PREVIEW (359)\ninstanceof patterns PREVIEW (305)\ntext blocks 2nd preview (368)" { style.fill: "#fff3e0"; width: 310; height: 100 }
gone: "CMS REMOVED (363)\nPack200 REMOVED (367)\nJFR event streaming (349)" { style.fill: "#ffebee"; width: 290; height: 100 }
final -> prev -> gone: ""
```

**Fig. 1.** Java 14: two finals, three previews, and the first big GC deletion of the six-month era.

> [!warning] Records did not "arrive" in 14
> Records and instanceof patterns previewed in 14 — that flag needs `--enable-preview` and could still change; both finalized in 16 ([[In which Java version were records standardized]], [[What is the instanceof operator for in Java]]). Lumping preview into final is the most common version-history lie in interviews.

> [!tip] Interview answer
> **Java 14 finalized switch expressions, shipped helpful NPE messages, and previewed records and instanceof patterns — both final in 16. It removed CMS (deprecated in 9) and Pack200, added JFR event streaming for in-process recording reads, and deprecated the PS+SerialOld combo. It is the release where the modern pattern-matching line clearly starts.**
