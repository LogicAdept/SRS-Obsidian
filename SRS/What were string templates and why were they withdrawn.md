<!--
reps: 0
priority: 0
-->
#Java/Versions/23 #SRS

# What were string templates and why were they withdrawn

> [!abstract] Short answer
> **String templates were previewed in Java 21 (JEP 430) and again in 22 (459) as inline interpolation with pluggable processors — `STR."user \{name} scored \{score}"` — and were withdrawn in Java 23 (JEP 465) before ever finalizing: the designers concluded the one-line interpolation syntax was too broadly enabling for a feature meant to encourage safe string composition. No replacement has shipped as of Java 26.**

## What they looked like and why they died

A template expression combined a processor and a template: `STR."..."` performed plain interpolation, `FMT."..."` added format specifiers, and you could write custom processors (JSON escaping, SQL binding). Values embedded via `\{expr}` were passed as structured data to the processor, not naively stringified — the design aimed at injection-safe composition. The withdrawal note in 465 is explicit that previewing shipped the wrong granularity: general-purpose interpolation in the language core invites the very concatenation-into-query bugs the feature was meant to fix, and the team chose to withdraw rather than lock in a flawed shape. The classic interview upgrade: saying "Java 23 removed string templates" is wrong — they were never finalized anywhere; nothing was removed because nothing shipped ([[What is a preview feature in Java]]).

```java
import java.text.MessageFormat;

public class V49_StringTemplates {
    public static void main(String[] args) {
        String user = "ada";
        int score = 91;
        System.out.println("concat: " + user + " scored " + score);
        System.out.println("format: " + "%s scored %d".formatted(user, score));
        System.out.println("msgfmt: " + MessageFormat.format("{0} scored {1}", user, score));
        // JEP 430 (21 preview) / 459 (22 2nd preview) would have been: STR."\{user} scored \{score}"
        // JEP 465 (23): withdrawn for redesign; no replacement shipped as of JDK 26.
    }
}
```

**Listing 1.** Verified on JDK 21 (V49_StringTemplates in empirics): `concat: ada scored 91`, `format: ada scored 91`, `msgfmt: ada scored 91` (out/V49_StringTemplates.txt) — the composition tools that remain after the withdrawal.

```d2
direction: right
p21: "Java 21\nPREVIEW (JEP 430)" { style.fill: "#fff3e0"; width: 180; height: 70 }
p22: "Java 22\n2nd PREVIEW (459)" { style.fill: "#fff3e0"; width: 180; height: 70 }
w23: "Java 23\nWITHDRAWN (465)" { style.fill: "#ffebee"; width: 180; height: 70 }
now: "as of Java 26:\nnothing shipped" { style.fill: "#e8f5e9"; width: 200; height: 70 }
p21 -> p22 -> w23 -> now: ""
```

**Fig. 1.** The full lifecycle of string templates: two previews, a formal withdrawal, and no shipped replacement.

> [!warning] Two popular lies about string templates
> First, "string templates are in Java 21" — they were preview-only and needed `--enable-preview`; code using `STR."..."` does not compile on any stock 21. Second, "Java 23 removed them" — removal implies prior finalization; the JEP was withdrawn for redesign, and as of 26 no successor syntax or API has landed ([[What was new in Java 23]]).

> [!tip] Interview answer
> **String templates were an interpolation feature with pluggable processors — previewed in 21 and 22, then withdrawn in 23 by JEP 465 before ever finalizing. The stated reason: one-line interpolation was too permissive for the goal of safe string composition, and the team preferred a redesign over locking in the wrong model. Today the tools are still formatted, MessageFormat, and concatenation.**
