<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Collections #Java/Collections/Queues #SRS

# What is LinkedTransferQueue and when does a transfer need a consumer

> [!abstract] Short answer
> **`LinkedTransferQueue` (Java 7) is an unbounded queue with two personalities: `put`/`offer` buffer elements for late consumers like any `BlockingQueue`, while `transfer(e)` is a rendezvous — it parks until a consumer *removes* the element.** `tryTransfer` makes the rendezvous non-blocking or timed, and `hasWaitingConsumer()` reports whether demand is waiting. It is the only JDK queue where buffering and per-element handoff are a per-call choice.

## The two personalities in one class

A `LinkedBlockingQueue` always buffers: an `offer` succeeds even when no consumer exists, and the element waits. A `SynchronousQueue` never buffers: capacity zero, a producer's `offer` fails unless a consumer is parked at that instant. `LinkedTransferQueue` implements `TransferQueue` (which extends `BlockingQueue`) and covers both behaviors with one node-based structure: buffered methods (`put`, `offer`, `add`) enqueue for whoever comes later, rendezvous methods (`transfer`, `tryTransfer`) require an actual consumer. The measured contrast, with no consumer anywhere:

```java
var lbq = new LinkedBlockingQueue<String>();
var sq  = new SynchronousQueue<String>();
var ltq = new LinkedTransferQueue<String>();

boolean lbqOk = lbq.offer("x");   // true  - buffered
boolean sqOk  = sq.offer("x");    // false - capacity 0, nobody to hand to
ltq.put("y");                     // buffered like the LinkedBlockingQueue
boolean ltqTry = ltq.tryTransfer("z"); // false - rendezvous attempt, no consumer
// lbq.size() == 1, ltq.size() == 1
```

**Listing 1.** Three queue personalities without a consumer. Verified on JDK 21: `LinkedBlockingQueue.offer` and `LinkedTransferQueue.put` both buffered (`size == 1`), `SynchronousQueue.offer` returned false, and `tryTransfer` returned false — the buffered and rendezvous halves are independent calls.

## transfer and tryTransfer, measured

`transfer(e)` enqueues the element in a "waiting for consumer" state and parks the producer until a consumer takes it; the producer returns only after the handoff completed. `tryTransfer(e)` returns immediately — true if a consumer was already waiting, false otherwise — and the timed overload waits up to a deadline. `hasWaitingConsumer()` and `getWaitingConsumerCount()` expose the demand side, which makes a producer-side throttle possible without polling the queue's size.

```java
var q = new LinkedTransferQueue<String>();
long t0 = System.nanoTime();
new Thread(() -> { try { q.transfer("payload"); } catch (InterruptedException ignored) {} }).start();
Thread.sleep(300);                 // consumer arrives late
boolean waiting = q.hasWaitingConsumer(); // false here - see warning below
String taken = q.take();           // releases the parked producer
long ms = (System.nanoTime() - t0) / 1_000_000;  // ~304 ms

new Thread(() -> { try { Thread.sleep(100); q.take(); } catch (InterruptedException ignored) {} }).start();
Thread.sleep(200);                 // consumer is now parked in take()
boolean handed = q.tryTransfer("fast");   // true - immediate handoff
```

**Listing 2.** Rendezvous timing. Verified on JDK 21: `transfer` parked ~304 ms until `take()` consumed the element; with a consumer parked in `take()`, `tryTransfer` returned true instantly — the second handoff never touched the buffer.

## Where it beats its neighbors

Against `[[What is a SynchronousQueue|SynchronousQueue]]`: both give handoff semantics, but the synchronous queue blocks *every* producer until a consumer shows up, while the transfer queue buffers burst traffic and lets each element opt into strict handoff with `transfer` — backpressure per element instead of per producer. Against a plain `LinkedBlockingQueue`: a buffered consumer never knows the producer finished the handoff; `transfer` is producer-side acknowledgment — when it returns, the element has crossed the boundary, which is the semantics message-passing code wants for work delegation. The costs are the usual linked-queue set: CAS-heavy unbounded nodes (an unbounded queue out of control is an OOME, so producers still need a bound somewhere), weakly consistent iterators, `size()` that traverses the chain, no fairness knob. The sibling single-queue comparisons: [[What is the difference between ConcurrentLinkedQueue and a BlockingQueue]] and [[What makes a BlockingQueue blocking]].

> [!warning] Two popular misreadings
> "transfer is put for impatient producers" — no: `transfer` returns *only after a consumer removed the element*; it is an acknowledgment, and using it as a drop-in `put` serializes producers against consumer speed. "hasWaitingConsumer shows my parked transfers" — no: the flag watches *consumers* only; a producer parked inside `transfer` is invisible to it (measured in Listing 2: the flag read false while the producer was the one waiting). Counting demand therefore needs consumers parked in `take`/`poll`, not the other side.

The deque sibling: [[What is a LinkedBlockingDeque and where does a two-ended concurrent queue pay off]]; the simple non-blocking cousin: [[What is ConcurrentLinkedQueue]]; how executor queues saturate: [[What happens when a thread pool queue is full and a new task arrives]].

> [!tip] Interview answer
> `LinkedTransferQueue` (Java 7) = unbounded `TransferQueue`: `put`/`offer` buffer like any `BlockingQueue`, `transfer(e)` parks until a consumer removes the element, `tryTransfer` is the instant/timed rendezvous probe, `hasWaitingConsumer()` reports parked consumers. Measured on JDK 21: with no consumer, `put` buffered (`size == 1`) while `tryTransfer` returned false; `transfer` parked ~300 ms until `take()`, and with a consumer parked in `take()` `tryTransfer` returned true immediately. Use it when you want one queue that absorbs bursts *and* can hand off specific elements with producer-side acknowledgment — remembering it is unbounded, weakly consistent, and `size()` is a traversal.
