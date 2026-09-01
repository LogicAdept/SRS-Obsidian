<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Versions/16 #SRS

# In which Java version were records standardized?

> [!abstract] Short answer
> **Java 16** (JEP 395, March 2021). They first appeared as a **preview** in Java 14 (JEP 359) and a **second preview** in Java 15 (JEP 384). Preview builds needed `--enable-preview`; from 16 the `record` keyword is a permanent language feature. Record **patterns** in `switch` / `instanceof` are a later feature (Java 21 / JEP 440), not part of that 16 standard.

## Preview is not the same as standard

```d2
direction: right
j14: "Java 14\nJEP 359 preview" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
j15: "Java 15\nJEP 384 second preview" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
j16: "Java 16\nJEP 395 standard" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
j21: "Java 21\nJEP 440 record patterns" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
j14 -> j15
j15 -> j16
j16 -> j21: "separate JEPs"
```

**Fig. 1.** Ask “when could I write `record` in production without preview flags?” — **16**. “When did the syntax first exist?” — 14.

JEP 395 status is Closed / Delivered, **Release 16**. Its History section: proposed by JEP 359 in JDK 14; refined by JEP 384 in JDK 15; finalized in JDK 16. `java.lang.Record` is **since 16**. The class-file `Record` attribute is major version 60.0, also Java 16 ([[How does the JVM represent a Java record]]).

Between previews the language moved. JEP 384 (second preview) changed canonical-constructor access to match the record class (no longer forced `public`), allowed local records, and forbade assigning instance fields in a compact constructor. JEP 395’s last language tweak: an inner class may declare a nested record (implicitly static). Treat 14/15 code as **recompile on 16**, not as a binary you keep.

```java
public record User(String name, int age, String email) {}

User user = new User("John", 25, "john@example.com");
user.name();  // accessor is name(), not getName()
```

**Listing 1.** This declaration is legal as a preview on 14/15 and as standard Java from 16. Production interviews mean the **16** line unless they ask about preview.

```text
# JDK 14 / 15 only — not needed from 16
javac --release 15 --enable-preview User.java
java  --enable-preview User
```

**Listing 2.** Preview class files use minor version 65535 and run only on that JDK with preview enabled. “Java 14+” on a résumé is not “shipped on 14.”

Record **patterns** (`case User(String name, int age, String email)`) need Java 21 — [[How do records work with pattern matching in switch]]. That is JEP 440, not JEP 395.

Records are a language construct with JVM metadata, not Lombok rewriting a class into JavaBeans getters. They are also **not** a new VM type and **not** an `ACC_RECORD` access-flag bit — see the JVM card and [[What is the difference between a Java record and Lombok Value]].

> [!warning] “Java 14+” is the preview start, not the standard
> Vault titles like [[What is record (Java 14+)]] mix first appearance with “safe to use.” If the interviewer says “from which version are records in the language,” answer **16**. Mention 14/15 only as preview, with `--enable-preview`.

> [!warning] Record patterns are Java 21
> `record Point(int x, int y)` is 16. `if (p instanceof Point(int x, int y))` / `switch` record patterns are 21. Do not collapse both into “records came in 21” or “patterns came in 16.”

> [!tip] Interview answer
> **Standardized in Java 16 (JEP 395).** Preview in 14 (JEP 359) and 15 (JEP 384) required `--enable-preview`; do not treat “Java 14+” as the production answer. Record patterns in `switch` are a separate Java 21 feature.
