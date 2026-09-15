<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Concurrency/Executors #Java/Streams/Operations #Java/JMM/HappensBefore #SRS

# What happens when a sequential stream creates `CompletableFuture` tasks and joins each one in `forEach`?

> [!abstract] Short answer
> **Yes — it prints 1 through 10, in order, on every run.** A sequential pipeline is pulled one element at a time in the calling thread, so each `runAsync` task is created only after the previous `join` has returned; at most one task is ever in flight. The order is chained together by two happens-before edges — executor submission and completion-to-retrieval — not by the stream itself. The price: the code is **secretly serial**, `runAsync` buys zero concurrency here.

## Create, join, then create again

```java
IntStream.range(1, 11)
        .mapToObj(i -> CompletableFuture.runAsync(() -> System.out.println(i)))
        .forEach(CompletableFuture::join);
```

**Listing 1.** The puzzle: `runAsync` submits one printing task per element, and the terminal `forEach` immediately joins that same task.

The source is a `range` stream — a *sequential ordered* `IntStream` from 1 (inclusive) to 11 (exclusive), so it carries a defined encounter order, and without `.parallel()` the whole pipeline is walked by the calling thread. Nothing runs until the terminal starts ([[When does a Java stream pipeline actually start executing]]). When `forEach` pulls element 1, the `mapToObj` mapper runs first, calls `runAsync`, and gets back a future whose task is already handed to the `ForkJoinPool.commonPool()`; the same pull then invokes the `forEach` action for element 1 — `join()` — and only after it returns is element 2 pulled. On an ordered stream the operations are constrained to the encounter order, and `forEach`'s "may not respect encounter order" clause is scoped to *parallel* pipelines ([[What is the difference between forEach and forEachOrdered on a stream]]).

## The two edges that chain the prints

The printed order is not a stream promise. It falls out of the executor memory-consistency pair — the same edges behind [[What memory consistency does executor submission guarantee in Java]] and [[What memory consistency does Future get guarantee in Java]]:

* the actions in a thread prior to submitting a task happen-before the task begins;
* the actions of the asynchronous computation happen-before the retrieval of its result in the waiting thread — the edge the package documentation states for `Future.get()`, whose role `join()` plays for `CompletableFuture` with an unchecked exception on the exceptional path.

So `println(1)` precedes `task 1` completing, completion precedes `join(1)` returning, the return precedes the mapper for element 2, and the next submission precedes `println(2)`. Transitively ([[How would you explain the happens-before guarantee in the Java Memory Model]]), every print precedes the next: 1, 2, …, 10. Nothing here depends on pool size — with a common pool of parallelism one, or the new-Thread-per-task fallback the class documentation names for a common pool below two, the same chain holds.

```d2
direction: down
m1: "main thread\nmapToObj(1) -> runAsync submits task 1" {
  width: 380
  height: 72
  style.fill: "#e3f2fd"
}
t1: "common pool\ntask 1 prints 1, completes" {
  width: 330
  height: 72
  style.fill: "#fff3e0"
}
m2: "main thread\njoin(1) returns -> mapToObj(2)\nrunAsync submits task 2" {
  width: 390
  height: 92
  style.fill: "#e3f2fd"
}
t2: "common pool\ntask 2 prints 2, completes" {
  width: 330
  height: 72
  style.fill: "#fff3e0"
}
end: "…repeats through 10\nat most one task in flight" {
  width: 350
  height: 72
  style.fill: "#e8f5e9"
}

m1 -> t1: "submission edge"
t1 -> m2: "print 1 happens-before\njoin(1) returns"
m2 -> t2: "submission edge"
t2 -> end
```

**Fig. 1.** The two happens-before edges — submission, and completion-to-retrieval — plus the single-threaded pull loop serialize the prints; the tasks never overlap.

## The variant that loses the guarantee

```java
List<CompletableFuture<Void>> futures = IntStream.range(1, 11)
        .mapToObj(i -> CompletableFuture.runAsync(() -> System.out.println(i)))
        .collect(Collectors.toList());        // all 10 submitted up front

futures.forEach(CompletableFuture::join);     // join order fixes nothing
```

**Listing 2.** Collecting the futures first submits every task before any `join` runs.

Now ten tasks run concurrently on the common pool, and joining them in list order says nothing about when each one *printed*: task 3 can print before task 2 finishes. The join order still orders the *returns* — that half of the contract stands ([[What memory consistency does Future get guarantee in Java]]) — but the side effects inside the tasks are ordered by the scheduler, not by the list. This collect-then-join shape is the correct way to actually get parallelism; it just cannot promise print order.

> [!warning] Where the intuition breaks
> *Async ⇒ unordered* is wrong **here**, and *the stream keeps the order* is the wrong **reason**: the stream only sequences create-and-join on the calling thread, while the print order lives in the happens-before chain. Swap `forEach` for `collect(toList())` and the guarantee is gone. Adding `.parallel()` is worse: `forEach` is explicitly nondeterministic there, the mapper application order is unconstrained, and the pipeline now joins tasks on the same shared pool it runs on ([[What is the difference between sequential and parallel streams in Java]]) — blocking workers on tasks that may be queued behind them.

> [!tip] Interview answer
> **Yes: strictly 1, 2, …, 10, on every run.** A sequential stream is pulled element by element, so each future is created after the previous `join` returned — the tasks never overlap — and the submission plus completion happens-before edges chain the prints in order. But it is a serial program wearing an async costume: collect the futures first and the print order becomes nondeterministic.
