<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #Java/Versions #SRS

# Can you use `assert` as an identifier after Java 1.4?

> [!abstract] Short answer
> **No. From Java 1.4, `assert` is a reserved keyword, so `int assert = 10;` does not compile.** The 1.4-era `javac -source 1.3` mode could still accept `assert` as a name (with warnings) and rejected the `assert` statement. Current `javac` does not offer that 1.3 mode.

## Keyword, not a name

An identifier must not have the same spelling as a reserved keyword. `assert` is reserved, like `if` or `class`, not a contextual keyword such as `var` or `yield` that can still be a name in other positions ([[In which Java version was the assert keyword introduced]]).

So these are illegal in 1.4+ source: a variable `assert`, a method `assert(...)`, a type named `assert`, a label `assert:`. The keyword is used only for the statement `assert cond;` / `assert cond : detail;` ([[What are the two forms of the Java assert statement]]).

A longer name is fine: `assertFlag` is a different identifier. Existing `.class` files that already used `assert` as a name still run; the break is at recompilation of source.

```d2
direction: down
src: "source mentioning assert" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
kw: "1.4+ source\nreserved keyword" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
old: "1.4 javac -source 1.3\nidentifier + warning" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
err: "int assert = 10\ncompile-time error" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
src -> kw
src -> old
kw -> err
```

**Fig. 1.** After 1.4, `assert` is a keyword in the language. `-source 1.3` was a transitional compiler switch, not a second language.

```java
class Demo {
    // int assert = 10; // does not compile — reserved keyword
    int assertFlag = 10;

    static void check(boolean ok) {
        assert ok;
    }
}
```

**Listing 1.** `assertFlag` is a legal identifier. Uncommenting `int assert = 10;` fails on any 1.4+ source level. `assert ok;` is the statement.

> [!warning] Exam dumps still quote `-source 1.3`
> On the 1.4 compiler, `-source 1.3` (the default then) accepted `int assert = 0;` with warnings and did not accept the `assert` statement. `assert(false);` in that mode is a method call named `assert`, not the keyword statement — it fails unless such a method exists. From JDK 9, `javac` no longer supports `-source` 5 or earlier, so that switch is gone.

> [!warning] Parentheses do not make it a method
> In 1.4+ source, `assert(false);` is the assert statement with a parenthesized condition, not a call you can define. You cannot declare `void assert(boolean b)` to “override” it.

> [!tip] Interview answer
> **No. Since 1.4, `assert` is a reserved keyword, so you cannot use it as a variable, method, type, or label name.** A 1.4-era `-source 1.3` compatibility mode could still treat it as an identifier with warnings; that mode is historical. Names like `assertEnabled` are still legal.
