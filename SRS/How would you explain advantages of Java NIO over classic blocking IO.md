<!--
reps: 0
priority: 0
-->
#Java/NIO #Java/IO #SRS

# How would you explain advantages of Java NIO over classic blocking IO?

> [!abstract] Short answer
> **NIO (Java 1.4) is buffer-and-channel I/O with optional non-blocking multiplex.** `java.io` streams `read`/`write` **block** the caller until the transfer finishes. A `SelectableChannel` in non-blocking mode **never blocks** and may transfer **fewer bytes than asked, or none**; a `Selector` lets **one thread** wait for readiness on **many** channels. `FileChannel` adds memory maps, `transferTo`/`transferFrom` (often zero-copy), positional I/O, `force`, and `FileLock`. Direct `ByteBuffer`s aim to skip a native copy. NIO.2 `Files.newDirectoryStream` iterates instead of a full `File.list` array. None of that makes NIO automatically faster for a small sequential file.

## What `java.io` cannot do the same way

Classic streams are sequential byte or char pipes. `InputStream.read()` **blocks** until a byte, EOF, or error ([[How does Java]], [[What is the difference between and what InputStream OutputStream Reader Writer]], [[How would you explain blocking versus non blocking methods in IO and concurrency]], [[How would you explain in how is difference between IO and NIO]]). `mark`/`reset` exist on some streams; you still do not have a file **position** you can set, a mapped region, or one thread watching hundreds of sockets.

NIO’s units (since 1.4):

| Piece | Advantage vs `java.io` |
| --- | --- |
| `Buffer` | Capacity / limit / position; relative **and absolute** `get`/`put`; `flip` / `clear` / `rewind` for a reusable window |
| `Channel` | Open connection (file, socket, device); `isOpen`; generally safe for concurrent use |
| `SelectableChannel` + `Selector` | Non-blocking mode + multiplexed readiness |
| `FileChannel` | Seek, absolute read/write, `map`, `transferTo`/`From`, `lock`, `force` |
| Direct `ByteBuffer` | JVM **best effort** to run native I/O on the buffer without an extra copy |
| NIO.2 `Files` (1.7) | `newDirectoryStream` instead of materializing every name; exceptions instead of `listFiles` → `null` ([[How do you list directory entries that match a criterion in Java]]) |

**Non-blocking and selectors.** Newly created selectable channels are **blocking**. `configureBlocking(false)`: an I/O call **never blocks** and may transfer **zero** bytes. Register with a `Selector` only after non-blocking mode (`IllegalBlockingModeException` if still blocking). `select()` asks the OS which registered channels are ready for the interest set — one thread, many connections, instead of one blocking thread per `Socket`/`InputStream` ([[How does NIO provide non-blocking access to resources]], [[What is blocking method]]).

**Files.** `FileChannel.map`: for **large** files, mapping is often much more efficient than looped `read`/`write`. Mapping a few tens of kilobytes is **usually more expensive** than ordinary reads. The mapping stays valid after the channel is closed (until the `MappedByteBuffer` is GC’d). `transferTo` / `transferFrom` can let the OS move bytes between the filesystem cache and another channel **without copying** through Java. `read`/`write` at an explicit position do not move the channel position.

**Direct buffers.** `ByteBuffer.allocateDirect`: native I/O may avoid an intermediate copy. Allocation/deallocation cost is typically **higher**; content may sit **outside** the GC heap. Allocate them for large, long-lived native I/O, and only when you **measure** a gain.

```d2
direction: down
io: "java.io stream\none thread blocks on read/write" {
  width: 300
  height: 55
  style.fill: "#fff8e1"
}
nio: "Selector + non-blocking channels\none thread, many ready keys" {
  width: 320
  height: 55
  style.fill: "#e8f5e9"
}
file: "FileChannel\nmap / transferTo / position / lock" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
io -> nio
```

**Fig. 1.** Stream blocking vs selector multiplex. File advantages are `FileChannel` operations, not `Selector` — `FileChannel` is not a `SelectableChannel`.

```java
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.nio.channels.SelectableChannel;
import java.nio.channels.Selector;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

class NioAdvantages {
    static long sendFilePrefix(Path src, Path dst, long count) throws IOException {
        try (FileChannel in = FileChannel.open(src, StandardOpenOption.READ);
             FileChannel out = FileChannel.open(
                     dst, StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {
            return in.transferTo(0, count, out);
        }
    }

    static Selector watch(SelectableChannel ch) throws IOException {
        ch.configureBlocking(false);
        Selector selector = Selector.open();
        ch.register(selector, ch.validOps());
        return selector;
    }
}
```

**Listing 1.** `transferTo` is the documented potentially-faster copy (may transfer **fewer** bytes than `count`). `watch` shows the required non-blocking mode before `register`. `FileChannel` cannot be passed to `watch`.

> [!warning] NIO is not “always faster” and files are not selectable
> `SelectableChannel` starts **blocking** — same as `java.io` until `configureBlocking(false)`. Non-blocking `read`/`write` can return `0`; you must retry after `select`. `Buffer` is **not** thread-safe. Direct buffers and maps cost more for small, short-lived work. `transferTo` is allowed to send a **partial** count. `FileChannel` does not implement `SelectableChannel`: you cannot multiplex ordinary file I/O with `Selector`. Interrupt of a thread blocked on an interruptible channel **closes** the channel.

> [!tip] Interview answer
> Classic `java.io` is blocking streams: the thread sits in `read` or `write`. NIO adds buffers, channels, and a `Selector` so one thread can service many non-blocking sockets, plus `FileChannel` maps, positional I/O, locks, and often zero-copy `transferTo`. Direct buffers skip a native copy when they are large and long-lived. Use NIO where you need multiplex, mapping, or measured throughput — not because the acronym says non-blocking.
