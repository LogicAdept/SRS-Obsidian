<!--
reps: 0
priority: 0
-->
#Java/IO/File #Java/NIO #OperatingSystems/IO/Files #SRS

# How do you list directory entries that match a criterion in Java?

> [!abstract] Short answer
> **Two families.** Classic `java.io`: `dir.listFiles(filter)` (Java 1.2) returns a `File[]` of **immediate** children whose `FileFilter.accept` or `FilenameFilter.accept` is `true` (extension, `isFile()`, name length). A `null` filter keeps every name; a failed listing returns **`null`**. NIO.2 (Java 7): `Files.newDirectoryStream(dir, "*.java")` or `Files.newDirectoryStream(dir, DirectoryStream.Filter)` — an **open** `DirectoryStream<Path>` you must close. Java 8 `Files.list(dir)` is a `Stream<Path>` you also close, then `.filter(...)`.

## `File.listFiles` versus `Files.newDirectoryStream`

`File` is a pathname, not an open directory ([[Does a java.io.File instance represent only a path without opening the file]], [[How would you explain the java.io.File class and path representation]]). `list()` / `listFiles()` read that directory once and copy names into an array. Children are `new File(dir, name)`; `.` and `..` are omitted; order is unspecified ([[What is FileFilter in Java]], [[How would you explain the java.io.File class and path representation]]).

| API | Match | Miss / failure |
| --- | --- | --- |
| `list()` / `listFiles()` | every immediate name (no `.` / `..`) | `null` if not a directory or listing fails |
| `listFiles(FileFilter)` | `accept(File)` on the child | same `null` |
| `listFiles(FilenameFilter)` / `list(FilenameFilter)` | `accept(dir, name)` | same `null` |
| `Files.newDirectoryStream(Path, String glob)` | file-name glob (`getPathMatcher`) | `NotDirectoryException` (optional) / `IOException`; bad glob → `PatternSyntaxException` |
| `Files.newDirectoryStream(Path, DirectoryStream.Filter<Path>)` | `accept(Path)` may throw `IOException` | same open-directory exceptions; filter `IOException` → `DirectoryIteratorException` on `hasNext` / `next` |

`FileFilter` (1.2) and `FilenameFilter` (1.0) are functional interfaces. `DirectoryStream.Filter` (1.7) is too; its `accept` is allowed to throw `IOException` (the `java.io` filters are not).

`File`’s own `listFiles` JavaDoc points at `Files.newDirectoryStream` for large or remote directories: iterate instead of materializing every name. Close that stream — try-with-resources, or `close()` after the loop. The iterator’s `Path` values are the entry name resolved against `dir`.

Neither API walks the tree. Recursion is `Files.walk` / `Files.find` (Java 8), a different method.

```d2
direction: down
q: "list children matching a criterion" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
io: "File.listFiles(filter)\nFile[] or null" {
  width: 260
  height: 60
  style.fill: "#fff8e1"
}
nio: "Files.newDirectoryStream\nclose the DirectoryStream" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
q -> io
q -> nio
```

**Fig. 1.** Snapshot array (`java.io`) versus an open directory iterator (NIO.2). Both are one directory deep.

```java
import java.io.File;
import java.io.IOException;
import java.nio.file.DirectoryStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

class ListMatchingEntries {
    static File[] txtFiles(File dir) {
        File[] matched = dir.listFiles(
                f -> f.isFile() && f.getName().endsWith(".txt"));
        return matched == null ? new File[0] : matched;
    }

    static List<Path> javaFiles(Path dir) throws IOException {
        List<Path> names = new ArrayList<>();
        try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, "*.java")) {
            for (Path entry : stream) {
                names.add(entry);
            }
        }
        return names;
    }
}
```

**Listing 1.** `FileFilter` on `getName()` plus `isFile()`, with `null` turned into an empty array. Glob `*.java` is the documented NIO name pattern; the `DirectoryStream` is closed by try-with-resources. `endsWith(".txt")` is case-sensitive `String` matching.

> [!warning] `listFiles` null versus an unclosed directory stream
> A `File[]` of **no matches** is empty and non-null; `null` means the `File` was not a listable directory (`SecurityException` if `checkRead` fails). NIO **throws** instead of returning null. Forgetting to close `DirectoryStream` (or `Files.list`) keeps the directory open. A glob matches the **file name string**, not `isFile()` — directories named `Foo.java` pass `*.java`. Filter I/O on NIO surfaces as `DirectoryIteratorException`, not a checked `IOException` from the for-each itself.

> [!tip] Interview answer
> Use `File.listFiles` with a `FileFilter` or `FilenameFilter` for a one-shot `File[]` of immediate children — and treat a null return as “not a directory,” not “no hits.” On NIO.2, `Files.newDirectoryStream(dir, "*.java")` or a `DirectoryStream.Filter` iterates matching `Path`s; close the stream. Neither call is recursive.
