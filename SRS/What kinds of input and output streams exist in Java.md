<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #Java/NIO #OperatingSystems/IO/Streams #SRS

# What kinds of input and output streams exist in Java?

> [!abstract] Short answer
> **Three cuts, all in `java.io`.** **Direction:** input vs output. **Unit:** **bytes** (`InputStream` / `OutputStream`, Java 1.0) vs **characters** (`Reader` / `Writer`, 1.1). **Role:** a **source or sink** (file, byte array, sequence) vs a **filter** (`FilterInputStream` / `FilterOutputStream` and the `Writer` wrappers) that adds buffering, pushback, data primitives, or encoding. Bridges (`InputStreamReader` / `OutputStreamWriter`) sit on the byte side and speak characters. This is not `java.util.stream`, not NIO `Channel`/`Buffer`, and not `RandomAccessFile` ([[What is the difference between and what InputStream OutputStream Reader Writer]]).

## Byte vs character, then node vs filter

| | Input | Output |
| --- | --- | --- |
| Bytes | `InputStream` — subclass supplies `read()` of the next byte (`-1` = EOF) | `OutputStream` — `write(int)` of the low 8 bits; `Flushable` |
| Characters | `Reader` | `Writer` (`Appendable`, `Flushable`) |

A `byte` is not a `char`. Text needs a charset on the bridge ([[Which classes convert between Java byte streams and character streams]], [[How does Java]]).

**Node (connects to a place).** `FileInputStream` / `FileOutputStream` open a `FileDescriptor`. `ByteArrayInputStream` / `ByteArrayOutputStream` keep a `byte[]` (`close()` is a no-op). `SequenceInputStream` concatenates other streams ([[What are common concrete InputStream and OutputStream implementations]], [[What is SequenceInputStream]]).

**Filter (wraps another stream).** `FilterInputStream` / `FilterOutputStream` hold `in` / `out` and forward. Subclasses: `Buffered*`, `DataInputStream`, `PushbackInputStream`, `PrintStream`, zip deflate/GZIP/ZIP filters (`java.util.zip`). `Deflater` / `Inflater` are ZLIB engines, not streams. Character side: `BufferedReader` / `BufferedWriter`, `PrintWriter`. Close (or `flush`) the **outer** decorator ([[What are buffered streams in Java]], [[What is PushbackInputStream]], [[Which Java classes read and write compressed streams]]).

`PrintStream` is still a **byte** stream that can print; `PrintWriter` is a `Writer` with no raw-byte `write` ([[What is the difference between PrintWriter and PrintStream]]). `ObjectInputStream` is a filter that **deserializes** — untrusted bytes are dangerous. `RandomAccessFile` is a seekable file, not in this tree ([[What is RandomAccessFile in Java]]).

**Not these “streams.”** `java.util.stream.Stream` is a lazy collection pipeline. `java.nio` is buffers and channels (`FileChannel` is not selectable). `Files.newInputStream` still returns a `java.io.InputStream` ([[How would you explain in how is difference between IO and NIO]], [[Which subclasses class InputStream you do you know for what they intended]]).

```java
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

class Kinds {
    static String firstLine(String path) throws IOException {
        try (FileInputStream bytes = new FileInputStream(path);          // node, bytes
             InputStreamReader chars = new InputStreamReader(bytes, StandardCharsets.UTF_8); // bridge
             BufferedReader buf = new BufferedReader(chars)) {           // filter, characters
            return buf.readLine();
        }
    }
}
```

**Listing 1.** One path, three kinds stacked: file source → charset bridge → buffered character filter. Closing `buf` closes the chain.

```d2
direction: down
byte: "InputStream / OutputStream\nbytes" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
char: "Reader / Writer\ncharacters" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
role: "node (file, array)\nor filter (buffer, pushback)" {
  width: 300
  height: 50
  style.fill: "#fff8e1"
}
byte -> char: "InputStreamReader / OutputStreamWriter"
byte -> role
char -> role
```

**Fig. 1.** Interview taxonomy: unit, then wrapper vs endpoint. Do not start with “NIO is another stream class.”

> [!warning] `java.util.stream` is the wrong “stream”
> Saying “map/filter/collect” here fails the I/O question. `available()` is not file length. Filters do not replace the four roots — they wrap them. `System.in` / `out` / `err` are a `InputStream` and two `PrintStream`s, still this model ([[Can you redirect standard input and output streams in Java]]).

> [!tip] Interview answer
> Java I/O streams split by direction and by byte versus character: `InputStream`/`OutputStream` and `Reader`/`Writer`. Then you wrap those with filters for buffering, data types, or pushback, and you bridge with `InputStreamReader` when text needs a charset. NIO channels and the Stream API are different APIs with the same English word.
