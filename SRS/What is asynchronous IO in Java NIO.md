<!--
reps: 0
priority: 0
-->
#Java/NIO/Channels #SRS

# What is asynchronous IO in Java NIO?

> [!abstract] Short answer
> **Asynchronous IO (NIO.2, Java 7) is the `AsynchronousChannel` family — `AsynchronousFileChannel`, `AsynchronousSocketChannel`, `AsynchronousServerSocketChannel`, `AsynchronousDatagramChannel` — where an operation starts immediately and you consume the result later in one of two styles: a returned `Future` or a `CompletionHandler<V, A>` callback ("A CompletionHandler is specified as a parameter and is invoked to consume the result of the I/O operation").** Handlers run on the threads of the channel's `AsynchronousChannelGroup` — a pool you can supply; the initiating thread never blocks. It is a different API from the selector world: these channels are not `SelectableChannel`s ([[What are channels in Java NIO]], [[How does NIO provide non-blocking access to resources]]).

## Two consumption styles

Every read/write/connect method has three overloads: plain (returns `Future<V>`), with an `Attachment` + `CompletionHandler`, and (for sockets) both. With a `Future` you choose when to wait — `get()` blocks, `isDone()` polls, `cancel(true)` attempts to abort the operation. With a `CompletionHandler` you never wait: the group's worker invokes `completed(result, attachment)` or `failed(exc, attachment)` when the OS finishes. The `attachment` parameter is your closure carrier — state that must travel with the operation.

| | `Future<V>` style | `CompletionHandler` style |
| --- | --- | --- |
| Waiting | caller decides (`get` / poll) | never — callback on group thread |
| Backpressure | natural (you start few) | easy to start thousands — must throttle |
| Error surface | `ExecutionException` on `get` | `failed(...)` callback |
| Cancellation | `future.cancel(true)` | channel close |

`AsynchronousFileChannel` opens through static `open(...)` methods (optionally with a group); the socket channels can also bind to a custom group whose executor sizes the callback pool. The default group is process-wide.

```java
import java.nio.ByteBuffer;
import java.nio.channels.AsynchronousFileChannel;
import java.nio.channels.CompletionHandler;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;

class AsyncRead {
    public static void main(String[] args) throws Exception {
        try (AsynchronousFileChannel ch = AsynchronousFileChannel.open(
                Path.of("/tmp/async.txt"), StandardOpenOption.READ)) {
            ByteBuffer buf = ByteBuffer.allocate(64);
            ch.read(buf, 0, buf, new CompletionHandler<Integer, ByteBuffer>() {
                public void completed(Integer n, ByteBuffer b) {
                    b.flip();
                    System.out.println("read " + n + " bytes: "
                            + StandardCharsets.UTF_8.decode(b));
                }
                public void failed(Throwable exc, ByteBuffer b) {
                    System.out.println("failed: " + exc);
                }
            });
            System.out.println("main thread continues before the read finishes");
            Thread.sleep(200);   // demo only: keep the JVM alive for the callback
        }
    }
}
```

**Listing 1.** Completion-handler read: `main` runs on, the callback lands on a group thread:

```text
main thread continues before the read finishes
read 9 bytes: async ok
```

**Listing 2.** The handler printed after `main` — proof the callback ran on a group thread.

```d2
direction: right
main: "initiating thread\nch.read(buf, pos, att, handler)" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
group: "AsynchronousChannelGroup\nworker pool" {
  width: 270
  height: 50
  style.fill: "#e8f5e9"
}
cb: "completed / failed\non the group thread" {
  width: 260
  height: 55
  style.fill: "#fff8e1"
}
main -> group: "operation starts"
group -> cb: "OS signals completion"
```

**Fig. 1.** The call returns immediately; the group's worker delivers the result to the handler.

> [!warning] Handlers run on borrowed threads
> Blocking inside `completed` / `failed` stalls the group's worker pool — offload heavy work elsewhere or size the group for it. Exceptions thrown **inside** a handler are swallowed (there is no caller to catch them); the `failed` callback is the only error channel. `AsynchronousFileChannel` is not a `SelectableChannel` — you cannot register it with a `Selector`, and it has no "position channel" sharing with `RandomAccessFile` the way `FileChannel` does. `future.cancel(true)` may or may not stop the underlying OS operation, but the handler (if any) is invoked with `CancelledKeyException`-style failure — do not double-consume a result.

> [!tip] Interview answer
> NIO.2 asynchronous channels start I/O now and deliver results later — via `Future` (poll or `get`) or via a `CompletionHandler` called on an `AsynchronousChannelGroup` thread with the result and your attachment. It is completion-based IO, distinct from selector multiplexing: these channels are not selectable, handlers must never block, and errors arrive in `failed`, not as exceptions in the calling thread.

