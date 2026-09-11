<!--
reps: 0
priority: 0
-->
#Java/Versions/15 #SRS

# What are text blocks

> [!abstract] Short answer
> **A text block (final in Java 15, JEP 378; previewed 13–14) is a multi-line `String` literal delimited by `"""`: line terminators are literal, incidental leading whitespace is stripped by the compiler, and the result is still an ordinary `String` — same pool, same methods, concatenation and formatting included.** The stripping rule is the interview: the **minimum indentation across content lines and the closing delimiter** is removed, and the closing delimiter's position decides the trailing newline.

## Incidental whitespace and the delimiters

Java splits each line into *incidental* whitespace (stripped) and *significant* whitespace (kept). The algorithm: compute the minimum indentation over all content lines **and the closing-delimiter line**, then strip that prefix from every line. So shifting the closing `"""` left or right changes the content without touching the opening delimiter — the classic formatting trap. A closing delimiter on its own line means the content ends with a newline; putting it on the last content line removes that trailing `\n`. Trailing spaces on a line are stripped (survive only via the `\s` escape), `\` at end of line joins lines, and standard escapes (`\n`, `\"`, `\\`) still apply.

Text blocks are real `String`s: interned like other literals when constant, comparable with `equals`, usable in `switch` selectors, and concatenatable — `"a" + """..."""` works, but the mixed indentation rules make the boundaries worth checking ([[What are switch expressions]]-era multi-line alternatives like `+ "\n" +` chains are what text blocks replace).

```d2
direction: down
src: "\"\"\"\n    {\n      \"k\": 1\n    }\n    \"\"\"  (closing on own line)" {
  width: 380
  height: 100
  style.fill: "#e3f2fd"
}
strip: "strip min indent of content + closing line" {
  width: 380
  height: 60
  style.fill: "#fff8e1"
}
res: "{\n  \"k\": 1\n}\n  (trailing newline kept)" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
src -> strip -> res
```

**Fig. 1.** The closing delimiter participates in the minimum-indent computation — moving it re-indents every line and toggles the trailing newline.

```java
public class V19_TextBlocks {
    public static void main(String[] args) {
        String a = """
                {
                  "k": 1
                }
                """;
        System.out.println("closing delimiter on own line -> length " + a.length() + ", endsWith newline = " + a.endsWith("\n"));

        String b = """
                same
                indent""";
        System.out.println("closing delimiter on last content line -> length " + b.length());

        String c = """
                keep trailing space:\s
                done""";
        System.out.println("escaped space kept -> line1 ends with space: " + c.lines().findFirst().get().endsWith(" "));

        String d = "SELECT id" +
                """
                FROM users
                WHERE id = 1""";
        System.out.println("concat: " + d);
    }
}
```

**Listing 1.** Verified on JDK 21 (V19_TextBlocks in empirics): `closing delimiter on own line -> length 13, endsWith newline = true`, `closing delimiter on last content line -> length 11`, `escaped space kept -> line1 ends with space: true`, `concat: SELECT idFROM users` + newline + `WHERE id = 1` — delimiter position controls the newline, `\s` saves the trailing space (out/V19_TextBlocks.txt).

> [!warning] Same source, different closing-delimiter column, different string
> The recurring production bug: an auto-formatter re-indents the closing `"""` and every line's content shifts, or a trailing space silently disappears (they are stripped unless `\s`) — diffs of JSON/SQL fixtures fail mysteriously. Second trap: text blocks are **not** raw strings — backslash escapes still process, so Windows paths and regexes need the same doubling as ordinary literals. Third: a text block still ends where the closing delimiter's line says — "it always ends with a newline" is exactly as wrong as "it never does" ([[What is the java.time API and why did it replace Date and Calendar]]-era boilerplate it replaces notwithstanding).

> [!tip] Interview answer
> **Text blocks (final 15) are `"""`-delimited multi-line Strings with compiler-run incidental-whitespace stripping: minimum indent across content and the closing delimiter, trailing newline iff the closing delimiter sits on its own line, trailing spaces stripped unless `\s`.** They are ordinary Strings — pool, escapes, concatenation — with formatting-sensitive boundaries.
