<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Synchronizers #SRS

# How does Exchanger swap data between two threads?

> [!abstract] Short answer
> Each thread calls `exchange(x)` on the same `Exchanger<V>`. The first arriver **blocks**; when a partner calls `exchange(y)`, they **pair**: each returns the other’s argument and continues. It is a bidirectional form of `SynchronousQueue`: a pair swaps objects, not a bounded queue and not an N-party barrier.

## Pair, swap, return the partner’s object

`Exchanger` (Java 5+) is a synchronization point where threads **pair and swap** objects. There is no party count in the constructor — matching is always **two at a time**. If a partner is already waiting, the caller transfers `x`, wakes that waiter, and returns immediately with the waiter’s object. If the slot is empty, the caller parks until another thread enters, an interrupt, or (timed form) a timeout.

```java
import java.util.concurrent.Exchanger;

public final class ParcelSwap {
    public static void main(String[] args) {
        Exchanger<String> exchanger = new Exchanger<>();
        new Thread(() -> swap(exchanger, "from-A")).start();
        new Thread(() -> swap(exchanger, "from-B")).start();
    }

    private static void swap(Exchanger<String> exchanger, String mine) {
        try {
            String theirs = exchanger.exchange(mine);
            System.out.println(mine + " got " + theirs);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
```

**Listing 1.** Two threads each offer a `String` and assign the return value. The documented pipeline shape is the same assignment: `currentBuffer = exchanger.exchange(currentBuffer)` between a filling thread and an emptying thread.

```d2
direction: down
offer: "A: exchange(x)\nB: exchange(y)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
pair: "pair at the Exchanger\nfirst waiter is released" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
done: "A returns y\nB returns x" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
offer -> pair
pair -> done
```

**Fig. 1.** Successful pairing: actions before `exchange` in each thread happen-before actions after the matching `exchange` returns in the other thread.

The timed overload `exchange(x, timeout, unit)` throws `TimeoutException` if no partner arrives (`timeout <= 0` means do not wait). OpenJDK accepts `null` as a payload by translating it to an internal sentinel for the slot algorithm, then translating back — a `null` offer is still a rendezvous, not a skip. Both sides passing `null` is a barrier of two with no data.

A third `exchange` does not join an in-flight pair; it waits for the **next** partner. The same instance can serve many successive (or concurrent) pairs; under contention the OpenJDK implementation spreads waits across an elimination arena. That is still pairwise swap, not `CyclicBarrier`’s fixed N-party trip — [[How does CyclicBarrier run a barrier action when all parties arrive]]. A start gate that releases many waiters without swapping objects is a latch — [[How do you use CountDownLatch so several threads start together]].

> [!warning] The first thread parks until a partner exists
> There is no `countDown` to open an empty exchanger. A forgotten second `exchange` leaves the first thread blocked (or until interrupt / timeout). Catch `InterruptedException` and restore the interrupt flag; do not treat a timeout as a successful swap.

> [!warning] `null` still waits
> Passing `null` does not mean “no meeting.” You still pair, and you still receive whatever the partner offered (including `null`). Use that when one side has nothing to hand off — not as a non-blocking probe.

> [!tip] Interview answer
> Two threads call `exchange` on one `Exchanger<V>`: the first waits, the second completes the pair, and each returns the other’s object. That is a bidirectional handoff, as in swapping full and empty buffers in a pipeline. A third caller waits for its own partner; `null` is a legal payload that still rendezvouses; interrupt and the timed overload are the only ways out without a match.
