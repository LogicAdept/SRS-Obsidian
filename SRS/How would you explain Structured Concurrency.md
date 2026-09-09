<!--
reps: 0
priority: 0
-->
#Java/Concurrency #SRS

# How would you explain Structured Concurrency

> [!abstract] Short answer
> A model — in Java the `StructuredTaskScope` API, a **preview** in `java.util.concurrent` since Java 21 (JEP 453) — where concurrent subtasks are forked, joined, and cancelled **as one unit** inside a lexical scope. If one subtask fails (or succeeds, depending on the policy), the scope shuts down and cancels the rest, so no thread can leak past the block that started it.

## The unit of work is the scope

The owner thread opens a scope in try-with-resources, forks subtasks with `scope.fork(callable)`, and calls `scope.join()` — mandatory: if the scope block exits before joining, the close waits for all subtasks anyway and throws. The policy objects decide when the whole scope shuts down: `ShutdownOnFailure` cancels the remaining subtasks the moment one fails; `ShutdownOnSuccess` cancels the rest the moment one succeeds — the race pattern for redundant services. Shutdown is implemented as interruption of the subtask threads, so subtasks must be responsive to interruption. After joining, results are read from the `Subtask` objects returned by `fork`.

```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Subtask<String> user = scope.fork(() -> findUser(100));
    Subtask<Integer> order = scope.fork(() -> fetchOrder(150));
    scope.join();
    scope.throwIfFailed();
    System.out.println("both ok: " + user.get() + ", " + order.get());
}
```

**Listing 1.** The canonical shape (JDK 21, `--enable-preview`): fork both subtasks, join, fail loudly if either failed, then compose. Output on JDK 21: `both ok: alice, 42`.

## What shutdown does to the siblings

```d2
direction: down
owner: "owner thread\nopens scope" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
u: "subtask: findUser\nslow, still running" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
o: "subtask: fetchOrder\nthrows immediately" {
  width: 270
  height: 100
  style.fill: "#ffebee"
}
sd: "shutdown on failure\ncancel the sibling" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
owner -> u
owner -> o
u -> sd: "interrupted\nstate UNAVAILABLE" {
  style.stroke: "#c62828"
}
o -> sd: "triggers"
```

**Fig. 1.** One failure shuts the scope; the sibling is interrupted and its `Subtask` state stays `UNAVAILABLE` — it will never produce a result, and calling `get()` on it throws `IllegalStateException`.

Running the failure path on JDK 21 printed `failed with: java.lang.IllegalStateException: boom`, then `sibling state after shutdown: UNAVAILABLE` — the cancelled subtask is not `FAILED` with a useful exception; it is simply out of the game. Compared to an ad-hoc `ExecutorService` + `CompletableFuture` pipeline, the lifetimes are confined to the block, cancellation propagates automatically, and thread dumps show the parent-child hierarchy instead of anonymous pool threads. The JEP is explicit that this is not a goal to replace `ExecutorService` and `Future` — unstructured concurrency still has its place, and the model itself kept evolving after 21 (the fifth preview shipped in Java 25 as JEP 505, with a redesigned joiner API). For the surrounding toolbox see [[How would you explain the java.util.concurrent package]]; the scheduling vocabulary it overlaps with is in [[How does multithreading differ from parallelism and async work]] and [[What is the difference between being async and being concurrent]].

> [!warning] It is a preview API — and it changed
> Running it requires `--enable-preview` with the matching `--source` level, and the API is not frozen: `fork` returned `Future` in the incubator versions, returns `Subtask` in 21, and the Java 25 preview replaces the policy classes with joiners. Pin the JDK version before building anything serious on top of it.

> [!tip] Interview answer
> Structured concurrency treats a fan-out as one unit: fork subtasks inside a `StructuredTaskScope`, join them, and the policy cancels the rest on first failure or first success — short-circuit errors, automatic cancellation propagation, hierarchy visible in thread dumps. Preview API in Java 21 (JEP 453), still preview in 25.

