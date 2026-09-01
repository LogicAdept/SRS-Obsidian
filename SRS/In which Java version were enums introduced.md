<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Versions/5 #SRS

# In which Java version were enums introduced?

> [!abstract] Short answer
> **Java 5 — JDK 1.5 / J2SE 5.0 (“Tiger”), 2004.** `java.lang.Enum` is documented `since 1.5`. JSR 201 added enumerations (with autoboxing, enhanced `for`, and static import) as language support for the typesafe-enumeration pattern. That is not the same date as **local** enums, which arrived in Java 16.

## 1.5 the platform, 5 the product name

Sun shipped the feature in J2SE 1.5. Marketing called that release Java 5 / J2SE 5.0. Interview answers that say “1.5” and “Java 5” are the same platform. `Enum`, `EnumSet`, and `EnumMap` are all `since 1.5`.

JSR 201’s enum work is a **syntax for enumerated types**: a class that defines a fixed set of named instances, not a bag of `int` literals. Each constant is an implicit `public static final` field. The type can have constructors, fields, methods, implement interfaces, and be used in `switch` ([[How would you explain Java enum types]], [[Can you use a Java enum in a switch]]).

```d2
direction: down
v5: "Java 5 / JDK 1.5\nenum types, Enum, EnumSet, EnumMap" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
v16: "Java 16\nlocal enum classes in a method" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}

v5 -> v16
```

**Fig. 1.** The type is a Java 5 language feature. Where you may *declare* one grew later ([[Can you declare a Java enum inside a method]]).

```java
enum Coin { PENNY, NICKEL, DIME, QUARTER }
```

**Listing 1.** Legal from Java 5. Before that, the usual substitute was `public static final int` (or `String`) constants — the pattern JSR 201 turned into language syntax ([[What is the advantage of a Java enum over int and String constant patterns]]).

Pre-5 code could still *simulate* a typesafe enum with a class and a private constructor. The 1.5 feature is that the language and `java.lang.Enum` guarantee the instance set, `values()` / `valueOf`, and serialization-by-name.

> [!warning] “1.5” and “Java 5” are the same release
> After 5, product numbers and `java.specification.version` lined up (6, 7, …). Enums are the last big language add from the `1.x` numbering. Saying “Java 1.5 only, not 5” is a naming quibble, not two features.

> [!warning] Local enums are Java 16, not 5
> `void m() { enum Kind { A, B } }` does not compile on 5–15. Nested **member** enums (inside a class) were valid from 1.5 and are implicitly `static`. Do not date the whole feature from 16 because method-local declarations are new.

> [!tip] Interview answer
> **Enums arrived in Java 5 (JDK 1.5 / Tiger) via JSR 201.** They are real classes with a fixed set of constants, not a pile of `int` fields. `Enum` / `EnumSet` / `EnumMap` are `since 1.5`. Declaring an enum *inside a method* is a Java 16 addition.
