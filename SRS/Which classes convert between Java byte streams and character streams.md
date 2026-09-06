<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# Which classes convert between Java byte streams and character streams?

> [!abstract] Short answer
> **`InputStreamReader` and `OutputStreamWriter` (Java 1.1) — the bridges.** `InputStreamReader` extends `Reader`: it reads **bytes** from an `InputStream` and **decodes** them to `char`s with a charset. `OutputStreamWriter` extends `Writer`: **characters written** are **encoded** to bytes on an `OutputStream`. Specify a `Charset`, a charset name, or a `CharsetDecoder`/`CharsetEncoder` (since 1.4). One-arg constructors use the **default charset**, or a `PrintStream`’s charset when wrapping one. Wrap with `BufferedReader` / `BufferedWriter` so the converter is not invoked on every tiny call ([[What is the difference between and what InputStream OutputStream Reader Writer]], [[What are buffered streams in Java]]).

## Decode inbound, encode outbound

| Direction | Class | Extends | Uses |
| --- | --- | --- | --- |
| Bytes → characters | `InputStreamReader` | `Reader` | charset **decoder** |
| Characters → bytes | `OutputStreamWriter` | `Writer` | charset **encoder** |

`getEncoding()` returns the historical name if there is one, else the canonical name, or **`null` after `close()`**. Named charset constructors throw `UnsupportedEncodingException` if the name is unknown. Both classes **replace** malformed and unmappable sequences with the charset default; use `CharsetDecoder` / `CharsetEncoder` for other error actions.

`OutputStreamWriter` accumulates **bytes** in a buffer; the **characters** you pass are not buffered there — hence `BufferedWriter`. `InputStreamReader.read` may read **ahead** more bytes than this call needs ([[What are buffered streams in Java]], [[How does Java]]).

`PrintStream` / `PrintWriter` also encode text, but they are print facades; this cue’s pair is the two bridges ([[What is the difference between PrintWriter and PrintStream]], [[What kinds of input and output streams exist in Java]]). For `System.in`, prefer `Console.charset()` (or `stdin.encoding`) ([[Can you redirect standard input and output streams in Java]], [[What kinds of input and output streams exist in Java]]).

```java
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;

class ByteCharBridges {
    static void copy(String from, String to) throws IOException {
        try (BufferedReader in = new BufferedReader(new InputStreamReader(
                new FileInputStream(from), StandardCharsets.UTF_8));
             BufferedWriter out = new BufferedWriter(new OutputStreamWriter(
                     new FileOutputStream(to), StandardCharsets.UTF_8))) {
            in.transferTo(out);
        }
    }
}
```

**Listing 1.** Named UTF-8 on both bridges, then buffered wrappers as the class docs recommend. Closing the outer reader/writer closes the files.

```d2
direction: down
bytes: "InputStream / OutputStream" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
isr: "InputStreamReader" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
osw: "OutputStreamWriter" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
chars: "Reader / Writer" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
bytes -> isr -> chars
chars -> osw -> bytes
```

**Fig. 1.** Conversion is these two classes, not `DataInputStream.readUTF` (modified UTF-8) and not NIO `Charset` used alone ([[Which class reads primitive values from a Java InputStream]]).

> [!warning] Default charset is not UTF-8, and `read()` returns characters
> `Reader.read()` yields `char`s / `-1`, not raw bytes. Omitting the charset constructor uses `Charset.defaultCharset()`. `getEncoding()` after `close()` may be `null`. These bridges are not `DataInputStream.readUTF`.

> [!tip] Interview answer
> Byte to character is `InputStreamReader`; character to byte is `OutputStreamWriter`. Always name the charset. Wrap them in `BufferedReader` and `BufferedWriter` so decoding is not done one character at a time.
