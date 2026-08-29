<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Atomics #SRS

# How would you write a minimal non-blocking stack (push and pop)?

> [!abstract] Short answer
> A **lock-free stack** is an **`AtomicReference` to the head node**. **`push`**: allocate a node, point it at the current head, **`compareAndSet`** until the head **is** that node. **`pop`**: read head; if null, empty; else **CAS** head to **`head.next`**. Empty `pop` returning **`null`** matches **`Deque.pollFirst`**, not **`java.util.Stack.pop`** (that throws). A **`Semaphore(1)`** around a linked list is a **mutex**, not non-blocking. Clear sibling: [[How do you implement a lock-free stack with push and pop]]. Semaphore version: [[How do you implement a lock-free stack using Semaphore]]. Prefer a **`Deque`**: [[How do you use a Deque as a stack]]. Avoid **`java.util.Stack`**: [[Why is java.util.Stack discouraged and what should you use instead]].

## CAS the head, do not lock it

`compareAndSet` is one atomic RMW on the **reference**. Failed CAS means another thread won; **retry** with a fresh `get()`. Writes to the new node’s fields **before** a successful CAS happen-before a `pop` that **observes** that node as head. Atomics: [[How would you explain Java atomic types in java.util.concurrent.atomic]].

**`Semaphore(1)` + `acquireUninterruptibly`** is **exclusion**: waiters **block**. That is the opposite of lock-free. Permits: [[What is Semaphore]]. If you **reuse** node objects, **ABA** can make a CAS succeed against a **recycled** head with a **stale** `next`; always allocating a new node (as below) avoids that reuse.

```java
final class LockFreeStack<E> {
    private static final class Node<E> {
        final E value;
        Node<E> next; // set only before this node is published as head
        Node(E value) { this.value = value; }
    }

    private final AtomicReference<Node<E>> head = new AtomicReference<>();

    void push(E value) {
        Node<E> n = new Node<>(value);
        Node<E> h;
        do {
            h = head.get();
            n.next = h;
        } while (!head.compareAndSet(h, n));
    }

    E pop() {
        Node<E> h;
        Node<E> next;
        do {
            h = head.get();
            if (h == null) return null;
            next = h.next;
        } while (!head.compareAndSet(h, next));
        return h.value;
    }
}
```

**Listing 1.** Two methods, lock-free. One node per `push`; on a failed CAS only `next` is rewritten **before** the node is published.

```d2
direction: down
p: "push: new node → old head" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
cas: "CAS head" {
  width: 140
  height: 36
  style.fill: "#e3f2fd"
}
pop: "pop: CAS head to next" {
  width: 200
  height: 40
  style.fill: "#fff8e1"
}
p -> cas
cas -> p: "lost race"
cas -> pop: "head published"
```

**Fig. 1.** Linearization is the successful CAS on `head`. Losers retry.

> [!warning] `Semaphore(1)` is not a non-blocking stack
> It is a **binary semaphore used as a lock**. Callers **wait**. That second sketch does not meet the lock-free cue.

> [!warning] `pop` on empty
> Returning `null` hides “empty vs stored null” if `E` is nullable. `Stack.pop` throws **`EmptyStackException`**. Pick one and document it.

> [!tip] Interview answer
> I CAS a linked head: push links a new node and swings head, pop swings head to next, retrying on failure. That is lock-free; a one-permit semaphore is just mutual exclusion. I would use ArrayDeque or ConcurrentLinkedDeque in production instead of java.util.Stack.
