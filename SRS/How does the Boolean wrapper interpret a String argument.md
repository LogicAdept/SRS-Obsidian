<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #Java/String #SRS

# How does the `Boolean` wrapper interpret a `String` argument?

> [!abstract] Short answer
> **Only** a non-null string that equals `"true"` **ignoring case** is treated as true (`"true"`, `"True"`, `"TRUE"`, `"tRUe"`). Every other string — `"false"`, `"False"`, `"yes"`, `"1"`, `""`, whitespace-padded `" true "` — is false. `parseBoolean` / `valueOf(String)` **do not throw** `NumberFormatException`. Prefer those factories; `new Boolean(String)` uses the same rule but is deprecated.

## One token: ignore-case `"true"`

`Boolean.parseBoolean(String s)` returns the primitive `true` if `s` is not `null` and equals `"true"` ignoring case; otherwise it returns `false`, **including when `s` is `null`**. Official examples: `parseBoolean("True")` → `true`; `parseBoolean("yes")` → `false`.

`Boolean.valueOf(String s)` applies that same test and returns a `Boolean` object (`Boolean.TRUE` / `Boolean.FALSE` — see [[What are Boolean.TRUE and Boolean.FALSE]]). There is no second token for false: `"False"` is simply not `"true"`.

The deprecated `Boolean(String)` constructor allocated a `Boolean` with the same rule. Use `parseBoolean` for an `int`-style primitive result, or `valueOf` for a wrapper.

```d2
direction: down
s: "String s" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
test: "s != null AND\nequalsIgnoreCase(\"true\")" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
t: "true / Boolean.TRUE" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
f: "false / Boolean.FALSE" {
  width: 240
  height: 60
  style.fill: "#ffebee"
}

s -> test
test -> t: "yes"
test -> f: "no, including null"
```

**Fig. 1.** String-to-boolean on `Boolean` is a single ignore-case match, not a true/false grammar.

```java
boolean a = Boolean.parseBoolean("true");   // true
boolean b = Boolean.parseBoolean("True");   // true
boolean c = Boolean.parseBoolean("tRUe");   // true
boolean d = Boolean.parseBoolean("False");  // false — not a false token
boolean e = Boolean.parseBoolean("yes");    // false
boolean f = Boolean.parseBoolean(null);     // false, no exception

Boolean boxed = Boolean.valueOf("TRUE");    // Boolean.TRUE
```

**Listing 1.** Conceptual: case-insensitive `"true"` only; `"False"` and `null` are false.

Unlike [[What is NumberFormatException]] on `Integer.parseInt`, bad Boolean strings are not errors. No `0`/`1` / `"yes"` / `"on"` dialect is recognized. Leading or trailing spaces fail the equality check.

> [!warning] `Boolean.getBoolean` does not parse the string
> `Boolean.getBoolean(name)` looks up a **system property** whose *name* is `name`, then applies the same ignore-case `"true"` test to that property’s value. `Boolean.getBoolean("true")` is not `parseBoolean("true")`; it is true only if a property literally named `"true"` exists and equals `"true"` ignoring case. Empty or `null` names yield `false`.

> [!warning] Deprecated constructor still fools interview snippets
> Snippets that write `new Boolean("False")` are using the old constructor (deprecated since 9, for removal). The result is `false` for the reason above, not because the API parsed a `false` keyword. Prefer `parseBoolean` / `valueOf`, and `TRUE`/`FALSE` when you already have a primitive.

> [!tip] Interview answer
> **`Boolean` treats a string as true only when it equals `"true"` ignoring case; everything else, including `"false"` and `null`, is false and does not throw.** Use `parseBoolean` or `valueOf(String)` — not `getBoolean`, which reads a system property by that name. `new Boolean(String)` followed the same rule but is deprecated.
