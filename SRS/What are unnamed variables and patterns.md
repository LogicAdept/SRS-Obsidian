<!--
reps: 0
priority: 0
-->
#Java/Versions/22 #SRS

# What are unnamed variables and patterns

> [!abstract] Short answer
> **JEP 456 (final in Java 22; previewed as 443 in 21) lets you write `_` where a binding is required but its value is unused: locals, for-loop and try-with-resources resources, lambda parameters, catch parameters, and as unnamed patterns in switch and instanceof. Multiple `_` can appear in the same scope because each names nothing, and `_` can never be read.**

## What problem `_` solves

Unused variables are noise and misinformation: `catch (NumberFormatException e) { return false; }` suggests `e` matters; two nested lambda parameters you ignore force inventing names like `ignored1`. With `_` the source literally states "not used", IDEs stop flagging warnings, and in pattern switches unnamed patterns participate in exhaustiveness without binding: `case Integer _ -> ...` matches and discards. The underscore was a legal identifier before Java 8; 8 reserved it for lambda use ("use of `_` as an identifier is not allowed"), and 21 previewed its rebirth as a non-identifier — 22 finalized it ([[What was new in Java 22]]).

```java
public class V45_UnnamedApi22 {
    static String kind(Object o) {
        return switch (o) {                                   // pattern switch (final 21)
            case Integer i when i > 0 -> "positive-int";
            case Integer _ -> "int";                          // unnamed pattern: matches, ignores value
            case String s -> "string:" + s;
            default -> "other";
        };
    }

    public static void main(String[] args) {
        System.out.println(kind(7));
        System.out.println(kind(-3));
        System.out.println(kind("hi"));
        System.out.println(kind(2.5));
        Runnable r = () -> { var _ = 1; };                    // unnamed variable in lambda
        r.run();
        System.out.println("lambda body ran");
    }
}
```

**Listing 1.** Verified on JDK 21 with `--enable-preview` (V45_UnnamedApi22 in empirics): `positive-int`, `int`, `string:hi`, `other`, `lambda body ran` (out/V45_UnnamedApi22.txt).

```d2
direction: right
decl: "locals, for/resources,\ncatch, lambda params" { style.fill: "#e8f5e9"; width: 270; height: 90 }
pat: "patterns: switch, instanceof\ncase Integer _ -> ..." { style.fill: "#e3f2fd"; width: 290; height: 90 }
rule: "cannot be read, duplicated freely,\nno shadowing questions" { style.fill: "#fff3e0"; width: 300; height: 90 }
decl -> pat -> rule: ""
```

**Fig. 1.** Two faces of `_`: unnamed declarations and unnamed patterns, with the common rule that it names nothing and reads nothing.

> [!warning] `_` is not a blank constant
> It cannot be read, assigned to later, or used as a field or method parameter — it is a compile-time statement of intent. Before 22 (without preview flags) using `_` at all was a compile error since Java 8, so legacy code that once had `int _ = 0;` identifiers had to be renamed when moving to modern javac ([[How would you explain notable language changes in recent Java versions]]).

> [!tip] Interview answer
> **Unnamed variables and patterns — JEP 456, final in 22 — give you `_` for bindings you never use: catch parameters, lambda params, loop variables, and switch patterns. It removes warning noise, makes intent explicit, and unnamed patterns still participate in exhaustiveness. Underscore was a normal identifier before 8, got reserved in 8, previewed again in 21, and finalized in 22.**
