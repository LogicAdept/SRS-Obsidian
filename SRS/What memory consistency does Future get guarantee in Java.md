<!--
reps: 0
priority: 0
-->
#Java/JMM/HappensBefore #Java/Concurrency/Executors #SRS

# What memory consistency does Future get guarantee in Java

> [!abstract] Short answer
> **The actions taken by the asynchronous computation represented by a `Future` happen-before actions subsequent to the retrieval of the result via `Future.get()` in another thread.** A successful `get()` publishes everything the task did — the receiving thread sees the full result state.

This is the return half of the executor pair: submission publishes to the task at start, and completion publishes from the task to everyone who calls `get` ([[What memory consistency does executor submission guarantee in Java]]). The implementation shows the mechanism literally: `FutureTask.set(V v)` first writes the outcome — `outcome = v` — and then stores the terminal state with a release write, `STATE.setRelease(this, NORMAL)`; `get()` observes the state change with acquire semantics and only then reads `outcome`, forming a release-acquire pair on one variable ([[How would you explain FutureTask in Java concurrency]]). Multiple threads may all call `get()` — each one receives the same publication edge.

```d2
direction: right
t: "Task thread" {
  width: 200
  height: 74
  c: "compute result\n(plain writes)" {
    width: 200
    height: 104
    style.fill: "#e3f2fd"
  }
  st: "outcome = v; STATE.setRelease(NORMAL)\n(release)" {
    width: 340
    height: 104
    style.fill: "#fff3e0"
  }
  c -> st: "program order"
}
m: "Main thread" {
  width: 200
  height: 74
  g: "future.get()\n(acquire on state)" {
    width: 222
    height: 104
    style.fill: "#fff3e0"
  }
  r: "reads result\n-> fully visible" {
    width: 204
    height: 104
    style.fill: "#e8f5e9"
  }
  g -> r: "program order"
}
st -> g: "release -> acquire\n(same FutureTask state)"
```

**Fig. 1.** `FutureTask` publishes the outcome before releasing the terminal state; `get()` acquires the state and therefore observes the outcome and all earlier task writes.

```java
Map<String, Stats> result = new HashMap<>();     // task-owned object

Future<Map<String, Stats>> f = pool.submit(() -> {
    result.putAll(computeStats());               // task writes
    return result;
});

Map<String, Stats> r = f.get();                  // successful return = acquire
for (var e : r.entrySet()) {                     // guaranteed fully populated
    render(e.getValue());
}
```

**Listing 1.** After a successful `get()`, the map's contents computed inside the task are visible to the main thread with no further synchronization.

> [!warning] No successful completion, no edge
> The property is about retrieval of the result: a `get()` that returns after a timeout while the task is still running delivers nothing, and reading the task's fields directly — without going through the future — races ([[How would you explain the Future interface in java.util.concurrent]]). An exceptional completion also publishes (the exception is stored as the outcome before the terminal state), so `get()` throwing `ExecutionException` still means the task's work up to the failure is visible. But if you complete a `CompletableFuture` manually from yet another thread, the publication is made by *that* thread's `complete()` call, not by the original producer — the chain of edges must actually connect your writes ([[What is CompletableFuture for]]).

> [!tip] Interview answer
> **Actions of the async computation happen-before the return of a successful `Future.get()` in any other thread: completion is stored via a release write and `get` acquires it, so the caller sees the whole result. A timed get that expires early gives no edge, and manual completion publishes from the completing thread — the usual traps.**
