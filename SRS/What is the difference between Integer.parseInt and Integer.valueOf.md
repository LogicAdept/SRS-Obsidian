<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use the wrapper classes' static methods. `parseXxx` returns a primitive; `valueOf` returns a wrapper object. Going the other way, `String.valueOf` or concatenation produces text.

```java
int n      = Integer.parseInt("42");     // primitive int
Integer w  = Integer.valueOf("42");       // Integer object
double d   = Double.parseDouble("3.14");
String s   = String.valueOf(42);          // "42"
```

A malformed string throws `NumberFormatException`, so wrap parsing of untrusted input in a try/catch or validate first.

Dumps also show radix overloads: `Integer.parseInt("111", 2)` and `Integer.valueOf("111", 2)` treat the text as binary and yield 7.

> [!warning] Unverified traps from the dump
> - `parseInt` yields `int`; `valueOf` yields `Integer` (and may use the integer cache).
> - Bad text throws `NumberFormatException`.
