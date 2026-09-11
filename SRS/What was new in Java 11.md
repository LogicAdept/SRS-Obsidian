<!--
reps: 0
priority: 0
-->
#Java/Versions/11 #SRS

# What was new in Java 11

> [!abstract] Short answer
> **Java 11 (September 2018, first LTS of the six-month era) standardized the HTTP client (`java.net.http`, JEP 321), added `String.isBlank/strip/lines/repeat`, `Files.readString/writeString`, `var` in lambda parameters (JEP 323), single-file source launch (JEP 330), Epsilon GC, ZGC experimental, open Flight Recorder, TLS 1.3 (JEP 332) — and removed the Java EE and CORBA modules (JEP 320).** It is the release whose removals, not additions, shaped migrations for years ([[What Java EE modules were removed in Java 11]]).

## The feature inventory

API ergonomics: `String` gained `isBlank`, `strip` (Unicode-aware vs `trim`'s `<= U+0020`), `lines`, `repeat`; `Files.readString`/`writeString` replaced reader-loop boilerplate. The **HTTP client** supports HTTP/2, async `CompletableFuture` sends, and WebSockets ([[What is the java.net.http HttpClient]]). `var` extends to lambda parameters — only so annotations can be written, and only uniformly ([[What is the var keyword in Java]]). JEP 330 runs `java Hello.java` without javac — scripts and examples get lighter.

Runtime: **Epsilon** (JEP 318) is the no-op GC for benchmarking and short-lived jobs; **ZGC** (JEP 333) arrived experimental with sub-millisecond pause targets; **Flight Recorder** (JEP 328) was open-sourced into the JDK; TLS 1.3 landed; nest-based access control (JEP 181) let nested classes share private members without synthetic bridges. Removals: Java EE (JAXB, JAX-WS, `javax.annotation`, activation, transaction) and CORBA left the JDK — the single biggest 8→11 break ([[What are the typical problems when upgrading from Java 8 to 17]]).

```d2
direction: down
api: "APIs" {
  shape: rectangle
  http: "java.net.http HttpClient (JEP 321)"
  str: "String isBlank/strip/lines/repeat"
  io: "Files.readString/writeString"
  var: "var in lambda params"
}
rt: "Runtime / platform" {
  shape: rectangle
  zgc: "ZGC experimental, Epsilon"
  tls: "TLS 1.3"
  jfr: "Flight Recorder open-sourced"
  j330: "launch single-file source"
}
rem: "Removals (JEP 320)\nJava EE: JAXB, JAX-WS, javax.annotation\nCORBA" {
  width: 380
  height: 80
  style.fill: "#ffcdd2"
}
```

**Fig. 1.** Java 11 in three shelves: new APIs, runtime investments (ZGC, JFR, TLS 1.3), and the removals that dominate upgrade stories.

```java
import java.nio.file.Files;
import java.nio.file.Path;

public class V15_Java11 {
    public static void main(String[] args) throws Exception {
        System.out.println("isBlank: " + "   ".isBlank());
        System.out.println("repeat: " + "ab".repeat(3));
        System.out.println("strip: '" + "  hi  ".strip() + "'");
        "line1\nline2".lines().forEach(l -> System.out.println("lines: " + l));

        Path p = Files.createTempFile("j11", ".txt");
        Files.writeString(p, "http client & TLS 1.3");
        System.out.println("readString: " + Files.readString(p));
    }
}
```

**Listing 1.** Verified on JDK 21 (V15_Java11 in empirics): `isBlank: true`, `repeat: ababab`, `strip: 'hi'`, `lines: line1`, `lines: line2`, `readString: http client & TLS 1.3` — the string/file ergonomics that land in code review instantly (out/V15_Java11.txt).

> [!warning] Java 11 is remembered for what it took away
> The traps: "JAXB is in the JDK" died in 11 — Spring Boot 2 apps on 11 needed explicit `jaxb-api` dependencies, and the failure is a runtime `ClassNotFoundException`, not a compile error ([[What Java EE modules were removed in Java 11]]). "Oracle JDK 11 is free like 8" was false from 8u211/11 GA on — the OTN license change is why Temurin-class builds filled the gap ([[What is the difference between Oracle JDK and OpenJDK]]). And `var` in lambdas is **all-or-nothing per lambda** — `(var x, y)` does not compile.

> [!tip] Interview answer
> **Java 11 is the first LTS of the new cadence: standard HTTP client, String/Files ergonomics, var in lambda params, single-file launch, Epsilon and experimental ZGC, open JFR, TLS 1.3 — and the removal of Java EE and CORBA modules.** The removals are the migration story; the HTTP client is the API story.
