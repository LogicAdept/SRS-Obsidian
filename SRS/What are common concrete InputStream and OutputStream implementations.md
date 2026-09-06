<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# What are common concrete `InputStream` and `OutputStream` implementations?

> [!abstract] Short answer
> **Sources vs filters, then the print/serialize extras.** `InputStream` / `OutputStream` (Java 1.0) are abstract: a subclass supplies `read()` of the next byte or `write(int)` of the low 8 bits. Direct sources: `FileInputStream` / `FileOutputStream`, `ByteArrayInputStream` / `ByteArrayOutputStream`, `SequenceInputStream`. Decorators via `FilterInputStream` / `FilterOutputStream`: `Buffered*`, `DataInputStream`, `PushbackInputStream`, `PrintStream`. `ObjectInputStream` deserializes graphs — **untrusted bytes are dangerous**. This is `java.io`, not `java.util.stream`.

## Byte sources, then wrappers

`FileInputStream` **opens a connection** to a named file (`FileDescriptor`); missing or unreadable → `FileNotFoundException`. `FileOutputStream` writes raw bytes to a `File` / name / descriptor; `append == true` writes at the end (1.1 / 1.4 overloads). Some platforms allow only one writer at a time. Close via try-with-resources ([[Does a java.io.File instance represent only a path without opening the file]], [[How does Java]]).

`ByteArrayInputStream` reads an existing `byte[]` (**not copied**). `read` **cannot block**. `close()` has **no effect**. `markSupported()` is `true`. `ByteArrayOutputStream` grows a buffer (initial capacity **32** if unspecified); retrieve with `toByteArray()` / `toString(Charset)`. `close()` is also a no-op. `toString()` without a charset uses the **default charset**; `toString(int hibyte)` is deprecated.

`SequenceInputStream` concatenates streams: two-arg (`s1` then `s2`) or an `Enumeration<InputStream>`. On EOF it **closes** the current substream and switches. `close()` on an enumeration constructor closes **remaining** streams ([[What is SequenceInputStream]]).

`FilterInputStream` wraps `in` and forwards; subclasses add behavior ([[What are buffered streams in Java]]):

| Class | Role |
| --- | --- |
| `BufferedInputStream` / `BufferedOutputStream` | Internal `buf`; refill / flush in chunks; BIS `mark`/`reset` |
| `DataInputStream` | `DataInput` primitives, machine-independent; **not** thread-safe; `readLine` **deprecated** (use `BufferedReader`). Pair: `DataOutputStream` ([[Which class reads primitive values from a Java InputStream]]) |
| `PushbackInputStream` | `unread` into a pushback buffer; default **1 byte**; `markSupported` is **false** ([[What is PushbackInputStream]]) |
| `PrintStream` | Print onto an `OutputStream`; charset; swallows write `IOException` into `checkError()` ([[What is the difference between PrintWriter and PrintStream]]) |

`ObjectInputStream` extends `InputStream` (not `FilterInputStream`) and deserializes what `ObjectOutputStream` wrote. Only `Serializable` / `Externalizable` types. JavaDoc warning: deserialization of **untrusted** data is inherently dangerous; use filters (`ObjectInputFilter`). Pair with `FileInputStream` / `FileOutputStream` for a file graph.

`RandomAccessFile` is **not** an `InputStream` ([[What is RandomAccessFile in Java]]). Character bridges are `InputStreamReader` / `OutputStreamWriter`, not byte-stream subclasses ([[What is the difference between and what InputStream OutputStream Reader Writer]], [[Which subclasses class InputStream you do you know for what they intended]]).

```d2
direction: down
in: "InputStream" {
  width: 160
  height: 35
  style.fill: "#e3f2fd"
}
out: "OutputStream" {
  width: 160
  height: 35
  style.fill: "#e3f2fd"
}
src: "File / ByteArray / Sequence / Object" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
fil: "Filter*\nBuffered / Data / Pushback / PrintStream" {
  width: 340
  height: 50
  style.fill: "#e8f5e9"
}
in -> src
out -> src
in -> fil
out -> fil
```

**Fig. 1.** Sources hold data or a file connection. `Filter*` wrap another stream. `ObjectInputStream` is a source-style `InputStream`, not a `FilterInputStream`.

```java
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;

class CopyBytes {
    static void copy(String from, String to) throws IOException {
        try (BufferedInputStream in = new BufferedInputStream(new FileInputStream(from));
             BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(to))) {
            in.transferTo(out);
        }
    }
}
```

**Listing 1.** Interview wrap: file source plus buffered filters. `transferTo` does not close either stream; try-with-resources does.

> [!warning] `close()` is not always a close, and `ObjectInputStream` is not a parser
> `ByteArrayInputStream` / `ByteArrayOutputStream` ignore `close()` — you can still `read`/`write`. `FileInputStream` / `FileOutputStream` really open OS connections. `DataInputStream.readLine()` is deprecated and does not convert bytes to characters correctly. `PushbackInputStream` is not `mark`/`reset`. Never `readObject` on bytes you do not trust. `PrintStream` is still bytes-with-charset, not a `Writer`.

> [!tip] Interview answer
> Recite sources (`File`, `ByteArray`, `Sequence`, `Object`) and filters (`Buffered`, `Data`, `Pushback`, `PrintStream`). `InputStream`/`OutputStream` are the abstract byte roots; you wrap a file stream in `Buffered*` for real I/O. Name `FilterInputStream` as the decorator base. Say `ObjectInputStream` is a security hazard on untrusted data, and `RandomAccessFile` is a different type.
