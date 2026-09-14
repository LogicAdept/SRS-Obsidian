<!--
reps: 0
priority: 0
-->
#Java/NIO/Channels #SRS

# How does FileChannel transferTo copy data and when is it zero copy?

> [!abstract] Short answer
> **`src.transferTo(position, count, target)` asks the channel to move up to `count` bytes to `target` in one call, "potentially much more efficient than a simple loop"** — the JVM may hand the whole job to the OS (`sendfile`-style), so the data never round-trips through a Java byte array. Zero copy happens **when the OS supports it** for the given channel pair; it is an optimization, not a contract. The method may transfer **fewer** bytes than requested, returns the actual count, does not change the source channel's position, and advances the target's position ([[What are channels in Java NIO]], [[What is a memory-mapped file in Java and when is it useful]]).

## One call, fewer copies

A plain copy loop (`BufferedReader`/`read`/`write`) moves every byte disk → kernel page cache → user buffer → kernel → target. `transferTo` can collapse the middle legs: the kernel copies page-cache pages straight to the target's file or socket. That is the "zero user-space copy" — CPU only drives metadata, not payloads. The javadoc phrase is deliberately hedged: "potentially much more efficient" and "whether this is efficient is platform-dependent", so benchmarks beat slogans.

| Contract point | What the javadoc fixes |
| --- | --- |
| Return value | bytes actually transferred (`≥ 0`), possibly fewer than `count` |
| Source position | unchanged — the start is the **absolute** `position` argument |
| Target position | written at the target's current position, then incremented |
| `position > size` | no bytes transferred, returns `0` |
| Interruption | thread may close channels → `AsynchronousCloseException` |
| Concurrency | if either channel is used by another thread, behaviour is unspecified |

`transferFrom(target, position, count)` is the mirror image and has the same shape of guarantees. Because a call may return short, production code loops on the returned count:

```java
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

class Xfer {
    static long copy(Path from, Path to) throws IOException {
        try (FileChannel src = FileChannel.open(from, StandardOpenOption.READ);
             FileChannel dst = FileChannel.open(to, StandardOpenOption.WRITE,
                     StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING)) {
            long pos = 0, n, total = 0;
            while ((n = src.transferTo(pos, src.size() - pos, dst)) > 0) {
                pos += n;
                total += n;
            }
            return total;
        }
    }

    public static void main(String[] args) throws IOException {
        System.out.println("copied " + copy(Path.of("/tmp/a.bin"), Path.of("/tmp/b.bin")) + " bytes");
    }
}
```

**Listing 1.** Loop until the source is drained — one big call is not guaranteed to finish the job:

```text
copied 1048576 bytes
```

**Listing 2.** One call is allowed to return short; the loop makes the copy complete.

```d2
direction: right
loop: "read/write loop\ndisk -> page cache -> user byte[] -> kernel" {
  width: 330
  height: 60
  style.fill: "#ffebee"
}
xfer: "transferTo\ndisk -> page cache -> target\n(user space skipped)" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
loop -> xfer: "same result, fewer copies"
```

**Fig. 1.** Same destination, different copy counts: the loop pays two extra boundary crossings per byte.

> [!warning] Zero copy is a hope, not a promise
> The optimization depends on OS, file system, and channel types — a socket target on Linux may use `sendfile`, an encrypted FS or unusual pair may fall back to a kernel or user copy, and the javadoc explicitly says "whether, and how many, bytes are transferred is platform-dependent". Do not claim "always zero copies" in an interview: say "the JVM is allowed to do it without user-space copies". Partial transfers are normal behaviour, not a bug — forgetting the loop silently truncates large copies. And `transferTo` does not work across arbitrary channel types; the target must be writable and open for the duration.

> [!tip] Interview answer
> `FileChannel.transferTo(position, count, target)` moves bytes channel-to-channel in one syscall-shaped call; the javadoc calls it potentially much more efficient than a read/write loop because the OS can avoid user-space copies (Linux `sendfile` for file-to-socket). It returns the bytes actually moved — possibly fewer than asked, so loop — leaves the source position alone, and advances the target. Zero copy is the best case on a friendly platform, not a guarantee.

