<!--
reps: 0
priority: 0
-->
#Java/Versions #SRS

# How would you explain notable language changes in recent Java versions

> [!abstract] Short answer
> **Walk the LTS spine, and only quote features that were permanent in that release.** Java 8: lambdas and default methods. Then Oracle’s language-updates catalog (SE 9 onward): **`var` (10)**, switch **expressions** (14), **text blocks (15)**, **records / `instanceof` patterns (16)**, **sealed types (17)**, **record patterns + pattern `switch` (21)**, **unnamed `_` (22)**, then **25**: `import module`, compact source / instance `main`, flexible constructor bodies. Previews are not “in the language” until they graduate. Virtual threads and sequenced collections are **libraries**, not language.

## Permanent language, by release

Oracle’s Java Language Changes Summary is the official 9-and-later table. Interview answers that lump “Java 17/21” as one blob are wrong ([[How would you explain Java 17 21]], [[How would you explain lambda expressions in Java]], [[How would you explain default interface methods since Java 8]]).

| Release | Permanent language (everyday) |
| --- | --- |
| **8** | Lambdas; `default` / `static` interface methods |
| **9** | Modules (`module-info.java`); small Coin leftovers |
| **10** | `var` on locals with initializers (also enhanced-`for` indexes). Not fields, not method params. No `var x = null`. Lambdas / method refs need a target type ([[How would you explain Java 17 21]] is the 16–21 slice) |
| **11** | `var` on lambda parameters |
| **14** | `switch` as an **expression**; `case L ->` (no fall through); `yield` from a block; expressions must be exhaustive |
| **15** | Text blocks: `"""` … `"""` (opening `"""` must be followed by a line terminator) |
| **16** | Records; `instanceof String s` ([[What is a Java record]], [[In which Java version were records standardized]]) |
| **17** | Sealed classes/interfaces + `permits` ([[How would you explain Sealed classes]]). Pattern `switch` is still **preview** here |
| **21** | Pattern `switch` (final); **record patterns** `Point(int x, int y)` including nesting ([[How do records work with pattern matching in switch]]) |
| **22** | Unnamed variables and patterns: `_` |
| **25** | `import module M;`; compact source files + instance `void main()`; statements **before** `super(...)` / `this(...)` |

`var` is a reserved type name, not a keyword — existing fields named `var` stay legal. It infers the initializer’s type; it is not “dynamic typing.”

Arrow `switch` runs only the right-hand side. A `switch` **expression** must yield a value or throw; `default` is usually required (enums can be exhaustive by covering constants). Pattern `switch` plus a sealed selector can be exhaustive without `default`.

Record patterns deconstruct components (`obj instanceof Point(int x, int y)`). Nested records nest patterns. `null` matches no record pattern. Enhanced-`for` record patterns were **removed** before 21 shipped.

`_` (22) names nothing: unused locals, `catch`, lambda params, nested record slots. It is not a field or method parameter. Single `_` as an identifier has been illegal since 9.

**25 in one line each:** `import module java.base` on-demand-imports every public type in packages that module exports (ambiguous simple names still need a single-type import). A compact source file can be just `void main() { ... }` — an implicitly declared class; `IO.println` needs the class name unless you import it. Constructor bodies may run statements before `super`/`this`, but those statements must not use `this` as a live object; they may initialize fields and validate arguments.

Still **preview in 25**: primitive types in patterns / `instanceof` / `switch`. **String templates** previewed in 21–22 and did **not** become permanent — do not list them as a language feature you ship.

```d2
direction: down
a: "8 lambdas / defaults\n10 var  14 switch expr  15 \"\"\"" {\n  width: 340\n  height: 55\n  style.fill: "#fff8e1"\n}\nb: "16 records + instanceof\n17 sealed" {\n  width: 280\n  height: 55\n  style.fill: "#e8f5e9"\n}\nc: "21 record patterns + pattern switch\n22 _   25 import module / compact main / pre-super" {\n  width: 360\n  height: 70\n  style.fill: "#e3f2fd"\n}\n\na -> b\nb -> c\n```

**Fig. 1.** Language only. Virtual threads (21) and sequenced collections (21) are APIs. Pattern `switch` is 21, not 17.

```java
record Point(int x, int y) {}

class Demo {
    static int demo(Object obj) {
        var html = """
                <p>ok</p>
                """;
        int n = switch (html.isBlank() ? 0 : 1) {
            case 0 -> 0;
            default -> 1;
        };
        if (obj instanceof Point(int x, int y)) {
            return x + y + n;
        }
        return switch (obj) {
            case String _ -> n;   // 22: unused binding
            default -> n;
        };
    }
}
```

**Listing 1.** 15 text block + 14 switch expression + 16 record + 21 record pattern + 22 unnamed `_`. Compact `void main()` and `import module` need 25.

> [!warning] Preview is not “recent Java”
> Pattern `switch` in 17 required `--enable-preview`. String templates never graduated. Primitive patterns are still preview in 25. Quoting a JEP number from a project page without checking **Permanent vs Preview** is the usual wrong answer.

> [!warning] `var` and `_` are narrow
> `var` needs an initializer and a denotable (or allowed) type — not `null`, not a lambda without a target type, not a field. `_` does not go in a method signature. `case L ->` does not fall through; mixing that muscle memory with `case L:` is a bug.

> [!tip] Interview answer
> **8 = lambdas. 10 = `var`. 14–15 = switch expressions and text blocks. 16 = records and `instanceof` patterns. 17 = sealed types. 21 = pattern `switch` and record patterns. 22 = `_`. 25 = `import module`, compact `main`, statements before `super`.** Always say which release made it **permanent**. Libraries (virtual threads, sequenced collections) are a different list.
