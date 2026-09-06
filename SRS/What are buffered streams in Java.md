<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# What are buffered streams in Java?

> [!abstract] Short answer
> **They are decorator streams that keep an in-memory array so each `read`/`write` does not hit the underlying stream (and usually the OS).** Bytes: `BufferedInputStream` / `BufferedOutputStream` (Java 1.0), subclasses of `FilterInputStream` / `FilterOutputStream`. Characters: `BufferedReader` / `BufferedWriter` (Java 1.1). The wrapper refills or flushes a `buf` in chunks. `BufferedInputStream` also implements `mark`/`reset`. Wrap costly sources (`FileInputStream`, `InputStreamReader`, `FileWriter`). Close (or `flush`) the **outer** stream so leftover output is written.

## Decorators with a `buf`

`FilterInputStream` wraps another `InputStream` in field `in` and, by default, forwards every call. Subclasses add behavior. `BufferedInputStream` creates an internal `byte[] buf` and, as you `read` or `skip`, **refills it from the contained stream, many bytes at a time**. `mark` stores a position in that buffer; `reset` re-reads those bytes before taking new ones from `in`. `markSupported()` is **`true`**. `available()` is bytes left in the buffer plus `in.available()`. Size `<= 0` is `IllegalArgumentException` ([[Which subclasses class InputStream you do you know for what they intended]], [[How does Java]]).

`BufferedOutputStream`: write into `buf` without a native call per byte. `flush()` forces the buffer to the underlying stream. `write(byte[],off,len)` normally copies into `buf`; if `len` is **at least the buffer size**, it flushes then writes **directly** to `out` (stacked buffered streams do not copy twice). `FilterOutputStream.close` (not overridden on `BufferedOutputStream`) **flushes, then closes `out`**.

Characters are the same idea on `Reader`/`Writer`. `BufferedReader` JavaDoc: each `Reader.read` usually causes a matching read of the underlying character or byte stream, so wrap `FileReader` / `InputStreamReader`. `readLine()` splits on `\n`, `\r`, `\r\n`, or EOF. `BufferedWriter` wrap `FileWriter` / `OutputStreamWriter`; `newLine()` writes `line.separator`, not a hard-coded `'\n'`. Default buffer size is “large enough for most purposes” — the JavaDoc does not publish a number; the two-arg constructors take an explicit size ([[Which classes convert between Java byte streams and character streams]], [[What is the difference between and what InputStream OutputStream Reader Writer]]).

These are **not** NIO `ByteBuffer`s and **not** `PushbackInputStream` (`unread` is a different filter) ([[How would you explain advantages of Java NIO over classic blocking IO]], [[What is PushbackInputStream]]).

```d2
direction: down
app: "your read/write" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
buf: "Buffered* buf[]\nrefill / flush in chunks" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
raw: "FileInputStream / FileOutputStream\nor InputStreamReader" {
  width: 300
  height: 55
  style.fill: "#fff8e1"
}
app -> buf
buf -> raw
```

**Fig. 1.** The buffered decorator sits between the caller and a costly stream. Closing the outer wrapper closes `in` / `out` (`FilterInputStream.close` is `in.close()`).

```java
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

class BufferedStreams {
    static void copyBytes(String from, String to) throws IOException {
        try (BufferedInputStream in = new BufferedInputStream(new FileInputStream(from));
             BufferedOutputStream out = new BufferedOutputStream(new FileOutputStream(to))) {
            in.transferTo(out);
        }
    }

    static String firstLine(String path) throws IOException {
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(new FileInputStream(path), StandardCharsets.UTF_8))) {
            return in.readLine();
        }
    }
}
```

**Listing 1.** Outer buffered streams in try-with-resources. `transferTo` drains the input (`InputStream.transferTo` does not close either stream; TWR does). The reader wrap matches `InputStreamReader`’s “for top efficiency, wrap in `BufferedReader`” note. Close flushes `BufferedOutputStream` via inherited `FilterOutputStream.close` ([[How would you explain the AutoCloseable interface in Java]], [[What is try-with-resources]]).

> [!warning] Unflushed `buf` and closing the inner stream
> If you close or discard the **inner** `FileOutputStream` while a `BufferedOutputStream` still holds bytes, those bytes never reach the file. Flush or close the **outer** stream. `flush` is still required when the wrapper must stay open (a socket you keep). Buffering does not make `read` non-blocking. `mark`/`reset` only work within `marklimit` on `BufferedInputStream`; a plain `FileInputStream` typically does not support mark. A huge `read`/`write` can skip the buffer and hit the underlying stream on purpose. The JavaDoc does **not** publish the default buffer size — do not quote 8192. Size `<= 0` is `IllegalArgumentException`, not “use default.”

> [!tip] Interview answer
> Buffered streams wrap another stream and keep an array so you pay for native I/O in chunks, not per byte or character. Use `BufferedInputStream`/`BufferedOutputStream` for bytes and `BufferedReader`/`BufferedWriter` for text, around file and charset bridges. `BufferedInputStream` adds `mark`/`reset`. Always flush or close the outermost wrapper, or the last writes stay in memory.
