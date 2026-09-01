<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Versions #SRS

# In which Java version was the assert keyword introduced?

> [!abstract] Short answer
> **Java 1.4 (J2SE 1.4).** From that language level, `assert` is a reserved keyword, so `int assert = 10;` does not compile. `AssertionError` and the class-loader assertion-status APIs are also since 1.4.

## Language change in 1.4

Before 1.4, `assert` was a legal identifier. The 1.4 language added the `assert` statement (`assert cond;` and `assert cond : detail;`) and reserved the word ([[What are the two forms of the Java assert statement]], [[Can you use assert as an identifier after Java 1.4]]). Using it as a name fails with: as of release 1.4, `'assert'` is a keyword, and may not be used as an identifier.

That is a **source** break, not a binary one: old `.class` files that used `assert` as a field or method name still run. Runtime checking is a separate switch: assertions are off until `-ea` ([[How do you enable Java assertions at runtime]]).

The 1.4-era `javac` defaulted to `-source 1.3` (identifier allowed, with warnings; the statement forbidden) and required `-source 1.4` to compile the new statement. Current `javac` does not offer 1.3 source; `assert` is simply a keyword.

```d2
direction: right
v13: "≤ 1.3\nidentifier OK" {
  width: 200
  height: 70
  style.fill: "#eceff1"
}
v14: "1.4+\nreserved keyword" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
v13 -> v14
```

**Fig. 1.** The keyword (and `AssertionError`) arrive in 1.4. Later versions keep that meaning.

```java
class Demo {
    // int assert = 10; // illegal from 1.4 source onward
    static void check(int n) {
        assert n > 0;
    }
}
```

**Listing 1.** From 1.4 source, `assert` is the statement, not a variable name. Uncommenting the field does not compile.

> [!warning] 1.4 `javac` did not default to 1.4 source
> Exam dumps pair `int assert = 0` with `-source 1.3` (warns) vs `-source 1.4` (error), and `assert false;` the other way around. That default-to-1.3 compatibility mode is historical. Do not treat “Java 1.4 is installed” as “the statement compiles without `-source 1.4`” for that era’s compiler.

> [!warning] Do not confuse with `enum` (Java 5)
> `assert` is 1.4. `enum` is 5. Both stole former identifiers; they are different releases.

> [!tip] Interview answer
> **`assert` was added in Java 1.4.** It became a reserved keyword, so you cannot use it as a variable or method name at a 1.4+ source level. Enabling the checks is still a runtime flag (`-ea`); introducing the keyword did not turn assertions on by default.
