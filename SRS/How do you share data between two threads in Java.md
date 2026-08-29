<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Threads #Java/Collections/Concurrency #Java/JMM #SRS

# How do you share data between two threads in Java?

> [!abstract] Short answer
> They share **heap objects**, not each other’s stacks. A shared field is not enough: you need a **happens-before** (monitor unlock/lock, `volatile`, `j.u.c`, `Thread.start` / `join`). The usual handoff is a thread-safe queue such as **`BlockingQueue`**: `put` happens-before `take` in the other thread.

## Shared reference plus an ordering

Objects live on the **shared heap**; frames are private — [[How do the stack and heap differ for multithreading in Java]]. Two threads with a reference to the same object still **data-race** if they conflict without synchronization.

Built-in orderings: an **unlock** of a monitor happens-before a later **lock** of that monitor (`synchronized` / `wait`–`notify` on that object). A **volatile write** happens-before a later read of that field. `Thread.start` happens-before work in the new thread; a successful **`join`** happens-before the joiner’s later actions. Two-thread swap of one payload: [[How does Exchanger swap data between two threads]]. Condition queues: [[How do methods wait and notify notifyAll]].

`BlockingQueue` (Java 5+) is built for producer–consumer. `put` waits for space; `take` waits for an element. Implementations are **thread-safe**; queuing methods are atomic. Actions **before** placing an element happen-before actions **after** that element is taken in another thread. `null` is forbidden (`poll` uses it as “failed”). Bulk `addAll` / `removeAll` are **not** necessarily atomic. No built-in close: a common pattern is a poison element.

```java
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

public final class ShareViaQueue {
    public static void main(String[] args) {
        BlockingQueue<String> q = new LinkedBlockingQueue<>();
        new Thread(() -> {
            try {
                q.put("hello");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
        new Thread(() -> {
            try {
                String s = q.take();
                System.out.println(s);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }).start();
    }
}
```

**Listing 1.** One shared queue object. The producer’s writes to `"hello"` happen-before the consumer’s use of `s`. The API allows **many** producers and consumers on the same queue, not only two.

```d2
direction: down
share: "same heap object" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
hb: "happens-before\nlock / volatile / j.u.c / start / join" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
race: "plain field, no order\ndata race" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
share -> hb: "safe publication"
share -> race: "not enough"
```

**Fig. 1.** Sharing a reference is necessary and not sufficient. Atomics (`getAndAdd`, `compareAndSet`) are another `j.u.c` path for a single variable.

> [!warning] A shared `ArrayList` or unsynchronized map is not a concurrent structure
> `BlockingQueue` queuing methods are thread-safe. `HashMap` / `ArrayList` are not. `Collections.synchronizedList` is one mutex, not a blocking handoff.

> [!warning] `put`/`take` throw `InterruptedException`
> Restore the interrupt flag if you abort. Do not treat a swallowed interrupt as a successful transfer.

> [!tip] Interview answer
> Threads share heap objects, not stacks. You still need happens-before: `synchronized`, `volatile`, or a concurrent collection. For messages, `BlockingQueue.put` / `take` is the usual producer–consumer API and is safe for many threads, not only two.
