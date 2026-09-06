<!--
reps: 0
priority: 0
-->
#Java/IO/File #SRS

# Does a `java.io.File` instance represent only a path without opening the file?

> [!abstract] Short answer
> **Yes: `File` is an abstract pathname, not an open file.** Since Java 1.0 it stores a system-independent path (optional prefix plus name sequence). Constructors convert a string, parent/child pair, or `file:` URI; they do not open a connection and do not throw `FileNotFoundException` if the path is missing. The instance may denote no real file or directory. Opening bytes is a later step: `new FileInputStream(file)` creates a `FileDescriptor` and can fail.

## Pathname object versus an open connection

`File` implements `Serializable` and `Comparable<File>`. It is **not** `Closeable` / `AutoCloseable`. Construction is `new File(pathname)`, `new File(parent, child)`, `new File(File parent, String child)`, or `new File(URI)` (1.4). A `null` pathname or child is `NullPointerException`. The empty string is the empty abstract pathname. The pathname on the object never changes (`File` is immutable) ([[How would you explain the java.io.File class and path representation]], [[What character separates path components in the Java File API]]).

Relative names resolve, when needed, against `user.dir` (the JVM’s current user directory). Absolute vs relative is system-dependent (`/` on UNIX; drive plus `\\` or UNC `\\\\` on Windows).

That is still only a path. `exists()`, `isFile()`, `isDirectory()`, `length()`, `canRead()` **query** the filesystem when you call them. `createNewFile()`, `mkdir()`, `delete()`, `renameTo()` **mutate** it. None of those turn the `File` into a live handle, and none keep a stream you must close ([[How would you explain the AutoCloseable interface in Java]]).

Contrast `FileInputStream(File)`: it **opens a connection** to the file named by that `File`, allocates a `FileDescriptor`, and throws `FileNotFoundException` if the name does not exist, is a directory, or cannot be opened for reading. `close()` releases that connection ([[Which subclasses class InputStream you do you know for what they intended]], [[What is RandomAccessFile in Java]]).

`toPath()` builds a `java.nio.file.Path` from the same abstract path (default filesystem). `Path` is still a location, not an open channel.

```d2
direction: down
file: "java.io.File\nabstract pathname, immutable" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
maybe: "may denote nothing\non disk" {
  width: 240
  height: 55
  style.fill: "#fff8e1"
}
open: "FileInputStream(file)\nopens a connection" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
fail: "FileNotFoundException\nif it cannot be opened" {
  width: 260
  height: 55
  style.fill: "#ffebee"
}
file -> maybe
file -> open
open -> fail
```

**Fig. 1.** `new File(...)` names a path. Opening happens when `FileInputStream` is constructed from that name.

```java
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

class FileIsAPath {
    static boolean constructMissing() {
        File missing = new File("no-such-file-does-not-exist");
        return missing.exists();
    }

    static int openMissing() throws IOException {
        File missing = new File("no-such-file-does-not-exist");
        try (FileInputStream in = new FileInputStream(missing)) {
            return in.read();
        }
    }
}
```

**Listing 1.** `constructMissing` builds a `File` and asks `exists()` — typically `false`, no open. `openMissing` throws `FileNotFoundException` from the `FileInputStream` constructor. (`exists()` is not a reliable lock; another process can create the name in between.)

`getCanonicalPath()` / `getCanonicalFile()` are the exception people miss: they **do** filesystem work (remove `.` / `..`, resolve UNIX links, normalize Windows drive letters) and are declared `throws IOException`. That still returns another pathname, not an open stream. Canonical form of a missing path can change after the file is later created.

> [!warning] `new File` succeeding is not “the file is there”
> A `File` for a missing path is legal. `exists()` returning `true` can be stale a moment later. `createNewFile()` is the atomic create-if-absent (not a lock — use `FileLock`). `renameTo` changes the directory entry; the original `File` object still holds the old pathname. `equals` / `hashCode` compare **pathnames** (case rules follow the OS), not inode identity. Do not put a `File` in try-with-resources; close the stream you opened.

> [!tip] Interview answer
> Yes. `java.io.File` is an immutable abstract pathname; constructing it does not open anything and does not require the file to exist. `new FileInputStream(file)` is what opens a connection, creates a `FileDescriptor`, and can throw `FileNotFoundException`. Methods like `exists()` and `createNewFile()` talk to the filesystem, but the `File` object itself stays a path.
