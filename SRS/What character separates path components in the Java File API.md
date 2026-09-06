<!--
reps: 0
priority: 0
-->
#Java/IO/File #OperatingSystems/IO/Files #SRS

# What character separates path components in the Java File API?

> [!abstract] Short answer
> **`File.separatorChar` / `File.separator`.** That is the **name-separator**: one character taken from the system property `file.separator`. On UNIX (including Linux) it is `/`; on Microsoft Windows it is `\`. When Java turns an abstract pathname into a string, each name is joined by **one** copy of that default separator. A different field, `File.pathSeparatorChar` (`path.separator`: `:` on UNIX, `;` on Windows), separates **filenames in a list** (classpath, `PATH`) — not components inside one path ([[Does a java.io.File instance represent only a path without opening the file]], [[How would you explain the java.io.File class and path representation]]). Prefer `new File(parent, child)` over hard-coding a slash.

## Name-separator versus path-separator

A `java.io.File` is an **abstract pathname**: optional prefix plus a sequence of names. It does not open the file. Conversion between that object and a `String` is system-dependent.

| Field | Property | Role | Typical UNIX | Typical Windows |
| --- | --- | --- | --- | --- |
| `separator` / `separatorChar` | `file.separator` | Join **names in one pathname** | `/` | `\` |
| `pathSeparator` / `pathSeparatorChar` | `path.separator` | Join **entries in a path list** | `:` | `;` |

The `*Char` fields are `char`. The `separator` / `pathSeparator` fields are one-character `String`s of those same values.

**Parsing in.** When a pathname string becomes a `File`, names may be split on the default name-separator **or** on any other name-separator the underlying filesystem accepts. On Windows that includes `/` as well as `\`. **Parsing out.** `getPath()` / `toString()` emit names separated by the **default** separator only.

```java
import java.io.File;

class PathSeparators {
    static void show() {
        File nested = new File("logs" + File.separator + "app.log");
        String pathList = "bin" + File.pathSeparator + "lib";
        // nested → "logs/app.log" or "logs\app.log"
        // pathList → "bin:lib" or "bin;lib"
    }
}
```

**Listing 1.** Build a nested pathname with `File.separator`. Build a **list** of locations with `File.pathSeparator`. Do not mix them.

```d2
direction: down
one: "one File path\nlogs + separator + app.log" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
list: "path list\nbin + pathSeparator + lib" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
one -> list: "different characters"
```

**Fig. 1.** Name-separator vs path-separator. Interviews fail people who quote `:` or `;` for folders inside one path ([[How would you explain the Java classpath]], [[How do you list directory entries that match a criterion in Java]]).

Hard-coding `/` in portable library code is the usual bug: it works on UNIX and often on Windows **input**, then `getPath()` still prints `\`. Prefer `File.separator` or `new File(parent, child)` so the platform fills the separator.

> [!warning] `pathSeparator` is not a slash
> `:` / `;` never join `logs` to `app.log`. They join **two paths** in an environment-style list. `File.separator` is a `String`; concatenating with `char` `separatorChar` is the other form. Neither field opens a file. `listFiles()` still returns **`null`** when the pathname is not a directory — separator choice does not change that ([[How do you list directory entries that match a criterion in Java]]).

> [!tip] Interview answer
> Path components in `java.io.File` are separated by `File.separatorChar`, from `file.separator` — slash on UNIX, backslash on Windows. `File.pathSeparator` is the other character, colon or semicolon, for lists like the classpath. Do not hard-code either if the code must run on both families.
