<!--
reps: 0
priority: 0
-->
#Java/Versions/23 #SRS

# What was new in Java 23

> [!abstract] Short answer
> **Java 23 (September 2024) added Markdown doc comments (JEP 467), made generational mode the default for ZGC (474), previewed primitive types in patterns (455) and module import declarations (476), re-previewed gatherers (473) and the Class-File API (466), and deprecated the memory-access methods in `sun.misc.Unsafe` for removal (471). String templates were formally withdrawn here (465).**

## Docs, GC defaults, and an official dead end

Markdown doc comments (467) let javadoc be written with `#`/`##`/lists instead of HTML tags — a documentation DX change with real adoption impact. ZGC generational-by-default (474) completes the arc that started with generational ZGC in 21 (439): the collector now serves short-lived-object workloads the way G1 always did, without a flag; 24 then removed the non-generational mode entirely (490). The withdrawal of string templates (465) is the first time a mainstream preview was pulled back for redesign rather than graduated or left to age — the design lesson (interpolation invites injection the same way SQL concatenation does) is interview gold ([[What were string templates and why were they withdrawn]], [[What is a preview feature in Java]]).

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.List;

public class V36_ZgcGen23 {
    public static void main(String[] args) throws Exception {
        var jdk = System.getProperty("java.home") + "/bin/java";
        var p = new ProcessBuilder(List.of(jdk, "-XX:+ZGenerational", "-version"))
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

**Listing 1.** Verified on JDK 21 (V36_ZgcGen23 in empirics): `exit=0` with the flag accepted — `-XX:+ZGenerational` exists as the opt-in flag of generational ZGC (JEP 439) already in 21; Java 23 (JEP 474) flipped the default so the flag became unnecessary (out/V36_ZgcGen23.txt).

```d2
direction: right
docs: "Markdown doc comments (467)" { style.fill: "#e8f5e9"; width: 240; height: 70 }
zgc: "ZGC generational BY DEFAULT (474)\n(21: opt-in 439 -> 24: non-gen removed 490)" { style.fill: "#e3f2fd"; width: 380; height: 90 }
gone: "String templates WITHDRAWN (465)\nUnsafe memory-access deprecated (471)" { style.fill: "#ffebee"; width: 350; height: 90 }
docs -> zgc -> gone: ""
```

**Fig. 1.** Java 23: documentation ergonomics, a GC default flip, and two legacy paths formally closing.

> [!warning] Withdrawn is not removed
> String templates were never part of any shipped JDK — there is nothing to "upgrade away from". Saying "Java 23 removed string templates" reverses the history: they existed only under preview flags in 21–22 and were pulled before ever finalizing.

> [!tip] Interview answer
> **Java 23 brought Markdown javadoc, made generational mode the ZGC default, and withdrew string templates — the first mainstream preview pulled for redesign rather than shipped. It also previewed primitive patterns and module imports, re-previewed gatherers and the Class-File API, and deprecated the memory-access methods of sun.misc.Unsafe for removal.**
