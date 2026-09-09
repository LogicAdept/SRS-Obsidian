<!--
reps: 0
priority: 0
-->
#Java/NIO #SRS

# What notable features does Java NIO offer

> [!abstract] Short answer
> **NIO (Java 1.4, extended by NIO.2 in Java 7) is buffers, channels, selectors, and file-system power: bulk I/O through `ByteBuffer`, bidirectional `Channel` abstractions, readiness multiplexing for sockets, memory-mapped files, file locking, `transferTo` for channel-to-channel copies, and the `java.nio.file` API with `Path`, `Files`, and directory walking.** The recurring theme: fewer system calls and fewer copies, more explicit control.

## The feature map

```d2
direction: right
core: "Core I/O\nByteBuffer + Channel\nfill / flip / drain" {
  width: 290
  height: 100
  style.fill: "#e3f2fd"
}
mux: "Selector + SelectableChannel\none thread, many sockets" {
  width: 310
  height: 100
  style.fill: "#fff3e0"
}
file: "FileChannel\nmap (mmap), lock, transferTo" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
fs: "NIO.2 file system\nPath, Files, walk, watch" {
  width: 290
  height: 100
  style.fill: "#e8f5e9"
}
core -> mux
core -> file
file -> fs
```

**Fig. 1.** Four feature clusters: the buffer/channel core, socket multiplexing, advanced file channels, and the NIO.2 file-system API.

What each cluster buys you. **Buffers**: direct buffers (`allocateDirect`) place data outside the heap so OS calls can use it without a copy; `flip`/`clear`/`rewind` control the read-write switch. **Channels**: one abstraction for files and sockets with bulk moves (`transferTo`/`transferFrom`, which can become zero-copy OS operations), memory-mapped files (`FileChannel.map`) that turn a file into a byte region addressable in memory, and file locks (`FileChannel.lock`). **Selectors**: readiness-based multiplexing — see [[How does NIO provide non-blocking access to resources]]. **NIO.2**: `Path`/`Files` replacing `File` with attribute views, recursive `walkFileTree`, symlink handling, and a `WatchService` for directory change events; plus the asynchronous channel group model for completion-based I/O.

```java
try (FileChannel ch = FileChannel.open(java.nio.file.Path.of("/tmp/nio-demo.txt"))) {
    MappedByteBuffer mapped = ch.map(FileChannel.MapMode.READ_ONLY, 0, ch.size());
    byte[] data = new byte[(int) ch.size()];
    mapped.get(data);
    System.out.println("mmap read: '" + new String(data, StandardCharsets.UTF_8) + "'");
}
try (FileChannel src = FileChannel.open(java.nio.file.Path.of("/tmp/nio-demo.txt"));
     FileChannel dst = new RandomAccessFile("/tmp/nio-copy.txt", "rw").getChannel()) {
    long n = src.transferTo(0, src.size(), dst);
    System.out.println("transferTo copied: " + n + " bytes");
}
```

**Listing 1.** Two file-channel superpowers, verified on JDK 21:

```java
mmap read: 'hello nio'
transferTo copied: 9 bytes
```

**Listing 2.** The mapped buffer read the file through memory mapping; `transferTo` moved the whole 9-byte file to another channel — both without manual read/write loops.

> [!warning] Direct buffers and mmaps are sharp tools, not defaults
> Three traps when selling "NIO features" in an interview. First, `allocateDirect` has a price: allocation and release are slower than heap buffers, and mismanaged direct memory is invisible to heap tools — use it for long-lived I/O buffers, not throwaway objects. Second, a memory-mapped file only sees updates if nothing has torn it down; unmapping is not exposed in the API (the `MappedByteBuffer` lives until GC), so a huge mmap can pin virtual memory — and `map` fails on a file you cannot `read` (and with `READ_WRITE`, one you cannot `write`). Third, feature lists age: `Path`/`Files` is NIO.2 (Java 7+), `AsynchronousSocketChannel` too; anything claiming "NIO means non-blocking files" is wrong — `FileChannel` blocks and does not register with selectors. The honest summary of when NIO wins over streams is in [[How would you explain advantages of Java NIO over classic blocking IO]], with the channel mechanics in [[What are channels in Java NIO]] and the IO/NIO conceptual split in [[How would you explain in how is difference between IO and NIO]].

> [!tip] Interview answer
> **NIO brought buffers and channels instead of streams, selectors for socket multiplexing, and file power: memory-mapped files, file locks, and zero-copy-ish transferTo. NIO.2 added the modern Path and Files API, directory watching, and asynchronous channels. Core wins: bulk transfers through buffers, one-thread readiness multiplexing for sockets, and fewer copies. Files themselves never became non-blocking — that is selector territory only.**

