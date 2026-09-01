<!--
reps: 0
priority: 0
-->
#Java/IO #SRS

# What is the difference between and what `InputStream` `OutputStream` `Reader` `Writer`?

> [!abstract] Short answer
> **Bytes vs characters, and in vs out.** `InputStream` / `OutputStream` (Java 1.0) are abstract **byte** streams (`read`/`write` of 8-bit values). `Reader` / `Writer` (Java 1.1) are abstract **character** streams (`char` / `char[]` / `String`). All four are sequential I/O, `Closeable` / try-with-resources. They are **not** `java.util.stream`. Bridge bytes↔chars with `InputStreamReader` / `OutputStreamWriter` and a **charset**. Dump’s “Unicode” is the character family, not a fourth type.

## Four abstract roots, two axes

| | Input | Output |
| --- | --- | --- |
| **Bytes** | `InputStream` — superclass of byte input; subclass must supply the next **byte** (`read()` → `0..255` or `-1`) | `OutputStream` — superclass of byte output; subclass must `write(int)` (low 8 bits) |
| **Characters** | `Reader` — abstract character input; subclass must implement `read(char[],int,int)` and `close()` | `Writer` — abstract character output; subclass must implement `write(char[],int,int)`, `flush()`, `close()` |

**In common:** sequential “stream” I/O (not random access), `close()` releases resources, `AutoCloseable` so try-with-resources applies. Output types also implement `Flushable`. `Writer` is `Appendable`. `Reader` is `Readable`. Closed streams throw `IOException` on further I/O.

**Difference that interviews want:** a `byte` is not a `char`. Text files, consoles, and XML need a charset. `InputStreamReader` is the documented **bridge from byte streams to character streams**: it reads bytes and **decodes** them with a named charset, a `Charset`, or the default. The reverse direction is `OutputStreamWriter` ([[Which classes convert between Java byte streams and character streams]], [[What kinds of input and output streams exist in Java]]).

`Reader.read()` returns a character as an `int` in `0..65535` (`char`’s range) or `-1`. That is UTF-16 code units in the language, not “a Unicode stream type.” Encoding lives at the bridge, not on `InputStream` itself.

Concrete trees: `FileInputStream`, `BufferedInputStream`, `PushbackInputStream`, `SequenceInputStream` under bytes; `FileReader`, `BufferedReader`, `InputStreamReader` under chars; `PrintStream` vs `PrintWriter` on the output side ([[What are common concrete InputStream and OutputStream implementations]], [[How would you explain buffered streams in Java IO]], [[What is the difference between PrintWriter and PrintStream]], [[What is PushbackInputStream]], [[What is SequenceInputStream]]).

```d2
direction: down
bytes: "InputStream / OutputStream\n(byte)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
bridge: "InputStreamReader / OutputStreamWriter\n(Charset)" {
  width: 300
  height: 55
  style.fill: "#fff8e1"
}
chars: "Reader / Writer\n(char)" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
bytes -> bridge
bridge -> chars
```

**Fig. 1.** Byte roots (1.0) and character roots (1.1), joined by a charset bridge.

```java
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

class Demo {
    static String firstLine(InputStream bytes) throws java.io.IOException {
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(bytes, StandardCharsets.UTF_8))) {
            return in.readLine();
        }
    }
}
```

**Listing 1.** JavaDoc’s efficiency hint: wrap `InputStreamReader` in `BufferedReader`. The charset is explicit; do not treat raw `InputStream.read()` as text.

> [!warning] Do not read text as bytes, and this is not the Stream API
> `InputStream.read()` is one **byte** (or `-1`), not one Unicode scalar. Mixing `PrintStream` (bytes, default charset traps) with `Writer` on the same sink is a separate mess. `Writer.close()` **flushes first**; `OutputStream`’s default `close()` is a no-op until a subclass overrides. Never confuse these four with `java.util.stream.Stream`.

> [!tip] Interview answer
> **`InputStream`/`OutputStream` = bytes in/out; `Reader`/`Writer` = characters in/out.** Same idea: sequential closeable streams. Convert with `InputStreamReader`/`OutputStreamWriter` and a charset. Name `Closeable` and “not `java.util.stream`.”
