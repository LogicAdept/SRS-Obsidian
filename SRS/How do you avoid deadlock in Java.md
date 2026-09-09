<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS

# How do you avoid deadlock in Java

> [!abstract] Short answer
> Break at least one Coffman condition. In practice: acquire nested locks in **one global order** (circular wait becomes impossible), or use **`ReentrantLock.tryLock` with a timeout** and back off — release what you hold and retry. The strongest fix is structural: no nested locks at all, small critical sections, and never call unknown code while holding a lock.

## Prevention by ordering

The cheapest lever is condition four: if every thread acquires the same set of monitors in the same order, the wait-for graph cannot close, because the "last edge" that would form the cycle never happens. The order must be global — one convention for the whole codebase, derived from something stable like an entity id, not from local convenience. Acquire in ascending order, release in reverse, and keep the critical section as short as the logic allows.

```java
Thread ordered = new Thread(() -> {
    lockA.lock();
    try {
        lockB.lock();
        try {
            System.out.println("ordered acquisition finished");
        } finally {
            lockB.unlock();
        }
    } finally {
        lockA.unlock();
    }
});
```

**Listing 1.** The `lock` / `try` / `finally` / `unlock` shape from the `ReentrantLock` documentation: `lock()` blocks until acquired, and the `finally` guarantees the release. Output on JDK 21: `ordered acquisition finished`, `still alive: no deadlock`.

## Recovery by timed acquisition

When a total order is impractical (many lock combinations, order not known up front), replace indefinite waiting with bounded waiting: `tryLock(timeout, unit)` returns `false` if the lock did not become free in time. The protocol: acquire the first lock, try the second with a timeout, and on failure release everything, back off, and retry. This breaks the "hold and wait forever" property — a cycle can still form momentarily, but some thread gives up and the cycle dissolves. On JDK 21 the demo thread printed `both locks acquired on attempt 1` and `thread finished: no deadlock`.

```d2
direction: down
nested: "Nested locks needed?" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
order: "Acquire in one\nglobal order" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
trylock: "ReentrantLock.tryLock\nwith timeout + backoff" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
none: "No nested locks,\nsmall critical sections" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
nested -> order: "yes, orderable"
nested -> trylock: "yes, not orderable"
nested -> none: "redesign"
```

**Fig. 1.** Decision ladder: drop nesting when you can, order what remains, and use timed acquisition where ordering is impossible.

Two cautions complete the picture. First, `tryLock` backoff can slide into livelock — threads actively retrying without progress — so add jitter or escalation, see [[What is livelock]]. Second, ordering and timeouts protect lock cycles, but a thread that blocks waiting for another thread's result (for example, two workers exchanging futures) can deadlock with zero shared locks; that is a design problem, not a lock-ordering one. Detection tools — `ThreadMXBean.findDeadlockedThreads`, thread dumps from `jstack` — verify the fix; the whole cycle mechanism is explained in [[What is deadlock]] and its conditions in [[What four conditions are required for a deadlock]]. The lock API itself belongs to the toolbox described in [[How would you explain the java.util.concurrent package]].

> [!warning] Ordering only works if it is truly global
> One module taking A-then-B while another takes B-then-A reintroduces the cycle even though each call site "looks" ordered. Derive the order from a stable, shared key — never from call-site convenience — and note that the untimed `tryLock()` does not honor a lock's fairness setting: it barges in even when others wait.

> [!tip] Interview answer
> I break a Coffman condition: a global lock acquisition order removes circular wait; `ReentrantLock.tryLock` with timeout and backoff caps hold-and-wait; the best redesign removes nested locks altogether. Detection via `jstack` or `ThreadMXBean` verifies there is no cycle left.

