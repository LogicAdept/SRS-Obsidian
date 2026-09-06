<!--
reps: 0
priority: 0
-->
#Java/IO/File #OperatingSystems/IO/Files #SRS

# How would you explain the `java.io.File` class and path representation?

> [!abstract] Short answer
> **`File` (Java 1.0) is an immutable abstract pathname, not an open file.** It stores a system-independent path: an optional prefix plus a sequence of names. `getPath()` joins those names with `File.separator` (`file.separator`: `'/'` on UNIX, `'\\'` on Windows). `pathSeparator` (`':'` / `';'`) separates entries in a **path list**, not components of one file. Construction does not open a connection and does not require the name to exist. Relative names resolve against `user.dir` when you ask for an absolute form.

## Abstract pathname, then the two separators

An abstract pathname has (1) an optional system-dependent **prefix** and (2) zero or more **names**. UNIX absolute prefix is `"/"`. The root directory is that prefix plus an empty name sequence. Windows: drive plus `":"` and possibly `"\\"`, or UNC prefix `"\\\\"` with host and share as the first two names. Relative UNIX paths have **no** prefix. Conversion to/from a string is system-dependent; when **parsing**, the JVM accepts the default separator **or** any other separator the OS supports ([[Does a java.io.File instance represent only a path without opening the file]], [[What character separates path components in the Java File API]]).

| Field | Property | Meaning |
| --- | --- | --- |
| `separator` / `separatorChar` | `file.separator` | Name separator inside one pathname (`/` vs `\`) |
| `pathSeparator` / `pathSeparatorChar` | `path.separator` | Separator in a **list** of pathnames (`:` vs `;`, as in `PATH`) |

`File` implements `Serializable` and `Comparable<File>`. It is **not** `Closeable`. The pathname never changes after construction. The instance **may or may not** denote a real file or directory.

Constructors: `File(String)`, `File(String parent, String child)`, `File(File parent, String child)`, `File(URI)` (1.4, `file:` scheme). Empty string → empty abstract pathname. `null` pathname or child → `NullPointerException`. If `parent` is `null`, it behaves like `new File(child)`. An **absolute** `child` is converted to relative in a system-dependent way.

`getName()` is the last name (empty string if the sequence is empty). `getParent()` / `getParentFile()` drop that last name (or `null` if there is no parent). `getPath()` emits names joined by the default separator. `isAbsolute()`: UNIX prefix `"/"`; Windows drive+`"\\"` or `"\\\\"`. `getAbsolutePath()`: already absolute → `getPath()`; empty pathname → `user.dir`; else resolve against the user directory (Windows may use the drive’s current directory). `getCanonicalPath()` is absolute **and unique** (drops `.` / `..`, resolves UNIX links, normalizes Windows drive case) and is declared `throws IOException`.

`toURI()` builds a `file:` URI (`toURL()` is deprecated — it does not escape illegal URL characters). `toPath()` yields a `java.nio.file.Path` for the same abstract path (default filesystem). `equals` / `hashCode` / `compareTo` compare **pathnames** (case rules follow the OS), not inodes.

Methods such as `exists()`, `listFiles()`, `createNewFile()` talk to the filesystem when you call them. They do not turn the `File` into a live handle. Opening bytes is `new FileInputStream(file)` ([[How does Java]], [[How do you list directory entries that match a criterion in Java]], [[Which methods class File you do you know]]).

```d2
direction: down
abs: "abstract pathname\nprefix + names" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
sep: "separator = file.separator\n/ or \\" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
list: "pathSeparator = path.separator\n: or ;  (PATH lists)" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
disk: "may denote nothing\nuntil exists / open" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
abs -> sep
abs -> list
abs -> disk
```

**Fig. 1.** `File` holds a pathname. `separator` joins names; `pathSeparator` joins a list of pathnames. Existence is a later query.

```java
import java.io.File;

class FilePathDemo {
    static String describe(String raw) {
        File f = new File(raw);
        return f.getPath()
                + " abs=" + f.isAbsolute()
                + " exists=" + f.exists()
                + " sep=" + File.separator;
    }

    static File child(File dir, String name) {
        return new File(dir, name);
    }
}
```

**Listing 1.** `new File(raw)` always builds a pathname (`exists()` may be `false`). `new File(dir, name)` resolves a child against a parent pathname. `File.separator` is the name separator, not `pathSeparator`.

> [!warning] `separator` is not `pathSeparator`, and `new File` is not an open file
> Mixing them breaks `PATH`-style lists on UNIX (`:`) vs Windows (`;`). `new File("missing")` does not throw `FileNotFoundException`. `getCanonicalPath()` **does** I/O. `renameTo` changes the directory entry; the `File` object still holds the old pathname. `toURL()` is deprecated; use `toURI()`. Do not put a `File` in try-with-resources.

> [!tip] Interview answer
> `java.io.File` is an immutable abstract pathname: prefix plus names, joined by `File.separator`. It does not open the file and need not exist. `pathSeparator` is only for lists of paths. Relative paths become absolute against `user.dir`; canonical form is the unique, filesystem-normalized string and can throw `IOException`.
