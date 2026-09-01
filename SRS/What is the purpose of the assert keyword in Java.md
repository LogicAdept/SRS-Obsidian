<!--
reps: 0
priority: 0
-->
#Java/Language/Assert #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Not an answer for review.

- Assert checks assumptions about values at arbitrary points in the program.
- A failed check typically aborts and reports where the bad data was found; that helps localize bugs, including after a refactor.
- Assertions are usually left on during development and testing and turned off in release builds.
- Because they may be stripped at compile time or disabled at run time, they must not change program behavior. Do not call methods that mutate program or external state inside `assert`.
- Java forms: `assert booleanExpr;` and `assert booleanExpr : nonVoidExpr;`.
- When assertions are enabled and the boolean is `false`, the JVM throws `java.lang.AssertionError`. The expression after `:` is converted to a string and passed to the `AssertionError` constructor.
