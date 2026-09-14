<!--
reps: 0
priority: 0
-->
#Java/NIO/Files #SRS

# How do you read and write files with the Files utility class in Java?

> [!abstract] Short answer
> **`java.nio.file.Files` is the static facade over `Path`: one-shot helpers for small files (`readAllBytes`, `readAllLines`, `readString`, `write`, `writeString`), stream-style helpers for big ones (`newInputStream`, `newBufferedReader`, `lines()`), plus `copy`, `move`, `delete`, `createDirectories`, `walk`, `find`, and attribute readers — everything throwing `IOException` with a cause and taking `StandardOpenOption` varargs.** The javadoc gates the one-shots: "intended for simple cases" and "not intended for reading in large files" ([[What is the difference between the java.io.File class and the java.nio.file.Path interface]], [[How does file reading work in Java]]).

## Small files vs streams

`readAllBytes` / `readString` / `readAllLines` load the whole content into memory — perfect for configs, wrong for gigabyte logs. The streaming side returns a closeable view: `newBufferedReader(path, cs)`, `newInputStream(path, options...)`, and `Files.lines(path)` which is a lazy `Stream<String>` **backed by the open file** — it must be closed (try-with-resources), or the channel leaks. The same split holds for writes: `write`/`writeString` create or truncate in one call; `newOutputStream` with `APPEND` / `CREATE` / `TRUNCATE_EXISTING` composes the mode.

| Task | One call | Notes |
| --- | --- | --- |
| Read small text | `readString(path)` | UTF-8 default; charset overload exists |
| Read big text | `newBufferedReader` / `lines()` | close the stream |
| Write/append | `writeString(path, s, APPEND)` | options compose |
| Copy | `copy(from, to, REPLACE_EXISTING)` | last-modified copyable via `COPY_ATTRIBUTES` |
| Move/rename | `move(from, to, ATOMIC_MOVE)` | may throw `AtomicMoveNotSupportedException` |
| Delete | `delete` / `deleteIfExists` | fails on non-empty directory |

`copy` and `move` accept option varargs: `REPLACE_EXISTING` (target may be replaced), `COPY_ATTRIBUTES`, `ATOMIC_MOVE` (move only). Without `REPLACE_EXISTING`, an existing target fails the call — a deliberate foot-gun against silent overwrites.

```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.stream.Stream;

class FilesDemo {
    public static void main(String[] args) throws IOException {
        Path p = Path.of("/tmp/notes.txt");
        Files.writeString(p, "first\nsecond\n");
        Files.writeString(p, "third\n", java.nio.file.StandardOpenOption.APPEND);
        try (Stream<String> lines = Files.lines(p)) {
            System.out.println("lines: " + lines.count());
        }
        Path dst = Path.of("/tmp/notes-copy.txt");
        Files.copy(p, dst, StandardCopyOption.REPLACE_EXISTING);
        System.out.println("copy size: " + Files.readString(dst).length());
        System.out.println("walk finds " + Files.find(p.getParent(), 1,
                (path, attr) -> attr.isRegularFile()).count() + " files at depth 1");
    }
}
```

**Listing 1.** Write, append, lazy line count, copy, and a depth-bounded find:

```text
lines: 3
copy size: 19
walk finds 2 files at depth 1
```

**Listing 2.** One-shot writes, a closed streaming read, and a bounded walk in one program.

```d2
direction: down
small: "readString / writeString\nwhole file in memory" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
big: "newBufferedReader / lines()\nstreaming, must close" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
fs: "copy / move / delete / walk\n+ OpenOption varargs" {
  width: 300
  height: 55
  style.fill: "#fff8e1"
}
small -> fs
big -> fs
```

**Fig. 1.** Pick the row by file size: one-shots for small, streams for big, operations for everything ([[How do you watch a directory for changes in Java]]).

> [!warning] Convenience bites on large inputs and silent targets
> `readAllBytes` on a multi-gigabyte file is an `OutOfMemoryError` in waiting — the javadoc explicitly scopes it to simple cases. `Files.lines` holds an open channel: without try-with-resources you leak descriptors and the JVM may not release the file. `copy`/`move` refuse to clobber unless you pass `REPLACE_EXISTING`; `move` with `ATOMIC_MOVE` may be rejected by the platform as `AtomicMoveNotSupportedException`. `delete` throws `NoSuchFileException` where `deleteIfExists` shrugs, and neither removes a non-empty directory. Defaults are UTF-8 since JDK 18 (JEP 400) — pass an explicit charset for anything user-controlled.

> [!tip] Interview answer
> `Files` gives one-call helpers (`readString`, `writeString`, `readAllBytes/lines`) that are fine for small files, stream helpers (`newBufferedReader`, `lines()`, `newInputStream`) that need closing for big ones, and filesystem operations (`copy`/`move` with `REPLACE_EXISTING`/`ATOMIC_MOVE`, `deleteIfExists`, `walk`/`find`). Everything throws `IOException` with the real cause and composes through `OpenOption` varargs.

