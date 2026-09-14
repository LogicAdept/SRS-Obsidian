<!--
reps: 0
priority: 0
-->
#Java/IO #Java/Concurrency/Threads #SRS

# What is a blocking method?

> [!abstract] Short answer
> A **blocking** method does **not return** until its wait is over: a connection, a queue element, a lock, a timer, or a `Future` result. The caller’s thread **stays in that call** (often **WAITING** / **TIMED_WAITING**, or parked in native I/O). **`ServerSocket.accept()`** “**blocks until a connection is made**.” Contrast: **non-blocking I/O** (`SelectableChannel`) or **callbacks / `CompletionStage`** that return **before** the work finishes. **`Future.get()` is still blocking.** Lock-free “non-blocking algorithms” are a **different** use of the word. I/O vs concurrency: [[How would you explain blocking versus non blocking methods in IO and concurrency]]. Queues: [[What makes a BlockingQueue blocking]]. NIO: [[How does NIO provide non-blocking access to resources]]. Algorithms: [[What are non-blocking algorithms]].

## The caller waits here

Typical waits: **`Thread.sleep`**, **`Object.wait`**, **`Lock.lock`**, **`BlockingQueue.take`/`put`**, **`Future.get`**, **`ServerSocket.accept`**, socket **`read`**. Interrupt often throws **`InterruptedException`** (or closes a channel). Virtual threads can **unmount** from a carrier while blocked on many of these — [[How would you explain Virtual Threads]]. Sleep: [[What does it mean to put a Java thread to sleep]]. `wait`: [[How would you explain the Object wait method and waiting on monitors]]. `Future`: [[How would you explain the Future interface in java.util.concurrent]].

**`Thread.State.BLOCKED`** means waiting for a **monitor**, not “any blocking call.” A thread in `accept` is **not** necessarily `BLOCKED`.

```java
Socket s = server.accept();           // returns only after a client connects
Item x = queue.take();                // returns only after a put
Integer v = future.get();             // returns only when the task completes
```

**Listing 1.** Three blocking APIs. `CompletableFuture.thenApply` can **register** work and return immediately; **`join`/`get`** still block.

```d2
direction: down
call: "blocking call" {
  width: 160
  height: 36
  style.fill: "#fff8e1"
}
wait: "thread waits" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
ret: "then return" {
  width: 130
  height: 36
  style.fill: "#e8f5e9"
}
call -> wait -> ret
```

**Fig. 1.** Control stays in the method until the event arrives (or it throws).

> [!warning] Blocking ≠ `Thread.State.BLOCKED`
> Monitor contention is **`BLOCKED`**. Sleep/wait/I/O use **other** states (or native park).

> [!warning] “Non-blocking” is overloaded
> NIO **non-blocking channels**, **async** APIs, and **lock-free** algorithms are three different ideas. `accept` is blocking I/O even if the rest of the app uses `CompletableFuture`.

> [!tip] Interview answer
> A blocking method keeps the calling thread until the wait is done, like accept or take or Future.get. Non-blocking I/O or a completion stage can return before the work finishes. I do not confuse that with lock-free algorithms or with the BLOCKED thread state.
