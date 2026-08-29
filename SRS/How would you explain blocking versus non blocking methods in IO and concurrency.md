<!--
reps: 0
priority: 0
-->
#Java/IO #Java/NIO #Java/Concurrency #SRS

# How would you explain blocking versus non blocking methods in IO and concurrency?

> [!abstract] Short answer
> A **blocking** call **parks the caller** until the operation can finish (`InputStream.read`, `Lock.lock`, `BlockingQueue.take`, `Future.get`). A **non-blocking** I/O call **returns at once**, possibly transferring **fewer bytes than asked, or none** (`SelectableChannel` in non-blocking mode). **Async** NIO starts work and gives a **`Future` / `CompletionHandler`** — waiting on that `Future` is still blocking. Concurrent “non-blocking” often means **CAS / lock-free**, not NIO. Channels: [[How does NIO provide non-blocking access to resources]]. Queues: [[What makes a BlockingQueue blocking]].

## Two vocabularies, one word

**I/O.** Classic streams keep the thread in the read/write until the OS has data or space. NIO **channels** are interruptible and asynchronously closeable. A **`SelectableChannel`** is created in **blocking** mode: every I/O waits until it completes. **`configureBlocking(false)`**: I/O **never blocks**; it may transfer a short count or **zero**. Put the channel in non-blocking mode, **register** with a **`Selector`**, then **select** for readiness. Readiness is a **hint**, not a guarantee — you must tolerate a would-block. Multiplexed non-blocking I/O is documented as more scalable than **one thread per connection**. Must be non-blocking **before** `register`; cannot go back to blocking until deregistered.

**Asynchronous channels** (1.7+): methods return a **`Future`** or take a **`CompletionHandler`**. The channel is non-blocking at initiation; **`Future.get`** still waits. A group uses an **`ExecutorService`** to run handlers — [[How does multithreading differ from parallelism and async work]].

**Concurrency.** `lock()` / `take()` / `await()` **disable the thread for scheduling** until a permit, element, or signal exists. `tryLock` / `offer` / `poll` return immediately with success or failure. `ConcurrentLinkedQueue` is a **non-blocking** linked algorithm (CAS). That is **not** the same as `configureBlocking(false)`. Interrupt of a thread blocked on an **InterruptibleChannel** closes the channel (`ClosedByInterruptException`). Algorithms: [[What are non-blocking algorithms]]. Advantages vs `java.io`: [[How would you explain advantages of Java NIO over classic blocking IO]].

```java
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;

public final class NonBlockingRead {
    static int tryRead(SocketChannel ch, ByteBuffer buf) throws java.io.IOException {
        ch.configureBlocking(false);
        return ch.read(buf);
    }
}
```

**Listing 1.** Non-blocking read: `read` may return `0` if no bytes are ready. In blocking mode the same `read` would park until at least one byte (or EOF).

```d2
direction: down
blk: "blocking: caller parked\nread / lock / take / get" {
  width: 320
  height: 55
  style.fill: "#fff8e1"
}
nbio: "NIO non-blocking: return now\n0 or short count" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
nbc: "j.u.c non-blocking: CAS\nno park on the hot path" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** Same English word, three mechanisms. Async I/O still blocks if you `get()` the `Future`.

> [!warning] `Future.get()` after `read(...)` on an async channel is blocking
> Initiation was non-blocking. The waiter is not. Use a `CompletionHandler` or poll `isDone` if you must not park.

> [!warning] Selector “ready” can still block
> The specification says treat readiness as a hint. Code that assumes `read` cannot block after select is wrong.

> [!tip] Interview answer
> Blocking means this thread waits inside the call until the operation can finish. Non-blocking NIO returns immediately, maybe with zero bytes, and you multiplex with a selector. In concurrency, non-blocking usually means try/CAS so nobody parks; `take()` on a `BlockingQueue` is the opposite.
