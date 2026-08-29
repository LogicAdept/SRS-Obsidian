<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #Career/Interview/Exercises #SRS

# How do you implement a lock-free stack using Semaphore?

> [!abstract] Short answer
> You **don’t**. A **`Semaphore` is a blocking synchronizer**: `acquire` parks until a permit exists. That is the opposite of **lock-free**. A lock-free stack updates a **head reference** with **`compareAndSet`** (retry on failure). The same exercise under a coherent title: [[How do you implement a lock-free stack with push and pop]]. Permits and fairness: [[What is Semaphore]].

## Blocking permits vs CAS on head

`Semaphore` counts **permits**. `acquire` waits (interruptibly, unless you use `acquireUninterruptibly`); `release` adds a permit. A binary semaphore can stand in for a mutex around an `ArrayDeque`, but waiters **block**. Fairness only changes **who** gets the next permit, not whether anyone sleeps — [[What does the fair flag on Semaphore change]].

Lock-free concurrent structures in `java.util.concurrent` are built on **atomic** updates, not permits. `ConcurrentLinkedQueue` documents a **non-blocking** linked algorithm. A stack is the same idea at one end: nodes linked through `next`, **head** in an `AtomicReference`. `compareAndSet(expected, next)` succeeds only if head is still `expected` (`==`). Failure means another thread won; **retry**. Push links the new node to the old head, then CAS head to the new node. Pop reads head, CAS head to `head.next`. Empty pop is `null` head. CAS vs `getAndAdd`: [[Compare compare and swap with fetch and add]].

`compareAndSet` uses the same memory effects as `VarHandle.compareAndSet`. The JDK has **no** `Semaphore`-based lock-free stack.

```java
import java.util.concurrent.atomic.AtomicReference;

public final class CasStack<E> {
    private static final class Node<E> {
        final E value;
        Node<E> next;

        Node(E value) {
            this.value = value;
        }
    }

    private final AtomicReference<Node<E>> head = new AtomicReference<>();

    public void push(E value) {
        Node<E> n = new Node<>(value);
        Node<E> h;
        do {
            h = head.get();
            n.next = h;
        } while (!head.compareAndSet(h, n));
    }

    public E pop() {
        Node<E> h;
        Node<E> n;
        do {
            h = head.get();
            if (h == null) {
                return null;
            }
            n = h.next;
        } while (!head.compareAndSet(h, n));
        return h.value;
    }
}
```

**Listing 1.** Head pointer CAS. Threads that lose the race **spin**, they do not `acquire` a permit. Not production-hardened (ABA if nodes are reused; no size).

```d2
direction: down
q: "Concurrent stack" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
cas: "AtomicReference.compareAndSet\non head — non-blocking" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
sem: "Semaphore.acquire\nblocks for a permit" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
q -> cas: "lock-free"
q -> sem: "not lock-free"
```

**Fig. 1.** The cue names two tools that do not combine. Use CAS for lock-free; use a semaphore to **limit** concurrent work.

> [!warning] `new Semaphore(1)` around `push`/`pop` is a lock
> Waiters park. A stalled holder stops everyone. That is not lock-free.

> [!warning] Reused nodes + plain CAS can see ABA
> Pop + push of a recycled node can make `compareAndSet` succeed on a head that is not the same abstract stack. `AtomicStampedReference` is the JDK type that pairs a stamp with the reference.

> [!tip] Interview answer
> I would not use a `Semaphore` for a lock-free stack; `acquire` blocks. I keep the top in an `AtomicReference` and `compareAndSet` a new head on push and pop, retrying when the CAS fails. For a real queue I would use `ConcurrentLinkedQueue` rather than hand-rolling.
