<!--
reps: 0
priority: 0
-->
#Java/IO #SRS

# How would you explain the difference between `PrintWriter` and `PrintStream`?

> [!abstract] Short answer
> **`PrintStream` is a byte `OutputStream` that prints; `PrintWriter` is a character `Writer` that prints.** JavaDoc tells you to use `PrintWriter` when you need characters, not bytes. Both swallow `IOException` on write and expose `checkError()`. Autoflush, when enabled, is **not** the same: `PrintStream` also flushes on `'\n'`; `PrintWriter` flushes only on `println` / `printf` / `format`.

## Bytes vs characters, then a quieter autoflush

`PrintStream` (Java 1.0) extends `FilterOutputStream`. It prints values onto another **output stream**. Characters are encoded to bytes with a charset (or the default). It has `write` for raw bytes. Use unencoded byte streams for raw bytes; use `PrintWriter` when the job is **characters** ([[What is the difference between and what InputStream OutputStream Reader Writer]], [[What kinds of input and output streams exist in Java]], [[What is the difference between PrintWriter and PrintStream]]).

`PrintWriter` (Java 1.1) extends `Writer`. It implements the same `print` family as `PrintStream` but **has no raw-byte writes**. Wrap a `Writer`, or an `OutputStream` (it builds an `OutputStreamWriter`). `println` / `printf` / `format` use the **platform line separator**, not a bare `'\n'`.

Neither print method throws `IOException`. Errors set an internal flag; `checkError()` flushes if still open and returns whether an I/O failure (or `setError()`) happened. `PrintWriter` constructors **may** throw (file/charset). `PrintStream.write(byte[])` is declared `throws IOException` but the API note says it never actually throws — it sets the flag like the rest.

Autoflush is a constructor flag (many constructors default to **off**). If on:

- `PrintStream` — flush after a **byte array** write, a `println`, or a newline **character or byte** `'\n'`.
- `PrintWriter` — flush only on `println`, `printf`, or `format`, **not** whenever a newline happens to be written.

`flush()` is always available on both to flush explicitly. Both replace malformed/unmappable sequences with the charset default replacement.

```d2
direction: down
job: "formatted print" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
ps: "PrintStream\nFilterOutputStream\nbytes + charset" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
pw: "PrintWriter\nWriter\ncharacters" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
job -> ps
job -> pw
```

**Fig. 1.** Same print API, different spine: bytes vs characters. Autoflush rules differ when the flag is on.

```java
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;

class Demo {
    static PrintStream bytes(OutputStream out, boolean autoFlush) {
        return new PrintStream(out, autoFlush, StandardCharsets.UTF_8);
    }

    static PrintWriter chars(Writer out, boolean autoFlush) {
        return new PrintWriter(out, autoFlush);
    }

    static boolean failed(PrintWriter w) {
        return w.checkError();
    }
}
```

**Listing 1.** `PrintStream` wraps an `OutputStream` and a charset. `PrintWriter` wraps a `Writer`. `checkError()` is how you notice a swallowed I/O failure.

> [!warning] Autoflush is optional and not “every `print`”
> Default `PrintStream(OutputStream)` / `PrintWriter(Writer)` are **without** automatic line flushing. `print()` does not flush a `PrintStream` unless autoflush is on **and** a `'\n'` is written (or you called `println` / wrote a byte array). `PrintWriter` will not flush on a `'\n'` inside `print("a\nb")` even with autoflush — only `println` / `printf` / `format`. Relying on `print()` to flush is wrong for both.

> [!warning] “Never throws” is write methods, not constructors — and not only `PrintWriter`
> `PrintStream` also never throws `IOException` from its print/write path; `checkError()` is required on **both**. File constructors still throw `FileNotFoundException` / `IOException` / `UnsupportedEncodingException`. Swallowing I/O means a full disk can look like a successful `println` until you check the flag.

> [!tip] Interview answer
> **`PrintStream` prints onto a byte stream; `PrintWriter` prints onto a character writer — JavaDoc prefers `PrintWriter` for characters.** Both suppress `IOException` and use `checkError()`. If autoflush is on, `PrintStream` also flushes on `'\n'`; `PrintWriter` flushes only on `println`, `printf`, and `format`.
