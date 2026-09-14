<!--
reps: 0
priority: 0
-->
#Java/IO/Streams #SRS

# What are piped streams in Java for?

> [!abstract] Short answer
> **Piped streams are an in-memory, bounded pipe connecting a producing thread to a consuming thread: `PipedOutputStream` -> `PipedInputStream` for bytes, `PipedReader` -> `PipedWriter` for characters.** The reader's buffer decouples the two threads ("a pipe is said to be broken if a thread that was providing data bytes... dies"); the writer **blocks when the buffer is full** and the reader blocks when it is empty — that blocking is the backpressure. Using both ends from a single thread is not recommended "as it may deadlock the thread" ([[What are common concrete InputStream and OutputStream implementations]], [[What is the difference between InputStream OutputStream Reader and Writer]]).

## Thread-to-thread handoff

A pipe is a fixed circular buffer (`PIPE_SIZE = 1024` bytes for `PipedInputStream`) plus thread bookkeeping: the input side remembers which thread last wrote, so if that thread dies, the reader gets `IOException: Pipe broken` instead of waiting forever. Connect the pair explicitly (`out.connect(in)` or `new PipedInputStream(out)`) **before** any thread starts using them. The character twins mirror the byte API one-to-one.

| Property | Behaviour |
| --- | --- |
| Capacity | fixed (1024 bytes); not configurable |
| Full buffer | writer blocks — backpressure, not data loss |
| Empty buffer | reader blocks |
| Producer thread death | reader throws `IOException` ("Pipe broken") |
| Wrong thread usage | possible deadlock — one thread cannot serve both ends |

```java
import java.io.IOException;
import java.io.PipedReader;
import java.io.PipedWriter;

class Pipe {
    public static void main(String[] args) throws InterruptedException {
        try (PipedWriter out = new PipedWriter(); PipedReader in = new PipedReader(out)) {
            Thread producer = new Thread(() -> {
                try (PipedWriter w = out) {
                    w.write("hello");
                    w.write(" pipe");
                } catch (IOException ignored) { }
            });
            Thread consumer = new Thread(() -> {
                try {
                    int c;
                    while ((c = in.read()) != -1) System.out.print((char) c);
                } catch (IOException ignored) { }
            });
            producer.start();
            consumer.start();
            producer.join();
            consumer.join();
            System.out.println();
        }
    }
}
```

**Listing 1.** One thread writes, another drains; the pipe hands the characters across:

```text
hello pipe
```

**Listing 2.** The consumer printed what the producer wrote — same JVM, different threads.

```d2
direction: right
p: "producer thread\nPipedWriter.write" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
buf: "circular buffer (1024)\nfull -> writer blocks" {
  width: 270
  height: 55
  style.fill: "#fff8e1"
}
c: "consumer thread\nPipedReader.read" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
p -> buf -> c
```

**Fig. 1.** The bounded buffer **is** the feature: a slow consumer stalls the producer instead of growing memory.

> [!warning] Same-thread pipes deadlock, and the buffer never grows
> `write` blocks on a full buffer; if the **only** reader is the thread you are blocking, you wait forever — the javadoc's deadlock warning. The 1024-element buffer is fixed: for large in-memory handoffs a `BlockingQueue` of chunks (or `java.nio.channels.Pipe` for channel-oriented code) scales better. Piped streams work **within one JVM** — for cross-process IPC you need OS pipes or sockets. And the reader only notices a dead producer when it tries to read past what was already buffered.

> [!tip] Interview answer
> Piped stream pairs (byte and character flavors) connect two threads through a fixed 1024-byte circular buffer: the writer blocks when full, the reader when empty, producer death breaks the pipe with an IOException. It is bounded backpressure inside one JVM — connect before use, never use both ends from one thread, and reach for a `BlockingQueue` when you need more capacity.

