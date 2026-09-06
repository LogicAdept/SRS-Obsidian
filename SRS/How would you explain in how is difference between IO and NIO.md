<!--
reps: 0
priority: 0
-->
#Java/IO #Java/NIO #SRS

# What is the difference between Java IO and NIO?

> [!abstract] Short answer
> **`java.io` is blocking stream I/O (Java 1.0/1.1). `java.nio` is New I/O (Java 1.4): buffers, channels, and optional non-blocking multiplex.** A stream `read`/`write` **blocks** the caller until the transfer finishes (or EOF/error). NIO I/O goes through a `Buffer` (position / limit / capacity) and a `Channel`. Non-blocking mode exists only on `SelectableChannel`: the call **never blocks** and may transfer **fewer bytes than asked, or none**. A `Selector` lets one thread wait for readiness on many of those channels. `FileChannel` is **not** selectable. NIO is not “always non-blocking.”

## Streams versus buffers and channels

| | `java.io` | `java.nio` (1.4) |
| --- | --- | --- |
| Unit | `InputStream` / `OutputStream` (bytes), `Reader` / `Writer` (chars) | `Buffer` + `Channel` |
| How data sits | Sequential pipe; some wrappers add a `buf` (`BufferedInputStream`) | You `read` into / `write` from a `Buffer`; absolute `get`/`put` by index |
| Blocking | `InputStream.read()` waits for a byte, EOF, or error | Selectable channels **start blocking**; `configureBlocking(false)` then never waits |
| Many sockets | Typically one thread per stream | `Selector` multiplexes `SelectableChannel`s |
| Files | `FileInputStream` sequential; `File` is a pathname | `FileChannel`: position, `map`, `transferTo`, `lock` — still not a `Selector` target |

`NIO` is **New I/O**, not a synonym for non-blocking. Non-blocking is a **mode** of `SelectableChannel` ([[How would you explain advantages of Java NIO over classic blocking IO]], [[How does NIO provide non-blocking access to resources]], [[How would you explain blocking versus non blocking methods in IO and concurrency]]).

**Stream-oriented.** `InputStream` is the byte-input root; `read()` returns `0..255` or `-1` and **blocks** ([[How does Java]], [[What is the difference between and what InputStream OutputStream Reader Writer]]). You do not get a movable file position on the stream itself. Dump text that says stream bytes are “never cached” and “you cannot move” is too strong: `BufferedInputStream` **does** cache and supports `mark`/`reset`; that is still a sequential window, not `FileChannel` absolute reads ([[What are buffered streams in Java]]).

**Buffer-oriented.** A `Buffer` is a finite primitive sequence with capacity, limit, and position (`0 ≤ mark ≤ position ≤ limit ≤ capacity`). Channel transfers are relative to the current position. `flip` / `clear` / `rewind` reuse the same array. Buffers are **not** thread-safe.

**Channels.** A `Channel` is an open connection (file, socket, device). In **blocking** mode, every I/O on a `SelectableChannel` waits until it completes. In **non-blocking** mode it never waits and may transfer **zero** bytes — the thread can do other work, then `select` again. Register with a `Selector` only after `configureBlocking(false)` (`IllegalBlockingModeException` otherwise). `select()` asks the OS which registered channels are ready for their interest set ([[What is blocking method]]).

**Files stay different.** `FileChannel` gives maps, positional I/O, and `transferTo` (often without a Java copy). It does **not** extend `SelectableChannel`. NIO.2 (Java 7) `Path` / `Files` is a later API on top of this story, not a third blocking mode.

```d2
direction: down
io: "java.io stream\nread/write blocks the caller" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
nio: "Channel + Buffer\noptional non-blocking" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
sel: "Selector\nmany SelectableChannels, one thread" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
file: "FileChannel\nnot selectable" {
  width: 240
  height: 45
  style.fill: "#ffebee"
}
io -> nio
nio -> sel
nio -> file
```

**Fig. 1.** Blocking streams vs buffer/channel NIO. Only selectable channels join a `Selector`. File I/O uses `FileChannel`, not that multiplexor.

```java
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.channels.SelectableChannel;
import java.nio.channels.Selector;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

class IoVsNio {
    static int blockingByte(String path) throws IOException {
        try (FileInputStream in = new FileInputStream(path)) {
            return in.read();
        }
    }

    static int channelRead(Path path) throws IOException {
        try (FileChannel ch = FileChannel.open(path, StandardOpenOption.READ)) {
            ByteBuffer buf = ByteBuffer.allocate(64);
            int n = ch.read(buf);
            return n;
        }
    }

    static Selector multiplex(SelectableChannel ch) throws IOException {
        ch.configureBlocking(false);
        Selector sel = Selector.open();
        ch.register(sel, ch.validOps());
        return sel;
    }
}
```

**Listing 1.** `blockingByte` sits in `InputStream.read`. `channelRead` fills a `ByteBuffer` (the channel may still **block** — `FileChannel` is not selectable). `multiplex` is the NIO difference for sockets: non-blocking plus `Selector`.

> [!warning] NIO does not mean “never blocks”
> New `SelectableChannel`s are **blocking** until `configureBlocking(false)`. A non-blocking `read` that returns `0` is success, not EOF (`-1` still means end on byte channels that use that convention). `FileChannel` cannot be registered with a `Selector`. A `Buffer` you share across threads needs your own locking. `java.io` buffering (`BufferedReader`) is not NIO and does not give you a selector.

> [!tip] Interview answer
> IO is blocking streams: the thread waits in `read` or `write`. NIO is New I/O — buffers and channels — and *may* be non-blocking on selectable channels, with a `Selector` so one thread watches many sockets. File NIO is `FileChannel` (maps, position, transfer), not selectors. Do not say NIO is always non-blocking or that streams never buffer.
