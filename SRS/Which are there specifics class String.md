<!--
reps: 0
priority: 0
-->
#Java/String #Java/Language/Switch #SRS

# Which are there specifics class String

> [!abstract] Short answer
> **`String` is a `final` class whose value never changes.** Every `"literal"` (and text block) is a `String`; those and constant concatenations are interned. Language `+` concatenates (a non-constant `+` is a new object). The API is UTF-16 `char`s (`length` / `charAt`); it implements `CharSequence` and `Comparable<String>`. From **Java 7**, a `switch` selector may be `String` (match with `equals`; `null` throws). **Not** every `String` lives in the intern pool.

## What is special about the type

**Immutable and `final`.** A `String` has a constant value; the class is `final`. Sharing and intern are safe because one interned instance cannot change under other references ([[How would you explain java.lang.String]], [[Why is java.lang.String immutable and final]]).

**Literals, not “all objects in the pool.”** Quotes create interned instances at class creation. `new String("x")`, run-time `+`, and `StringBuilder.toString()` are extra objects unless you `intern()` ([[What is the Java string pool]]).

**`+`.** The language concatenates strings. Compilers may lower one expression to `StringBuilder` / `StringConcatFactory`; a loop of `s = s + x` still allocates many `String`s.

**UTF-16 API.** Indexes count code units; supplementary characters take two slots. `toCharArray()` copies.

**`switch` (Java 7+).** Selector type may be `String`. Case equality uses `String.equals`, not `==`. A `null` selector is a run-time error (historically NPE), not `default` ([[Can you use strings in a Java switch statement]]).

**`hashCode`.** The JDK caches the hash in fields (`hash` / `hashIsZero`) on first use — not a public “computed at construction” contract — which together with immutability makes `String` a natural map key.

JDK 9+ compact `byte[]` + coder is implementation, not the language model ([[How is java.lang.String implemented under the hood]]).

```d2
direction: down
type: "final String\nconstant Unicode sequence" {
  width: 260
  height: 45
}
lang: "\"literals\" interned · + concat · switch since 7" {
  width: 320
  height: 50
}
api: "UTF-16 charAt/length · CharSequence · intern()" {
  width: 320
  height: 50
}

type -> lang
type -> api
```

**Fig. 1.** Special vs `StringBuilder`: language literals/`+`/`switch`, intern, immutability.

```java
public class StringSpecificsDemo {
    static String tag(String kind) {
        switch (kind) { // String selector since 7; uses equals
            case "ok":
                return "OK";
            default:
                return "other";
        }
    }

    static void literals() {
        String a = "x";
        String b = "x";
        boolean interned = a == b;
        String plus = a + b; // new String unless constant
    }
}
```

**Listing 1.** Quotes, `+`, and `switch` on `String`. `tag(null)` does not take `default` — it throws.

> [!warning] Not every `String` is pooled, and `switch` is not `==`
> `new String("x")` is not the interned `"x"`. `switch` compares with `equals`; interned identity is a separate fact. A `null` selector is not a silent miss. Immutability does **not** make passwords safe — you cannot overwrite a `String`; use `char[]`.

> [!tip] Interview answer
> **`String` is `final` and immutable; literals intern; `+` concatenates; the API is UTF-16.** Java 7 allowed `switch` on `String` via `equals`. Only interned strings are in the pool — not every `String` object.
