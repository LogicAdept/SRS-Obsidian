<!--
reps: 0
priority: 0
-->
#Java/Versions/14 #SRS

# What is a helpful NullPointerException

> [!abstract] Short answer
> **JEP 358 (Java 14, enabled by default since 15) makes `NullPointerException.getMessage()` return a sentence pinpointing the null value: the exact variable or expression that was null and the operation that failed — "Cannot invoke String.length() because <local2> is null" — instead of plain `null`. The message is computed lazily when first accessed, not at throw time.**

## How the message is built

The JVM records, per bytecode instruction, what dereference failed (field access, array store, method invoke) and which slot; when a message is requested, it renders the program point using class-file debug info for local-variable names. Without `-g` or in synthetic cases you get positional descriptions like `<local2>`; with names you get the variable itself. Cost model: throw time is unchanged — the string is built only when `getMessage()` is called, so hot paths that catch-and-recover do not pay for rendering ([[What was new in Java 14]] placed it in the timeline). The flag `-XX:-ShowCodeDetailsInExceptionMessages` disables it on current builds — useful when message construction would leak data ([[What is profiling in Java]] for the diagnostics context around NPE triage).

```java
public class V52_HelpfulNpe {
    record Order(String id) {}                             // JEP 358 (14), on by default since 15

    public static void main(String[] args) {
        Order known = new Order("o-1");
        Order missing = null;
        try {
            System.out.println(known.id().length() + missing.id().length());
        } catch (NullPointerException e) {
            System.out.println("message: " + e.getMessage());
        }
    }
}
```

**Listing 1.** Verified on JDK 21, two runs (V52_HelpfulNpe in empirics): default — `message: Cannot invoke "V52_HelpfulNpe$Order.id()" because "<local2>" is null`; with `-XX:-ShowCodeDetailsInExceptionMessages` — `message: null` (out/V52_HelpfulNpe.txt).

```d2
direction: right
throw: "NPE thrown at missing.id()\nno message built yet" { style.fill: "#fff3e0"; width: 290; height: 80 }
catch: "handler calls getMessage()" { style.fill: "#e3f2fd"; width: 250; height: 70 }
msg: "JVM renders the program point:\nvariable + operation" { style.fill: "#e8f5e9"; width: 300; height: 80 }
throw -> catch -> msg: ""
```

**Fig. 1.** Lazy message construction: nothing is paid at throw time; rendering happens on first `getMessage()`.

> [!warning] Helpful messages are a debugging surface, not stable output
> Variable names, synthetic slots, and the message format are JVM-version dependent — parsing `getMessage()` in tests or alerting breaks across upgrades. And the message reveals internal variable names in logs you may not want end users to read ([[How would you explain OutOfMemoryError]] sits in the same "diagnostics messages changed shape" bucket).

> [!tip] Interview answer
> **Helpful NPEs — JEP 358, shipped in 14 and default since 15 — make the NullPointerException message name the exact null variable and failed operation, built lazily on first getMessage so throwing stays cheap. I mention the format is debug-info dependent, not API-stable, and the flag ShowCodeDetailsInExceptionMessages can turn it off.**
