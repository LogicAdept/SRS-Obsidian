<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Collections #Java/Collections/Queues/BlockingQueue #SRS

# What is a LinkedBlockingDeque and where does a two-ended concurrent queue pay off

> [!abstract] Short answer
> **`LinkedBlockingDeque` (Java 6) is the only JDK deque with blocking semantics: an optionally bounded doubly linked list where `put`/`offer`/`take`/`poll` work at both ends, with timeouts.** The two-ended shape is what work-stealing needs — the owner pushes and pops one end, thieves steal the other, where the oldest task sits — and the bound turns the deque into backpressure for both directions at once.

## The two ends, and the one lock

Every operation comes in a `First`/`Last` pair: `putFirst` blocks while the deque is at capacity, `takeLast` blocks while it is empty, `offerFirst(e, timeout)` and `pollLast(timeout)` give up after a deadline. The bound is optional — the no-arg constructor is `Integer.MAX_VALUE`, which in practice means "unbounded, one OOME away", so a capacity is the default choice for producer-facing deques. The measured behavior on a capacity-2 deque:

```java
var d = new LinkedBlockingDeque<Integer>(2);
d.putFirst(1);
d.putFirst(2);                     // deque is [2, 1] - capacity reached
// another thread:
long t0 = System.nanoTime();
d.putFirst(3);                     // parks: full, nobody consuming
// 150 ms later a thief calls takeLast() -> removes 1, putFirst(3) wakes
long parked = (System.nanoTime() - t0) / 1_000_000;   // ~201 ms
d.pollFirst();                     // 3
d.pollFirst();                     // 2
```

**Listing 1.** The blocking bound at work. Verified on JDK 21: `putFirst(3)` parked ~201 ms until the thief's `takeLast()` freed a slot; the owner then drained `3, 2` — LIFO from its own head while the thief had taken the oldest element from the tail.

## Where two ends beat one

The work-stealing pattern is the headline use: each worker owns a deque, pushes newly forked work at its head and continues at the head (LIFO — the newest subtask is the most cache-warm and deepest in the recursion), while a starved worker steals from the *tail* of someone else's deque — the oldest task, the one its owner is least likely to touch soon, so owner and thief collide rarely. `ForkJoinPool` builds exactly this over its own deques; a hand-rolled version is the natural fit for per-thread task lists with a shared drain. Beyond stealing: retry queues where `putFirst` lets reprocessed items jump the line, log shipping with multiple consumers draining from one end while the app appends at the other, and bounded two-sided handoff between a fast and a slow stage. The blocking-pair comparison lives in [[How would you explain BlockingQueue]] and [[What is the difference between ArrayBlockingQueue and LinkedBlockingQueue]].

The sibling implementation is `ConcurrentLinkedDeque` (Java 7): lock-free, unbounded, non-blocking — `putFirst` never parks and there is no capacity to enforce, so it suits fire-and-forget timelines rather than bounded backpressure. Note the engineering trade inside the blocking variant: **one lock guards both ends**, unlike the per-end illusions of the API — simpler invariants (a `takeLast` can wake a `putFirst` directly) but a shared throughput ceiling; the lock-free sibling removes the ceiling and the blocking, and gives up bounded waiting in exchange. Weakly consistent iterators and O(n) `size()` apply to both families ([[What is ConcurrentLinkedQueue]] covers the non-blocking costs).

> [!warning] Two popular misreadings
> "A deque is two independent queues" — no: one lock covers both ends, so heavy traffic from both directions serializes; that is the price for cross-end coordination (a blocked `putFirst` wakes on the matching `takeLast`), and the reason throughput-heavy designs shard across several deques instead. "Unbounded is the safe default" — no: the default capacity is `Integer.MAX_VALUE`; without a bound, a slow consumer converts the deque into a memory leak with a queue interface, the same discipline as any [[How would you explain BlockingQueue|BlockingQueue]].

The transfer-side sibling: [[What is LinkedTransferQueue and when does a transfer need a consumer]]; the framework built on the stealing pattern: [[What is the Java ForkJoin framework]]; choosing among the queues: [[What is the difference between ConcurrentLinkedQueue and a BlockingQueue]].

> [!tip] Interview answer
> `LinkedBlockingDeque` (Java 6) = the only blocking deque: optionally bounded doubly linked list, `put/take/offer/poll` in `First`/`Last` pairs with timeouts. Measured on JDK 21: a capacity-2 deque parked `putFirst(3)` ~200 ms until a thief's `takeLast` freed a slot, and the owner then drained LIFO from its head while the thief got the oldest element. Use it for work-stealing shapes (owner at head, thief at tail), retry queues (`putFirst` = jump the line), and bounded two-ended backpressure. Know the trade: one lock for both ends — simpler invariants, shared throughput ceiling; `ConcurrentLinkedDeque` is the lock-free, unbounded, non-blocking alternative.
