<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# What are the typical problems when upgrading from Java 8 to 17

> [!abstract] Short answer
> **The 8→17 upgrade breaks in four layers: (1) removed modules — Java EE (JAXB/JAX-WS/annotation) and CORBA left the JDK (JEP 320); (2) strong encapsulation — reflection on JDK internals now needs `--add-opens` (JEP 403); (3) toolchain floor — bytecode 61 requires upgraded ASM/CGLIB/byte-buddy, modern Gradle/Kotlin/IDEs; (4) runtime shifts — default GC is G1 (since 9, CMS removed in 14), new language features, changed defaults like UTF-8 (18).** `javax`→`jakarta` rides along with Spring Boot 3/Tomcat 10, but is ecosystem, not JDK ([[What Java EE modules were removed in Java 11]], [[What is strong encapsulation of JDK internals]]).

## The four layers in upgrade order

**Dependencies first:** the old bytecode manipulators crash first — Hibernate's javassist/byte-buddy, Mockito, CGLIB proxies fail with `UnsupportedClassVersionError` or verify errors on class file 61; each needs the version supporting your target JDK. JAXB-dependent libraries (old SOAP/XML stacks) throw `ClassNotFoundException` at runtime, not compile time. **Encapsulation second:** `InaccessibleObjectException` from reflection frameworks lands in production configs as a pile of `--add-opens` flags — each one is a marker for a library upgrade you should make instead ([[What is strong encapsulation of JDK internals]]).

**Toolchain and runtime third/fourth:** build plugins, annotation processors, and agents (old APM/audit agents especially) must support 17; the default collector changed to G1 in 9 with CMS gone since 14 — tuning flags like `-XX:+UseConcMarkSweepGC` no longer start the JVM; `SecurityManager` install fails without the allow flag ([[What was removed or deprecated in Java 17]]). The positives: records, sealed classes, text blocks, switch expressions, and pattern matching are the payoff for surviving the move ([[What was new in Java 21]]).

```d2
direction: down
l1: "1 removed modules\nJAXB/JAX-WS/CORBA (JEP 320)\n-> add dependencies" {
  width: 380
  height: 80
  style.fill: "#ffcdd2"
}
l2: "2 strong encapsulation (JEP 403)\nInaccessibleObjectException\n-> upgrade libs or --add-opens" {
  width: 400
  height: 80
  style.fill: "#fff3e0"
}
l3: "3 toolchain floor\nclass file 61, ASM/byte-buddy,\nGradle/Kotlin/agents" {
  width: 400
  height: 80
  style.fill: "#fff8e1"
}
l4: "4 runtime defaults\nG1 default, CMS gone, UTF-8 (18)\n-> retune, re-verify" {
  width: 400
  height: 80
  style.fill: "#e3f2fd"
}
l1 -> l2 -> l3 -> l4
```

**Fig. 1.** Fix in this order: dependencies, encapsulation, toolchain, runtime defaults — fighting layer 2 with flags before fixing layer 1's libraries produces the classic 20-flag monster JVM command line.

```java
public class V26_Migration {
    public static void main(String[] args) {
        System.out.println("java.class.version: " + System.getProperty("java.class.version"));
        System.out.println("Runtime.version: " + Runtime.version().feature());
    }
}
```

**Listing 1.** Verified on JDK 21 (V26_Migration in empirics): `java.class.version: 65.0`, `Runtime.version: 21` — Java 17 emits class file major **61**, Java 21 emits **65**; a dependency stack that cannot read 61 fails before any of your code runs (out/V26_Migration.txt).

> [!warning] The two most confidently wrong migration claims
> First: "Spring Boot 3 needs Java 17 because of jakarta in the JDK" — `jakarta.*` has never been in the JDK; the JDK removed `javax.*` EE modules back in **11**, and Jakarta is the ecosystem's new namespace; the coupling is Spring Boot 3's requirements, not the JDK's. Second: "just add --add-opens everywhere" — each open re-creates the internals coupling JEP 403 exists to kill and breaks again on later JDKs; the durable fix is upgrading the library. Bonus trap: skipping 9–16 in one hop is fine, but "nothing changed since 8" ignores G1-default (9), CMS removal (14), and the warnings-to-errors escalation of encapsulation ([[What is the Java release cadence since Java 9]]).

> [!tip] Interview answer
> **8→17 breaks by layers: removed EE/CORBA modules (add JAXB dependencies), strong encapsulation (upgrade reflection-heavy libs or --add-opens), bytecode-61 toolchain floor (ASM, byte-buddy, Gradle, agents), and runtime default shifts (G1, CMS gone, later UTF-8).** Jakarta is ecosystem, not JDK. I fix libraries first, use --add-opens surgically, and treat new language features as the payoff.
