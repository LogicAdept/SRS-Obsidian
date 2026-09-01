<!--
reps: 0
priority: 0
-->
#Java/IO #SRS

# What is `PushbackInputStream`?

> [!abstract] Short answer
> **A `FilterInputStream` that can unread bytes into a small internal buffer.** After you `read` a delimiter you did not want to consume, `unread` puts it back so the **next** `read` returns it again. Default pushback size is **1 byte**; unread past the buffer throws `IOException`. This is `java.io` (since 1.0), not `java.util.stream`. `mark`/`reset` are **not** supported.

## Unread, then the next `read` sees it again

`PushbackInputStream` wraps another `InputStream` and adds the ability to **push back** (unread) bytes, stored in an internal buffer (`buf` / `pos`). The JavaDoc use case: a parser reads until a terminator (for example an operator byte after an identifier), then **unreads** that terminator so the next reader sees it ([[What is PushbackInputStream for]], [[Which subclasses class InputStream you do you know for what they intended]], [[What are common concrete InputStream and OutputStream implementations]]).

It is **not** a non-consuming peek. You still `read()`. `unread(int)` copies the low-order byte to the front of the pushback buffer; afterward the next byte read is `(byte) b`. Overloads unread a full `byte[]` or a slice. `read()` returns the most recently pushed-back byte if the buffer is not empty, otherwise it delegates to the underlying stream.

Constructors: `PushbackInputStream(in)` — **1-byte** buffer; `PushbackInputStream(in, size)` — `size > 0` or `IllegalArgumentException`. Pushback is not the same as `BufferedInputStream`’s read-ahead cache ([[How would you explain buffered streams in Java IO]], [[What kinds of input and output streams exist in Java]]).

`markSupported()` is `false`. `mark` is a no-op; `reset` throws `IOException`. After `close()`, `read` / `unread` / `available` / `skip` throw `IOException`. This is a **byte** stream; character pushback is `PushbackReader` ([[What is the difference between and what InputStream OutputStream Reader Writer]]).

```d2
direction: right
under: "underlying InputStream" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
pb: "pushback buf" {
  width: 140
  height: 50
  style.fill: "#fff8e1"
}
app: "read / unread" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
under -> pb
pb -> app
```

**Fig. 1.** `read` drains the pushback buffer first, then the wrapped stream. `unread` fills the buffer from the front.

```java
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.PushbackInputStream;

class Demo {
    static int peekThenPutBack(byte[] data) throws IOException {
        try (PushbackInputStream in = new PushbackInputStream(new ByteArrayInputStream(data))) {
            int b = in.read();
            in.unread(b);
            return in.read(); // same byte again
        }
    }
}
```

**Listing 1.** One-byte default buffer: `unread` then `read` returns the same value. Unreading two bytes without `new PushbackInputStream(in, 2)` throws `IOException`.

> [!warning] Default buffer is one byte, and this is not `java.util.stream`
> `unread` when the pushback buffer is full throws `IOException` (closed stream too). Do not call `reset()` expecting `BufferedInputStream` behavior. Tag mix-up: `PushbackInputStream` is `java.io.FilterInputStream`, not the Stream API.

> [!tip] Interview answer
> **`PushbackInputStream` lets a parser unread a byte (or a few) it already read, so the next `read` sees it again.** Name `unread`, the 1-byte default buffer, and “no `mark`/`reset`.” Contrast with `BufferedInputStream` (read-ahead, not unread).
