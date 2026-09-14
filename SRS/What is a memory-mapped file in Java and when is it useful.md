<!--
reps: 0
priority: 0
-->
#Java/NIO/Channels #SRS

# What is a memory-mapped file in Java and when is it useful?

> [!abstract] Short answer
> **`FileChannel.map(mode, position, size)` maps a region of the file "directly into memory": the returned `MappedByteBuffer` is a `ByteBuffer` whose content is the file itself, backed by virtual memory and the OS page cache.** No `read`/`write` calls, no copy into a Java array — you index the bytes like memory. Modes: `READ_ONLY`, `READ_WRITE` (changes flow back to the file, `force()` pushes them to the device), and `PRIVATE` (copy-on-write — your changes never reach the file). It shines for large files with random access and for sharing data between processes; the mapping stays valid "until the buffer itself is garbage-collected" — there is **no explicit unmap** ([[What are channels in Java NIO]], [[What notable features does Java NIO offer]]).

## The three modes and the lifecycle

`map` requires the channel to match the mode (a read-only channel cannot `READ_WRITE`-map, a write-only channel cannot `READ_ONLY`-map; `PRIVATE` needs read). The map is made against the channel's file at the moment of the call; a later `write` through the file channel does not move the buffer's view, and truncating the file while mapped is "unspecified" territory.

| Mode | Reads | Writes | Who sees the changes |
| --- | --- | --- | --- |
| `READ_ONLY` | yes | throws | — |
| `READ_WRITE` | yes | yes | the file, eventually other mappers |
| `PRIVATE` | yes | yes | nobody — copy-on-write page |

Durability is manual: `MappedByteBuffer.force()` writes changed pages of a `READ_WRITE` map down to storage; until then the OS page cache may hold them. "Closing the channel, in particular, has no effect upon the validity of the mapping" — unmapping is tied to garbage collection of the buffer, and the API deliberately hides it.

```java
import java.io.IOException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

class Mmap {
    public static void main(String[] args) throws IOException {
        try (FileChannel ch = FileChannel.open(Path.of("/tmp/mm.txt"),
                StandardOpenOption.READ, StandardOpenOption.WRITE,
                StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {
            ch.write(StandardCharsets.UTF_8.encode("page-0000"));
            MappedByteBuffer buf = ch.map(FileChannel.MapMode.READ_WRITE, 0, ch.size());
            buf.put(5, (byte) '9');                    // random-access write into the file
            System.out.println("via mmap: " + StandardCharsets.UTF_8.decode(buf.duplicate()));
            System.out.println("forced: " + buf.force());
        }
    }
}
```

**Listing 1.** Write through the mapping at an arbitrary offset, then force it to the device:

```text
via mmap: page-9000
forced: java.nio.DirectByteBuffer[pos=0 lim=9 cap=9]
```

**Listing 2.** The write landed through the mapping and `force()` returned the buffer.

```d2
direction: right
app: "MappedByteBuffer\nindex like memory" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
vm: "virtual memory / page cache" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}
file: "file on disk\n(READ_WRITE: writeback)" {
  width: 250
  height: 50
  style.fill: "#fff8e1"
}
app <-> vm <-> file
```

**Fig. 1.** The mapping plugs user indexes straight into the page cache; `force()` flushes dirty pages.

> [!warning] Sharp tool, not a default
> There is no `unmap()`: a huge mapping can pin virtual address space and page cache until the `MappedByteBuffer` becomes unreachable — and a lazy GC never collects it. `map` fails on a file you cannot read (and with `READ_WRITE` on a file you cannot write); mapping a **zero-length** file throws `IOException`. `PRIVATE` writes vanish by design. Changed pages are visible to other processes only when the OS schedules the writeback — use `force()` plus your own coordination for cross-process messaging. And for sequential streaming reads, a plain buffered stream usually beats a map.

> [!tip] Interview answer
> `FileChannel.map` turns a file region into a `MappedByteBuffer` through virtual memory: random access to big files, zero read/write syscalls, `READ_ONLY` / `READ_WRITE` / `PRIVATE` (copy-on-write) modes, `force()` for durability. The mapping lives until GC — no explicit unmap — so it is best for large, randomly accessed or shared files, not for small streaming reads.

