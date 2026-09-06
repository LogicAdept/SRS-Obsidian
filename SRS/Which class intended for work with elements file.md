<!--
reps: 0
priority: 0
-->
#Java/IO/File #Java/NIO #OperatingSystems/IO/Files #SRS

# Which class is intended for working with filesystem entries?

> [!abstract] Short answer
> **`java.io.File` (Java 1.0) — an immutable abstract pathname for files and directories, not an open stream.** Construction does not open anything and does not require the name to exist. When you call methods, it can **create** (`createNewFile`, `mkdir` / `mkdirs`) and **query** (`exists`, `isFile` / `isDirectory`, `length`, `canRead` / `canWrite`, `lastModified`, `getParent`). Dump “creation time” is **wrong** on `File`: `lastModified()` is last **modification** (milliseconds, possibly coarse). Creation/access times are `Files.readAttributes(..., BasicFileAttributes.class).creationTime()` (Java 1.7+) ([[How would you explain the java.io.File class and path representation]], [[Does a java.io.File instance represent only a path without opening the file]]).

## Pathname object, then filesystem calls

`File` is the interview “filesystem element” class in `java.io`. Bytes still go through `FileInputStream` / `FileOutputStream` or NIO `Files`. `RandomAccessFile` is a seekable **open** file, not this type ([[What is RandomAccessFile in Java]], [[How does Java]]).

| Dump claim | Actual API |
| --- | --- |
| Size | `length()` — unspecified if the pathname is a **directory** |
| Access rights | `canRead()` / `canWrite()` (`canExecute()` exists too). Privileged JVMs may return `true` even when the file looks unreadable/read-only |
| Time | `lastModified()` — **not** creation. `0L` can mean missing file or I/O error |
| Parent | `getParent()` / `getParentFile()` — `null` if the name sequence has no parent |
| Create file | `createNewFile()` — atomic create-if-absent; **not** a lock (`FileLock` instead) |
| Create dir | `mkdir()` one level; `mkdirs()` also missing parents (failure may still have created some) |

`delete()` requires an empty directory. `listFiles` / `FileFilter` list **children**, not a tree ([[What is FileFilter in Java]], [[How do you list directory entries that match a criterion in Java]], [[Which methods class File you do you know]]).

```java
import java.io.File;
import java.io.IOException;

class FsEntry {
    static boolean ensureDir(File dir) throws IOException {
        if (dir.exists()) {
            return dir.isDirectory();
        }
        return dir.mkdirs();
    }

    static long sizeIfFile(File f) {
        return f.isFile() ? f.length() : -1L;
    }
}
```

**Listing 1.** `File` creates and inspects entries. `length()` on a directory is unspecified — check `isFile()` first.

```d2
direction: down
file: "File\nabstract pathname" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
meta: "exists / length / lastModified\nmkdir / createNewFile" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
open: "FileInputStream / RandomAccessFile\nactually open bytes" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
file -> meta
file -> open
```

**Fig. 1.** The class for names, create, and metadata. Opening content is a different type ([[What character separates path components in the Java File API]], [[What is and]]).

> [!warning] `File` is not creation time, and `canRead` is not a permission dump
> There is no `getCreationTime()` on `File`. `lastModified()` granularity may be **seconds**. `canRead()` tests whether **this JVM** can read, not the POSIX mode bits. A `File` that never existed still has a parent string. `createNewFile` returning `false` means the name already existed, not necessarily a permission failure.

> [!tip] Interview answer
> `java.io.File` is the class for filesystem entries: a pathname you can create, delete, and query without opening a stream. Use `length`, `canRead`/`canWrite`, `lastModified`, and `getParent` for metadata. Creation time is NIO `BasicFileAttributes`, not `File`.
