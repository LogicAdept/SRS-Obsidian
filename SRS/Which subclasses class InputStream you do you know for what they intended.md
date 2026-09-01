<!--
reps: 0
priority: 0
-->
#Java/IO #SRS

# Which subclasses class `InputStream` you do you know for what they intended?

> [!abstract] Short answer
> **`InputStream` is the abstract byte-input root (Java 1.0).** Directly useful types: `FileInputStream` (file bytes), `ByteArrayInputStream` (in-memory `byte[]`), `PipedInputStream` (pair with `PipedOutputStream`), `SequenceInputStream` (concatenate), `ObjectInputStream` (deserialize — untrusted data is dangerous). Decorators via `FilterInputStream`: `BufferedInputStream` (`mark`/`reset`), `DataInputStream` (primitives), `PushbackInputStream` (`unread`). **`StringBufferInputStream` is deprecated** — use `StringReader`. This is `java.io`, not `java.util.stream`.

## Byte-input tree, then the usual interview extras

`InputStream`: superclass of all **byte** input streams; a subclass must supply the next byte ([[What is the difference between and what InputStream OutputStream Reader Writer]], [[What kinds of input and output streams exist in Java]], [[What are common concrete InputStream and OutputStream implementations]]).

`java.io` package one-liners (dump list, checked):

| Class | Intended for |
| --- | --- |
| `FileInputStream` | Bytes from a file |
| `ByteArrayInputStream` | Internal buffer of bytes as the source |
| `FilterInputStream` | Wrap another stream; transform or add behavior |
| `BufferedInputStream` | Buffer + `mark`/`reset` ([[How would you explain buffered streams in Java IO]]) |
| `DataInputStream` | Primitive types from an underlying stream, machine-independent ([[Which class reads primitive values from a Java InputStream]]) |
| `PushbackInputStream` | `unread` into a pushback buffer — you still `read`, then put back; default 1 byte ([[What is PushbackInputStream]]) |
| `SequenceInputStream` | Logical concatenation of other `InputStream`s ([[What is SequenceInputStream]]) |
| `PipedInputStream` | Connected to a `PipedOutputStream`; reads what the pipe writes |
| `ObjectInputStream` | Deserialize primitives and objects previously written by `ObjectOutputStream` |

**Do not use `StringBufferInputStream`:** deprecated; it incorrectly treats bytes as characters. Prefer `StringReader`.

Dump also asked the other three roots — same package:

**`OutputStream`:** `FileOutputStream`, `ByteArrayOutputStream`, `FilterOutputStream` → `BufferedOutputStream`, `DataOutputStream`, `PrintStream` (`print`/`println`), `PipedOutputStream`, `ObjectOutputStream`.

**`Reader`:** `InputStreamReader` (bytes→chars + charset) ([[Which classes convert between Java byte streams and character streams]]), `FileReader`, `BufferedReader`, `CharArrayReader`, `StringReader`, `PipedReader`, `PushbackReader`, `LineNumberReader` (counts lines), `FilterReader`.

**`Writer`:** `OutputStreamWriter` encodes **characters to bytes** (dump had the direction backwards), `FileWriter`, `BufferedWriter`, `CharArrayWriter`, `StringWriter`, `PipedWriter`, `PrintWriter` ([[What is the difference between PrintWriter and PrintStream]]), `FilterWriter`.

```d2
direction: down
root: "InputStream" {
  width: 160
  height: 35
  style.fill: "#e3f2fd"
}
src: "File / ByteArray / Piped\nSequence / Object" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
fil: "FilterInputStream\nBuffered / Data / Pushback" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
root -> src
root -> fil
```

**Fig. 1.** Sources vs `FilterInputStream` decorators. `StringBufferInputStream` is omitted on purpose (deprecated).

```java
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.IOException;

class Demo {
    static int firstByte(String path) throws IOException {
        try (BufferedInputStream in = new BufferedInputStream(new FileInputStream(path))) {
            return in.read();
        }
    }
}
```

**Listing 1.** Typical wrap: `FileInputStream` for the file, `BufferedInputStream` for buffering and `mark`/`reset`.

> [!warning] Deprecated string-as-bytes, deserialization, and `java.util.stream`
> `StringBufferInputStream` is deprecated. `ObjectInputStream` on untrusted bytes is a security hazard (package serialization warning). `PushbackInputStream` is not a non-consuming peek. `OutputStreamWriter` writes **chars as encoded bytes**, not “bytes to chars.” None of these types are `java.util.stream.Stream`.

> [!tip] Interview answer
> Recite **sources** (`File`, `ByteArray`, `Piped`, `Sequence`, `Object`) and **filters** (`Buffered`, `Data`, `Pushback`). Name `FilterInputStream` as the decorator base. Add `StringReader` instead of `StringBufferInputStream`. If they ask all four trees, pair each with its `OutputStream` / `Reader` / `Writer` twin and the charset bridges.
