<!--
reps: 0
priority: 0
-->
#Java/IO/File #Java/NIO #OperatingSystems/IO/Files #SRS

# What is `FileFilter` in Java?

> [!abstract] Short answer
> **`java.io.FileFilter` (since 1.2) is a `@FunctionalInterface`:** `boolean accept(File pathname)`. It is “a filter for abstract pathnames,” used only as an argument to `File.listFiles(FileFilter)`. Each **child** `File` is kept when `accept` returns `true`. A `null` filter accepts every child. The older twin is `FilenameFilter.accept(File dir, String name)` (1.0). NIO’s analogue is `DirectoryStream.Filter<Path>` on `Files.newDirectoryStream` ([[How do you list directory entries that match a criterion in Java]], [[How would you explain the java.io.File class and path representation]]).

## A predicate on a child `File`

`listFiles(FileFilter)` lists **immediate** children of a directory pathname (not `.` / `..`). For each child it builds a `File` and calls `accept`. Order is unspecified. The `File` you receive is still only a pathname — `isDirectory()`, `isFile()`, `exists()`, `length()`, `getName()` hit the filesystem **at list time** ([[Does a java.io.File instance represent only a path without opening the file]], [[How would you explain the java.io.File class and path representation]]).

If the abstract pathname is not a directory, or the listing fails, `listFiles` returns **`null`**, not an empty array. A directory that exists but matches nothing returns a **zero-length** `File[]`. `SecurityException` if a manager denies `checkRead`.

| Type | Method | Typical hook |
| --- | --- | --- |
| `FileFilter` | `accept(File pathname)` | `listFiles(FileFilter)` → `File[]` |
| `FilenameFilter` | `accept(File dir, String name)` | `list` → `String[]`, or `listFiles` → `File[]` |
| `DirectoryStream.Filter<Path>` | `accept(Path)` may throw `IOException` | `Files.newDirectoryStream(dir, filter)` |

`FilenameFilter` is enough for a name suffix. `FileFilter` is the one to use when the decision needs `isDirectory()` without constructing `new File(dir, name)` yourself. It is a functional interface, so a lambda is a legal implementation ([[How do you list directory entries that match a criterion in Java]], [[What character separates path components in the Java File API]]).

```java
import java.io.File;
import java.io.FileFilter;

class Filters {
    static final FileFilter DIRS = File::isDirectory;

    static File[] listedDirs(File dir) {
        File[] kids = dir.listFiles(DIRS);
        if (kids == null) {
            throw new IllegalArgumentException("not a listable directory: " + dir);
        }
        return kids;
    }
}
```

**Listing 1.** Method reference `File::isDirectory` is a `FileFilter`. Treat `null` as “could not list,” not “no directories.”

```d2
direction: down
list: "File.listFiles(FileFilter)" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
acc: "accept(child File)" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
out: "File[] or null" {
  width: 180
  height: 40
  style.fill: "#fff8e1"
}
list -> acc -> out
```

**Fig. 1.** `FileFilter` does not walk trees. Recursion is your loop over accepted directories.

> [!warning] `null` from `listFiles` is not “filter rejected all”
> Iterate only after a null check. `FileFilter` is not recursive and not NIO `PathMatcher` / glob. `accept` must not assume the child still exists after listing. There is no `isExists()` on `File` — the method is `exists()`. `endsWith(".txt")` is case-sensitive `String` matching even where `File.equals` is not.

> [!tip] Interview answer
> `FileFilter` is a one-method interface, `accept(File)`, passed to `listFiles` to keep some children. Use it when you need file-type checks; use `FilenameFilter` when a name string is enough. If `listFiles` returns null, the path was not a listable directory.
