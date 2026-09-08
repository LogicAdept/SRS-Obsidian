<!--
reps: 0
priority: 0
-->
#Java/Language #SRS

# Which recommendations to style code on Java?

> [!abstract] Short answer
> There is **no style the compiler enforces**. The language’s own **naming** “shoulds” live in the declarations chapter: packages in lowercase (`com.example`), types in PascalCase nouns, methods in camelCase **verbs**, constants `UPPER_SNAKE`, type parameters like `T` / `E` / `K` / `V`. Oracle still **hosts** *Code Conventions for the Java Programming Language* (last revised **20 April 1999**, archived): 4-space indent, ~80-column lines, one public type per file, fields then constructors then methods. Teams may use a later house guide; `javac` will not check it. File shape: [[What does the typical structure or form of Java source code look like]].

## Spec “should” vs a 1999 booklet

**Names (still the language document).** Unique package names start with a lowercase DNS-style prefix (`com`, `org`, …). Class names are descriptive nouns in mixed case with each word capitalized (`ImageSprite`). Interface names look like class names (noun or adjective: `Runnable`). Methods are verbs (`runFast`, `getPriority`, `isInterrupted`, `toString`). Non-constant fields are camelCase with a lowercase first letter; `public` mutable fields are rare. Constants (`static final`) are uppercase words separated by `_`. Locals are short but meaningful; one-letter names are for throwaways (`i`, `n`, `c`). Type variables stay uppercase and pithy (`T`, `E` for elements, `K`/`V` for maps).

Those are **conventions**, not compile-time rules. `class foo` compiles; it just fights every Java reader.

**Oracle Code Conventions (1999, archived).** Oracle marks the pages “archive purposes only.” Useful leftovers that still match common Java:

| Topic | 1999 booklet |
| --- | --- |
| File | One **public** class or interface; it is first; package then imports then types |
| Indent | **Four** spaces per level; tabs, if used, every **8** columns |
| Line length | Avoid more than **80** characters |
| Class body order | `static` fields, instance fields, constructors, then methods grouped by **behavior** not by `public`/`private` |
| Names | Same camelCase / `UPPER_SNAKE` split as above |
| Variables | Do not start names with `_` or `$` even though the language allows them |

Methods grouped by functionality means a private helper may sit next to the public method that uses it. Beginning-of-file copyright blocks and “files longer than 2000 lines” are booklet advice, not SE 25.

```d2
direction: down
lang: "language naming shoulds\ncom.example, PascalCase, getX" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
book: "1999 Code Conventions\n4 spaces, 80 cols, member order" {
  width: 320
  height: 55
  style.fill: "#fff3e0"
}
team: "project formatter\nnot javac" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
lang -> team
book -> team
```

**Fig. 1.** Naming is in the language document. Layout is a house rule. Neither is a compilation requirement.

```java
package com.example.app;

public class ImageSprite {
    public static final int MAX_WIDTH = 999;

    private int pixelCount;

    public ImageSprite() {}

    public int getPixelCount() {
        return pixelCount;
    }

    public void runFast() {
        int n = pixelCount;
        pixelCount = n;
    }
}
```

**Listing 1.** Names that match the declarations chapter: package, type, constant, field, getter, verb method. Indentation is four spaces.

> [!warning] Code Conventions is not “the Java spec” and not current Oracle policy
> The dump’s “recommendations are in Java Code Conventions” names a real Oracle document, last edited **1999**, now archived. It does not mention records, `var`, modules, or compact source. `javac` does not read it. Answering only “follow Code Conventions” without naming the **1999** date and the JLS naming shoulds is incomplete.

> [!warning] Do not treat Google Java Style (or 80 columns) as the language
> Other popular guides exist. They are not Java SE. 80-column terminals are why the 1999 booklet picked 80; many codebases use 100 or 120. Tabs-every-8 with 4-space indents is a booklet quirk that surprises people who set tab width to 4. Style tools can enforce a project rule; they are not `javac`.

> [!tip] Interview answer
> **Java does not compile style.** The language document still asks for `com.example` packages, PascalCase types, camelCase verb methods, and `UPPER_SNAKE` constants. Oracle’s *Code Conventions* is a 1999 archived layout guide (4 spaces, about 80 columns, one public class per file). Follow the project formatter; do not quote that booklet as if it were Java 25.
