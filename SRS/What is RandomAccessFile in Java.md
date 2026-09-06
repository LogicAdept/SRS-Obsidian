<!--
reps: 0
priority: 0
-->
#Java/IO/RandomAccessFile #OperatingSystems/IO/Files #SRS

# What is `RandomAccessFile` in Java?

> [!abstract] Short answer
> **`RandomAccessFile` (Java 1.0) is a bidirectional file with a movable file pointer — not an `InputStream` or `OutputStream`, not `java.util.Random`, and not the Stream API.** It implements `DataInput`, `DataOutput`, and `Closeable`. The file acts like a big byte array; `getFilePointer()` / `seek(long)` read and set the cursor. Constructors take a path or `File` **and a mode**: `"r"`, `"rw"`, `"rws"`, or `"rwd"`. Writes in `"r"` throw `IOException`. `read()` at EOF returns `-1` like a stream; `readInt()` and friends throw `EOFException`.

## A cursor, not a stream hierarchy

It extends `Object`. Opening creates a `FileDescriptor`. `"rw"` (and `rws`/`rwd`) can **create** the file; `"r"` requires an existing regular file or you get `FileNotFoundException`. A bad mode is `IllegalArgumentException` ([[What file access modes does RandomAccessFile support]], [[Does a java.io.File instance represent only a path without opening the file]]).

| Mode | Meaning |
| --- | --- |
| `"r"` | Read only; any `write` → `IOException` |
| `"rw"` | Read and write; create if missing |
| `"rws"` | Like `"rw"`, every update to **content and metadata** forced to storage (like `FileChannel.force(true)` on every I/O) |
| `"rwd"` | Like `"rw"`, force **content** only (`force(false)` style) |

Local-device `rws`/`rwd`: when a method returns, that invocation’s changes are on the device (crash durability). No such guarantee for a remote file. `"rwd"` typically does fewer low-level I/Os than `"rws"`.

**Pointer.** Input reads at the pointer and advances it; in read/write mode, output writes at the pointer and advances it. Writing past EOF **extends** the file. `seek(pos)` is from the start; `pos` **may be past EOF** without changing `length()` — the file grows only if you then write. `setLength(newLength)` truncates or extends (extended bytes are undefined); if the pointer was past the new length, it is moved to `newLength`. `skipBytes(n)` **attempts** to skip; it may skip fewer (including zero), **never** throws `EOFException`, and skips nothing if `n < 0` ([[How would you explain the java.io.File class and path representation]], [[How would you explain advantages of Java NIO over classic blocking IO]]).

**DataInput / DataOutput.** `readBoolean` / `readInt` / `readUTF` / `writeByte` / … are the primitive and modified-UTF contracts. Class-level rule: those reading routines throw `EOFException` if EOF hits before enough bytes. Contrast `read()` / `read(byte[])`: documented to match `InputStream.read` (`0..255` or `-1`, blocks). `readFully` keeps reading until the exact count or EOF/error.

`readLine()` is **not** Unicode: each byte becomes a `char` with the high eight bits zero. Terminators `\r`, `\n`, `\r\n`, or EOF; terminators are dropped. `readUTF()` is modified UTF-8 with a two-byte length prefix (`UTFDataFormatException` if invalid).

`getChannel()` returns the **unique** `FileChannel` for this file; its position tracks `getFilePointer()` both ways. `close()` cannot be reopened and closes that channel too. You cannot wrap this in `InputStreamReader` ([[How does Java]], [[Which class reads primitive values from a Java InputStream]]).

```d2
direction: down
raf: "RandomAccessFile\nDataInput + DataOutput + Closeable" {
  width: 340
  height: 55
  style.fill: "#e3f2fd"
}
ptr: "file pointer\ngetFilePointer / seek" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
not: "not InputStream / OutputStream" {
  width: 280
  height: 45
  style.fill: "#fff8e1"
}
raf -> ptr
raf -> not
```

**Fig. 1.** One open file, a cursor you can move, stream-like `read()` plus `DataInput` primitives. No place in the byte-stream class tree.

```java
import java.io.EOFException;
import java.io.IOException;
import java.io.RandomAccessFile;

class RafDemo {
    static int readIntAt(String path, long offset) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile(path, "r")) {
            raf.seek(offset);
            return raf.readInt();
        }
    }

    static void appendByte(String path, int b) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile(path, "rw")) {
            raf.seek(raf.length());
            raf.write(b);
        }
    }
}
```

**Listing 1.** `"r"` plus `seek` then `readInt()` (EOF → `EOFException`, not `-1`). `"rw"` plus `seek(length())` appends. Catch `EOFException` separately from a closed-file `IOException` if that matters.

> [!warning] `read()` EOF is not `readInt()` EOF, and `readLine` is not text
> `read()` returns `-1` at end; `readInt()` / `readFully` throw `EOFException`. `skipBytes` can skip **fewer** than `n`. `seek` past EOF does not grow the file until a write. `readLine()` cannot represent characters above `0xFF`. You cannot wrap this in `InputStreamReader`. Closing the `RandomAccessFile` closes its `FileChannel`. Dump talk of “mostly native methods” is not in the JavaDoc — treat the class as the `DataInput`/`DataOutput` file with a pointer.

> [!tip] Interview answer
> `RandomAccessFile` is not in the stream hierarchy: it is a file plus a pointer you `seek`, with `DataInput` and `DataOutput` on the same object. You must pass a mode — `"r"` or `"rw"` at minimum, plus `"rws"` / `"rwd"` for synchronous writes. `read()` looks like `InputStream`; the typed `readXxx` methods throw `EOFException` instead of returning `-1`.
