<!--
reps: 0
priority: 0
-->
#Java/NIO #SRS

# What are channels in Java NIO

> [!abstract] Short answer
> **A channel is an open connection to an I/O-capable entity — a file, a socket, a hardware device — through which data moves in bulk between the entity and a `ByteBuffer`.** The javadoc frames it as "an open connection to an entity such as a hardware device, a file, a network socket, or a program component"; channels are open/closed, asynchronously closeable, and interruptible, and they replace java.io's one-byte-at-a-time streams with buffer-driven, position-based transfers.

## The channel family

Two families live in `java.nio.channels`. `FileChannel` reads and writes files: it has a position, supports `map(...)` for memory-mapped access and `transferTo`/`transferFrom` for channel-to-channel copies. The `SelectableChannel` lineage (`SocketChannel`, `ServerSocketChannel`, `DatagramChannel`, `Pipe.SinkChannel/Pipe.SourceChannel`) can be switched to non-blocking mode and registered with a `Selector` — the basis of multiplexed I/O.

```d2
direction: right
buf: "ByteBuffer\nposition / limit / capacity" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
ch: "Channel\nFileChannel or SocketChannel..." {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
ent: "Entity\nfile, socket, device" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
sel: "Selector (only for\nSelectableChannel)" {
  width: 290
  height: 80
  style.fill: "#e8f5e9"
}
buf <-> ch <-> ent
ch -> sel
```

**Fig. 1.** Data always goes through a buffer — channels read *into* buffers and write *from* buffers; selectors watch the selectable ones.

```java
try (FileChannel ch = new RandomAccessFile("/tmp/nio-demo.txt", "rw").getChannel()) {
    ByteBuffer out = ByteBuffer.allocate(64);   // capacity = 64
    out.put("hello nio".getBytes(StandardCharsets.UTF_8));
    out.flip();                                 // position=0, limit=9
    ch.write(out);
    System.out.println("after write: position=" + out.position() + " limit=" + out.limit());

    ch.position(0);
    ByteBuffer in = ByteBuffer.allocate(64);
    ch.read(in);
    in.flip();
    byte[] data = new byte[in.remaining()];
    in.get(data);
    System.out.println("read back: '" + new String(data, StandardCharsets.UTF_8) + "'");
}
```

**Listing 1.** Verified on JDK 21:

```java
after write: position=9 limit=9
read back: 'hello nio'
```

**Listing 2.** The buffer is the working end: fill it, `flip()` to switch direction, then the channel drains or fills it. `FileChannel.map(...)` (memory-mapped read) and `transferTo(0, size, dst)` (9-byte copy in the same run) show the two bulk-transfer shortcuts files have and sockets do not.

## Why channels instead of streams

Streams are one-directional (InputStream vs OutputStream) and byte-oriented; a channel is bidirectional (`ByteChannel` unifies readable + writable), position-based (`seek`-style control on files), and the unit of work is a buffer — which lets the JVM hand contiguous memory to the OS efficiently. The interface contract adds two things streams never had: channels are **asynchronously closeable** (a thread blocked in I/O on a channel is released by another thread's `close()`) and **interruptible** (blocking I/O on an interruptible channel responds to `Thread.interrupt` with `ClosedByInterruptException`).

> [!warning] Channels are not automatically non-blocking, and buffers do not move themselves
> Two recurring mistakes. First, "channels are the non-blocking thing in NIO" is only true for `SelectableChannel` descendants after an explicit `configureBlocking(false)` plus a selector — a plain `SocketChannel` in blocking mode blocks exactly like a stream, and `FileChannel` has no non-blocking mode at all (multiplexing applies to sockets, not files). Second, the flip dance is the classic bug source: after `put`, position equals limit, and a direct `get` or write reads from the wrong end — `flip()` (or `clear`/`rewind` for the other variants) must reset position/limit deliberately. Bulk details live in [[What notable features does Java NIO offer]], the multiplexing story in [[How does NIO provide non-blocking access to resources]], and the blocking-vs-NIO comparison in [[How would you explain advantages of Java NIO over classic blocking IO]].

> [!tip] Interview answer
> **A channel is an open connection to a file, socket, or device, used as a bulk pipe between that entity and a ByteBuffer. Two families: FileChannel with position, memory mapping and transferTo; and selectable channels — sockets — that can go non-blocking and register with a Selector. Channels are bidirectional, asynchronously closeable and interruptible; data always flows through a buffer, and flip() is what switches the buffer between writing and reading.**

