<!--
reps: 0
priority: 0
-->
#Java/Versions/9 #SRS

# What is jshell

> [!abstract] Short answer
> **`jshell` (JEP 222, Java 9) is the JDK's interactive REPL: it evaluates declarations, expressions, and statements incrementally, keeps state across lines, auto-imports `java.io`/`java.math`/`java.net`/`java.nio.file`/`java.util` and friends, and supports tab completion, `/vars`, `/methods`, `/types`, `/list`, and `/exit`.** It runs snippets under the hood by wrapping them into classes and invoking via a remote agent — not by interpreting source.

## How a session works

Feed it stdin or a `.jsh` script: variables and methods become live snippets you can redefine line by line (forward references resolve as you fill them in), expressions echo their value into implicit variables (`$4`), and classpath/import ergonomics come from the auto-import list plus `/env`. Feedback modes (`-q`, `-s`, `--feedback concise`) control echo verbosity. It is a JDK tool, so it launches with the JDK you point it at — useful for checking an API's behavior on exactly the target version ([[How does Java version numbering work]]).

Verified shape of a session on JDK 21 with concise feedback — input `int x = 2; int y = 40; int sum() { return x + y; } sum()`: the transcript reports `x ==> 2`, `y ==> 40`, creates the method, and the value expression lands in implicit variable `$4 ==> 42`. On a pipe the variable/method echoes are suppressed and only `$4 ==> 42` surfaces.

```d2
direction: down
in: "snippet / .jsh script" {
  width: 240
  height: 50
}
wrap: "wrap snippets into classes\ncompile with javac" {
  width: 300
  height: 60
  style.fill: "#fff8e1"
}
agent: "execute in remote JVM agent\nkeep state, echo result" {
  width: 320
  height: 65
  style.fill: "#e3f2fd"
}
out: "value in implicit var ($N)\nor /vars /methods state" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
in -> wrap -> agent -> out
```

**Fig. 1.** JShell is not an interpreter: snippets are compiled and run in an execution agent, with session state tracked by the tool.

```java
// V13_Jshell.jsh (verbatim input):
int x = 2;
int y = 40;
int sum() { return x + y; }
sum()
```

**Listing 1.** Verified on JDK 21 (V13_Jshell in empirics, `jshell --feedback concise`): the transcript ends `$4 ==> 42` — the `sum()` call's result captured in the implicit variable `$4`; declarations `x`, `y`, `sum()` stay live in the session (out/V13_Jshell.txt).

> [!warning] JShell state is not a classpath program
> Three traps: jshell auto-imports make code look dependency-free — a snippet that "works in jshell" may fail to compile in a real file missing the import. Redefining a method/variable replaces the old snippet silently; `/list` is how you see what actually exists. And exceptions in snippets are reported per line, not as crash traces — people wrongly conclude jshell "handles" exceptions. It is also not a scripting replacement for production: no stable packaging story, no guarantee of the wrapping behavior ([[What is the Java release cadence since Java 9]]).

> [!tip] Interview answer
> **jshell is the Java 9 REPL — incremental, stateful, auto-importing, backed by compiled snippets run in an execution agent.** I use it to probe APIs on the exact target JDK and to sanity-check expressions; it is a developer tool, not a deployment artifact.
