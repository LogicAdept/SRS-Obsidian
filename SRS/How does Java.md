<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# How does file reading work in Java?

> [!abstract] Short answer
> **You open a stream on the path, then `read` until `-1` (EOF).** Bytes: `InputStream` (`FileInputStream`, `Files.newInputStream`) — `read()` returns `0..255` or `-1` and **blocks**. Characters: wrap bytes in `InputStreamReader` with a **charset**, usually inside `BufferedReader` for `readLine()` and fewer native reads. `java.io.File` is only a pathname. Close the stream (`try-with-resources` or `close()`). `Files.readAllBytes` / `readString` load the whole file and close it for you — not for large files.

## Open, decode, buffer, close

A `File` does not open anything ([[Does a java.io.File instance represent only a path without opening the file]]). `new FileInputStream(file)` **opens a connection** and a `FileDescriptor`; missing or unreadable files throw `FileNotFoundException` ([[Which subclasses class InputStream you do you know for what they intended]]).

`InputStream` (Java 1.0) is the abstract **byte** input root. A subclass must supply the next byte. `read()` blocks until a byte, EOF, or an error. Array `read` may return fewer bytes than requested. After `close()`, further `read` throws `IOException`.

Text is not bytes. `Reader` (Java 1.1) is abstract **character** input; a subclass must implement `read(char[],int,int)` and `close()`. `InputStreamReader` is the **bridge**: it reads bytes and **decodes** them with a named charset, a `Charset`, or the **default charset**. One `read()` on the reader may pull extra bytes from the underlying stream for conversion ([[Which classes convert between Java byte streams and character streams]], [[What is the difference between and what InputStream OutputStream Reader Writer]]).

Buffering is a decorator, not a third kind of stream. `BufferedInputStream` keeps an internal `byte[]` and refills it from the wrapped stream **many bytes at a time**; it also implements `mark` / `reset`. `BufferedReader` buffers characters and lines. `InputStreamReader` JavaDoc tells you to wrap it in `BufferedReader` for efficiency. `BufferedReader` JavaDoc: without that wrap, each `read` / `readLine` can hit the file and decode ([[What are buffered streams in Java]]).

`readLine()` ends a line on `\n`, `\r`, `\r\n`, or EOF; the returned `String` has no terminator (`null` at EOF with no characters). `BufferedReader.lines()` (Java 8) is a lazy `Stream<String>`; I/O failures become `UncheckedIOException`.

NIO.2 convenience (already on `Files`): `newBufferedReader(path, charset)` (UTF-8 overload exists), `newInputStream` (unbuffered), `readAllBytes` / `readString` (closes the file themselves; documented as simple/small-file helpers).

```d2
direction: down
path: "File / Path\nname only" {
  width: 200
  height: 50
  style.fill: "#fff8e1"
}
bytes: "FileInputStream\nInputStream.read → 0..255 or -1" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
chars: "InputStreamReader\nbytes → chars + charset" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
buf: "BufferedReader\nreadLine, refill buffer" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
path -> bytes
bytes -> chars
chars -> buf
```

**Fig. 1.** Typical text read: open bytes, decode with an explicit charset, buffer, then close the outer stream.

```java
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

class ReadTextFile {
    static String firstLine(String path) throws IOException {
        try (BufferedReader in = new BufferedReader(
                new InputStreamReader(
                        new FileInputStream(path), StandardCharsets.UTF_8))) {
            return in.readLine();
        }
    }
}
```

**Listing 1.** Outer `BufferedReader` in try-with-resources. `FileInputStream` opens; `InputStreamReader` decodes UTF-8; `readLine()` uses the character buffer. `FileInputStream`’s API note: call `close()` directly or via try-with-resources ([[How would you explain the AutoCloseable interface in Java]], [[What is try-with-resources]]).

> [!warning] Default charset, blocking `read`, and “must TWR”
> `new InputStreamReader(in)` (no charset) uses the **default charset** — not a portable file encoding. `read()` **blocks**; it is not a non-blocking NIO channel. Close is required to release the connection, but **not** only via try-with-resources: `close()` yourself is legal. `InputStream.readAllBytes()` does **not** close the stream; `Files.readAllBytes` does, and is not for large files. `read()` returning `int` is not a Java `byte` (`-1` is EOF, not a signed byte).

> [!tip] Interview answer
> File reading is streams: open an `InputStream` on the file, wrap `InputStreamReader` with an explicit charset for text, and usually `BufferedReader` so you are not decoding one character at a time. `read` blocks and returns `-1` at EOF. A `File` object is only a path; close the stream with try-with-resources or `close()`.
