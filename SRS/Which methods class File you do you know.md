<!--
reps: 0
priority: 0
-->
#Java/IO/File #OperatingSystems/IO/Files #SRS

# Which methods of the `File` class do you know?

> [!abstract] Short answer
> **`File` methods inspect or change the filesystem named by an immutable abstract pathname — they do not open a stream.** Create/delete: `createNewFile()` (atomic empty file, `throws IOException`), `mkdir()` / `mkdirs()`, `delete()` (directory must be **empty**), `renameTo(dest)` (platform-dependent; check the `boolean`). Query: `exists()`, `isFile()` / `isDirectory()` / `isHidden()`, `length()`, `lastModified()`, `canRead()` / `canWrite()`. Path: `getName()`, `getParent()` / `getParentFile()`, `getAbsolutePath()`, `getCanonicalPath()`. List: `list()` → `String[]`, `listFiles()` → `File[]` — **`null` if not a directory**, never `.` / `..` ([[Which class intended for work with elements file]], [[How would you explain the java.io.File class and path representation]]).

## Dump list, with the contracts

`File` is still only a pathname until you call these ([[Does a java.io.File instance represent only a path without opening the file]], [[What character separates path components in the Java File API]]).

| Method | Dump | Official extra |
| --- | --- | --- |
| `createNewFile()` | try to create | Iff absent, atomic; **not** a lock; `throws IOException` |
| `delete()` | try to delete file or dir | Dir must be empty; `boolean`, no `IOException` |
| `mkdir()` | try to create a dir | One level. Prefer `mkdirs()` for missing parents |
| `renameTo(File dest)` | try to rename | May fail across stores; may not be atomic; **this** `File` still names the old path |
| `exists()` | exists? | File or directory denoted by the pathname |
| `getAbsolutePath()` | absolute form of constructor path | Relative → `user.dir` (Windows may use drive cwd); empty `File` → `user.dir` |
| `getName()` | short name | Last name in the sequence; `""` if the sequence is empty |
| `getParent()` | parent directory name | Parent **pathname string**, or **`null`** |
| `isDirectory()` / `isFile()` | dir / file | `isFile()` is a **normal** file (not a directory, plus OS rules) |
| `isHidden()` | hidden | UNIX: name starts with `'.'`; Windows: filesystem flag |
| `length()` | size in bytes | **Unspecified** if the pathname is a directory |
| `lastModified()` | last change time | Milliseconds, possibly coarse; **not** creation time |
| `list()` / `listFiles()` | children | **`null`** if not a listable directory; order unspecified |

`list(FilenameFilter)` / `listFiles(FileFilter)` keep some children. Empty match → zero-length array, not `null` ([[What is FileFilter in Java]], [[How do you list directory entries that match a criterion in Java]]).

```java
import java.io.File;
import java.io.IOException;

class FileMethods {
    static String[] kids(File dir) throws IOException {
        if (!dir.isDirectory()) {
            throw new IOException("not a directory: " + dir.getAbsolutePath());
        }
        String[] names = dir.list();
        if (names == null) {
            throw new IOException("listing failed: " + dir);
        }
        return names;
    }
}
```

**Listing 1.** `list()` after `isDirectory()` can still be `null` (I/O / security). Do not iterate `listFiles()` without a null check.

```d2
direction: down
path: "getName / getParent / getAbsolutePath" {
  width: 300
  height: 40
  style.fill: "#e3f2fd"
}
meta: "exists / isFile / length / lastModified" {
  width: 320
  height: 40
  style.fill: "#e8f5e9"
}
mut: "createNewFile / mkdir / delete / renameTo" {
  width: 320
  height: 40
  style.fill: "#fff8e1"
}
```

**Fig. 1.** Three buckets interviews want: path strings, metadata, mutating the entry ([[What is and]], [[How does Java]]).

> [!warning] `list`/`listFiles` return `null`, and `renameTo` is not `mv -f`
> Dump omitted `null`, `mkdirs`, `IOException` on `createNewFile`, and that `renameTo` does not update this object. `length()` on a directory is unspecified. `lastModified()` is not creation time. `delete()` on a non-empty directory fails.

> [!tip] Interview answer
> Name create/delete (`createNewFile`, `mkdir`/`mkdirs`, `delete`, `renameTo`), metadata (`exists`, `isFile`/`isDirectory`, `length`, `lastModified`), path (`getName`, `getParent`, `getAbsolutePath`), and listing (`list` / `listFiles`). Stress that listing returns null when the path is not a directory, and that `File` never opens a byte stream.
