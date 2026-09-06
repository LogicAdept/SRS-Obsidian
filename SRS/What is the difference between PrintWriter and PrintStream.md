<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# What is the difference between `PrintWriter` and `PrintStream`?

> [!abstract] Short answer
> **`PrintStream` (1.0) is a byte `FilterOutputStream` that can also print values; `PrintWriter` (1.1) is a `Writer` for formatted text and has no raw-byte `write`.** Both swallow `IOException` from print methods and expose `checkError()`. Autoflush differs: `PrintStream` flushes after a byte array, after `println`, or when a `'\n'` byte/char is written; `PrintWriter` flushes only on `println` / `printf` / `format`, using the **platform line separator**, not whenever `'\n'` appears. JavaDoc: use `PrintWriter` when the job is **characters**, unencoded byte streams when the job is **bytes** ([[What is the difference between and what InputStream OutputStream Reader Writer]], [[What kinds of input and output streams exist in Java]]).

## Bytes that print vs a character writer

| | `PrintStream` | `PrintWriter` |
| --- | --- | --- |
| Extends | `FilterOutputStream` | `Writer` |
| Since | 1.0 | 1.1 |
| Raw bytes | `write(int)` / `write(byte[])` as given | **None** — use an unencoded `OutputStream` |
| Print API | `print` / `println` / `printf` | Same set (documented to match `PrintStream`) |
| Autoflush | byte array, `println`, or `'\n'` | only `println`, `printf`, `format` |
| Line break | `'\n'` triggers autoflush | platform line separator; `'\n'` in `print` does **not** autoflush |
| Errors | flag + `checkError()` | same; constructors may still throw |
| Wrap | `OutputStream` | `Writer` or `OutputStream` (via `OutputStreamWriter`) |

`System.out` / `System.err` are `PrintStream`s ([[Can you redirect standard input and output streams in Java]]). Characters you `print` on a `PrintStream` are still encoded to bytes (given charset, or the default). `PrintWriter(OutputStream)` builds that encoder for you. Both classes replace malformed/unmappable sequences with the charset default replacement ([[Which classes convert between Java byte streams and character streams]], [[What are common concrete InputStream and OutputStream implementations]]).

```java
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;

class PrintCompare {
    static void both(OutputStream bytes) {
        PrintStream ps = new PrintStream(bytes, true, StandardCharsets.UTF_8);
        PrintWriter pw = new PrintWriter(bytes, true, StandardCharsets.UTF_8);
        ps.write(0xFF);           // raw byte
        pw.print("line");         // characters; no autoflush yet
        pw.println();             // platform newline + flush if autoFlush
        boolean failed = pw.checkError() | ps.checkError();
    }
}
```

**Listing 1.** Same destination, different contracts. `write(0xFF)` exists only on the stream. `checkError()` is how you notice a failed write — `print` does not throw.

```d2
direction: down
ps: "PrintStream\nFilterOutputStream + print" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
pw: "PrintWriter\nWriter + print, no raw bytes" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
ps -> pw: "prefer Writer for text"
```

**Fig. 1.** Interview split: stream = bytes (and encoded prints); writer = characters only ([[What kinds of input and output streams exist in Java]], [[What are buffered streams in Java]]).

> [!warning] Autoflush is not “any newline,” and silence is not success
> Default `PrintStream(OutputStream)` / `PrintWriter(Writer)` are **without** automatic line flushing. `pw.print("a\n")` with autoflush **on** still does not flush. `ps.write('\n')` does. `println()` on `PrintWriter` writes `line.separator`, which may be `\r\n`. `PrintStream.write(byte[])` is declared `throws IOException` but print methods swallow errors and set `checkError()`. Never skip `checkError()` after a batch of prints. Do not send raw protocol bytes through `PrintWriter`. File constructors still throw.

> [!tip] Interview answer
> `PrintStream` is a byte stream that also prints; `PrintWriter` is a character writer with the same print methods and no byte `write`. Both hide I/O exceptions behind `checkError()`. Autoflush on the writer is only `println`/`printf`/`format`; the stream also flushes on `'\n'` and byte-array writes. Prefer `PrintWriter` for text.
