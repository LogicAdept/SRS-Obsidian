<!--
reps: 0
priority: 0
-->
#Java/IO/RandomAccessFile #OperatingSystems/IO/Files #SRS

# What file access modes does RandomAccessFile support?

> [!abstract] Short answer
> **Four mode strings, constructor argument only:** `"r"`, `"rw"`, `"rws"`, `"rwd"`. Anything else is `IllegalArgumentException`. `"r"` is read-only (any `write` → `IOException`; missing file → `FileNotFoundException`). `"rw"` reads and writes and **creates** if the path is absent. `"rws"` / `"rwd"` are `"rw"` plus a **synchronous** flush of every update to the storage device: content **and metadata**, or **content only**. They behave like `FileChannel.force(true)` / `force(false)` except they apply on **every** I/O ([[What is RandomAccessFile in Java]]).

## The `mode` argument

Constructors: `RandomAccessFile(String name, String mode)` and `RandomAccessFile(File file, String mode)`. Opening creates a `FileDescriptor`. `RandomAccessFile` is not in the `InputStream` / `OutputStream` tree; mode is how you get write access at all ([[Does a java.io.File instance represent only a path without opening the file]]).

| Mode | Opens | Missing file | Durability |
| --- | --- | --- | --- |
| `"r"` | Read only | `FileNotFoundException` | n/a |
| `"rw"` | Read and write | Attempt to **create** | Ordinary buffered I/O |
| `"rws"` | Same as `"rw"` | Same create rule | Every update to **content and metadata** written synchronously |
| `"rwd"` | Same as `"rw"` | Same create rule | Every update to **content** written synchronously |

Modes that **begin with** `"rw"` share the create-or-fail `FileNotFoundException` rule: not an existing writable regular file, and a new regular file cannot be created. `"r"` requires an existing regular file.

**Why two sync modes.** On a **local** device, when a method returns, that invocation’s changes are on the device (crash durability). **No** such guarantee if the file is remote. `"rwd"` skips metadata updates and usually costs **at least one fewer** low-level I/O than `"rws"`. Sync modes are often **more** efficient than calling `FileChannel.force` after each write because they are built into every operation ([[How would you explain advantages of Java NIO over classic blocking IO]], [[How would you explain the java.io.File class and path representation]]).

```java
import java.io.IOException;
import java.io.RandomAccessFile;

class RafModes {
    static void readOnly(String path) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile(path, "r")) {
            raf.read(); // write() would throw IOException
        }
    }

    static void createAndWrite(String path) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile(path, "rw")) {
            raf.writeInt(1);
        }
    }

    static void durableContent(String path) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile(path, "rwd")) {
            raf.writeInt(2); // content synced when write returns (local device)
        }
    }
}
```

**Listing 1.** `"r"` vs `"rw"` vs `"rwd"`. Catch `FileNotFoundException` when `"r"` points at a missing path. A typo like `"read"` is `IllegalArgumentException`, not `FileNotFoundException`.

```d2
direction: down
r: "r\nread only" {
  width: 160
  height: 45
  style.fill: "#e3f2fd"
}
rw: "rw\nread + write + create" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
sync: "rws / rwd\nrw + sync every I/O" {
  width: 220
  height: 50
  style.fill: "#fff8e1"
}
rw -> sync
```

**Fig. 1.** Four strings. Sync modes are `"rw"` plus forced storage, not extra letters for “shared” or “sequential.”

> [!warning] `"rws"` is not “read-write-shared”
> The extra `s` is **synchronous** (content + metadata). `"rwd"` is content-only. Neither is a lock, `SHARE_DELETE`, or NIO `StandardOpenOption.SYNC` spelled differently — use these four literals. Do not invent `"w"` or `"a"`. Writes in `"r"` fail with `IOException`, not a compile error. Sync guarantees apply to a **local** device only. Both sync modes open **as with `"rw"`**, not “like each other except metadata.”

> [!tip] Interview answer
> `RandomAccessFile` takes `"r"`, `"rw"`, `"rws"`, or `"rwd"`. Read-only versus read-write, and the last two force every update to disk — metadata included, or content only. A wrong string is `IllegalArgumentException`; `"r"` on a missing file is `FileNotFoundException`.
