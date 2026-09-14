<!--
reps: 0
priority: 0
-->
#Java/JMM #Java/Collections/Concurrency #SRS

# What memory consistency do concurrent collections guarantee in Java

> [!abstract] Short answer
> **Actions in a thread prior to placing an object into any concurrent collection happen-before actions subsequent to the access or removal of that element from the collection in another thread** — the memory consistency property of `java.util.concurrent` collections. A queue hand-off is therefore a valid publication channel.

The property turns every `put`/`offer`/`add` into a release and every `take`/`poll`/`get` of that element into an acquire, so whatever the producer built before enqueueing is fully visible to the consumer that dequeues it ([[How do you implement producer-consumer with a BlockingQueue]]). This is the foundation of worker-pool designs: tasks are objects, and submitting an object into a concurrent queue publishes its state to whichever worker takes it. Internally the guarantee is implemented with the same primitives the model defines — for example `ConcurrentHashMap` nodes hold `volatile V val` and `volatile Node<K,V> next` fields, so element reads acquire through volatile semantics, and `BlockingQueue` implementations lock or CAS through `volatile`/VarHandle state ([[What is a SynchronousQueue]]).

```d2
direction: right
p: "Producer thread" {
  b: "build order DTO\n(plain writes)" { style.fill: "#e3f2fd" }
  put: "queue.put(order)\n(release)" { style.fill: "#fff3e0" }
  b -> put: "program order"
}
q: "BlockingQueue\n(volatile / lock state)" { style.fill: "#f3e5f5" }
c: "Consumer thread" {
  take: "order = queue.take()\n(acquire)" { style.fill: "#fff3e0" }
  u: "reads order fields\n-> fully visible" { style.fill: "#e8f5e9" }
  take -> u: "program order"
}
put -> q: "enqueue"
q -> take: "dequeue\nsame element"
```

**Fig. 1.** The collection's internal volatile/lock state adds the synchronizes-with edge between enqueue and dequeue of the same element; program order on both sides extends it to the whole payload.

```java
BlockingQueue<Order> queue = new LinkedBlockingQueue<>();

// producer
Order order = new Order("AAPL", 42);   // constructor writes
order.setPrice(199.5);
queue.put(order);                      // release: everything above is published

// consumer (another thread)
Order o = queue.take();                // acquire on that element
System.out.println(o.symbol());        // guaranteed to see all producer writes
```

**Listing 1.** The consumer sees a fully initialized `Order` without any synchronization of its own — the collection hand-off carries the edge.

> [!warning] The edge covers hand-off of that element, not everything, forever
> Writes the producer makes *after* `put` are outside the edge — only pre-enqueue state is published. Reusing and mutating a mutable object that is already in flight is a race: the consumer may see mid-update state for accesses that race with the producer's later writes. And the guarantee belongs to the concurrent collections — hand-rolling a "queue" over a plain `ArrayList` has none of it ([[Is there a universal fix for race conditions in concurrent code]]). Iteration semantics of weakly consistent iterators are a separate story from element hand-off ([[What is the difference between a race condition and a data race]]).

> [!tip] Interview answer
> **Placing an object into any concurrent collection happens-before a later access or removal of that element in another thread — the canonical j.u.c memory consistency property. Queues publish task objects to workers, maps publish values to readers, all without extra synchronization. It covers state written before the insert of that element; post-insert mutations of the same object are not ordered.**
