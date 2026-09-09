<!--
reps: 0
priority: 0
-->
#Java/Versions/8 #Java/Library/Nashorn #Java/Tooling #SRS

# What is jjs

> [!abstract] Short answer
> **`jjs` is the JDK 8 command-line launcher for the Nashorn JavaScript engine.** With files it interprets them; with none it starts an interactive shell. Arguments after `--` become the script’s `arguments`. It is **not** Node, not a browser, and **not on a current JDK**: deprecated for removal in **11**, **removed in 15**. `javax.script` stayed.

## Nashorn’s shell, 8 through 14

Nashorn (JEP 174, Java 8) replaced Rhino as the JDK’s ECMAScript-262 Edition **5.1** engine, exposed through `javax.script` and through a new tool **`jjs`** for scripts, shebang files, and a REPL ([[What is Nashorn]]).

Synopsis: `jjs [options] [script-files] [-- arguments]`. No files → interactive `jjs>` prompt (`println`, `quit()`). `jjs script.js` runs a file. `jjs -- a b c` then `arguments.join(", ")` yields `a, b, c`. Useful flags from the Java 8 tool page: `-cp` / `-classpath`, `-Dname=value`, `--language=es5` (the default), `-strict` (ES5.1 strict mode), `-scripting`, `-fx` (JavaFX), `-doe` (full stack on error).

Nashorn does **not** ship a browser plugin, DOM/CSS, or jQuery. It is not ES6. Java interop is via Nashorn’s linker (`javax.script` from Java, Java APIs from JS). The older `jrunscript` tool is a different launcher (see also on the `jjs` page).

Java 11 terminally deprecated Nashorn, the `jdk.scripting.nashorn*` modules, and `jjs` (`jjs` printed a removal warning). Java 15 **removed** those modules and the tool. `javax.script` itself was **not** removed ([[How are JavaScript and Java related if at all]]).

```d2
direction: down
j8: "Java 8\njjs + Nashorn (ES5.1)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
j11: "Java 11\ndeprecated for removal" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
j15: "Java 15+\njjs gone" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}

j8 -> j11
j11 -> j15
```

**Fig. 1.** Interview dump “run JS in the console” is the Java 8 `jjs` story. A JDK 17/21/25 install has no `jjs`.

```text
jjs script.js
jjs
jjs> println("Hello, World!")
jjs> quit()
jjs -- a b c
jjs> arguments.join(", ")
```

**Listing 1.** Java 8 tool examples: file, REPL, `--` arguments. On JDK 15+ these commands are not there.

> [!warning] `jjs` is not “the JDK JavaScript console” forever
> It shipped with **Nashorn in 8**, warned in **11**, vanished in **15**. GraalJS / Node / a browser are not `jjs`. ES6 syntax is out of spec. `-fx` needed JavaFX on that JDK. The Java 8 tools page points at `jrunscript` as a different launcher — not an alias.

> [!tip] Interview answer
> **`jjs` is Nashorn’s CLI: run `.js` files or an interactive ES5.1 shell, introduced in Java 8.** Pass script args after `--`. It is gone as of Java 15; `javax.script` remains. Not a browser, not Node.
