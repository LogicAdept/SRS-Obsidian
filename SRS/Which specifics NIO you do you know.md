<!--
reps: 0
priority: 0
-->
#Java/NIO #Java/IO #SRS

# What NIO features do you know?

> [!abstract] Short answer
> **Three pillars of `java.nio` (Java 1.4): `Channel` + `Buffer`, optional `Selector` multiplex, and `java.nio.charset`.** NIO is **New I/O**, not “never blocks.” `SelectableChannel` **starts blocking**; `configureBlocking(false)` then a `read`/`write` never waits and may transfer **zero** bytes. A `Selector` is a multiplexor of those channels (`select` asks the OS which are ready). `FileChannel` maps, locks, `transferTo`/`force` — and is **not** selectable. Buffers exist for every primitive **except `boolean`**. `Charset` maps 16-bit Unicode code units to bytes via `newDecoder()` / `newEncoder()` ([[How would you explain in how is difference between IO and NIO]], [[How would you explain advantages of Java NIO over classic blocking IO]]).

## Channels and selectors (dump, corrected)

A `Channel` is an open connection (`isOpen` / `close`). `FileChannel` is a `SeekableByteChannel`: position, size, truncate, absolute read/write, `map` into memory (often faster than a loop of `read`/`write`), `force` to the device, `lock`, `transferTo`/`transferFrom` (often via the FS cache). Get one from `FileInputStream`/`FileOutputStream`/`RandomAccessFile.getChannel()` — position is shared with that object ([[What is RandomAccessFile in Java]], [[What file access modes does RandomAccessFile support]]).

Dump “channels never block” is false. Dump “socket is the blocking tool” is noise. Non-blocking multiplex is **`Selector` + `SelectableChannel`** (sockets, not files) ([[How does NIO provide non-blocking access to resources]], [[What are channels in Java NIO]]).

## Buffers

A `Buffer` has capacity, limit, position (`0 ≤ mark ≤ position ≤ limit ≤ capacity`). `clear` / `flip` / `rewind` / `mark` / `reset` reuse the same storage. Subclasses `get`/`put` typed values. `ByteBuffer` also does bulk copies and **views** as other primitive types (byte order). `MappedByteBuffer` is the `map` result. **No `BooleanBuffer`.** Buffers are not thread-safe ([[What notable features does Java NIO offer]]).

## Charsets

`Charset` is a named mapping between `char` sequences and bytes. `newDecoder()` / `newEncoder()` build `CharsetDecoder` / `CharsetEncoder`. `Charset.decode`/`encode` convenience methods **replace** malformed/unmappable sequences; use the decoder/encoder directly to detect them. Standard names include `US-ASCII`, `UTF-8`, `UTF-16`. `InputStreamReader.getEncoding()` returns a historical name from this model ([[Which classes convert between Java byte streams and character streams]]).

```java
import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;

class NioBits {
    static String head(String path) throws IOException {
        try (RandomAccessFile raf = new RandomAccessFile(path, "r");
             FileChannel ch = raf.getChannel()) {
            ByteBuffer buf = ByteBuffer.allocate(256);
            ch.read(buf);
            buf.flip();
            return StandardCharsets.UTF_8.decode(buf).toString();
        }
    }
}
```

**Listing 1.** `getChannel()` (already tied to `"r"`), fill a `ByteBuffer`, `flip`, charset decode. This channel is **not** a `Selector` target.

```d2
direction: down
ch: "Channel\nFileChannel vs SelectableChannel" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
buf: "Buffer\nflip / get / put" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
sel: "Selector\nready keys" {
  width: 180
  height: 45
  style.fill: "#fff8e1"
}
cs: "Charset\nencoder / decoder" {
  width: 200
  height: 45
  style.fill: "#e8f5e9"
}
ch -> buf
ch -> sel
buf -> cs
```

**Fig. 1.** Interview three-pack: buffers, channels (file vs selectable), charset. Selector does not apply to `FileChannel`.

> [!warning] NIO is not “non-blocking I/O,” and files are not selectable
> Registering a blocking `SelectableChannel` with a `Selector` fails (`IllegalBlockingModeException`). `FileChannel` concurrent ops that move position **block each other**; that is not `Selector`. `Charset.decode` swallows errors unless you use `CharsetDecoder`. Do not say `java.io` “has no buffers” — `BufferedInputStream` exists; it is not a `java.nio.Buffer`.

> [!tip] Interview answer
> NIO gives you buffers and channels, a selector to wait on many non-blocking socket channels, file maps and locks on `FileChannel`, and charset encoders/decoders. Channels start blocking; you opt into non-blocking. There is no boolean buffer, and you cannot select a `FileChannel`.
