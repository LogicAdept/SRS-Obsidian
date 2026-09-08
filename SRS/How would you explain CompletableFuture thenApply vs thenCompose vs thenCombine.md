<!--
reps: 0
priority: 0
-->
#Java/Concurrency/Executors #Java/Async #SRS

# How would you explain `CompletableFuture` thenApply vs thenCompose vs thenCombine?

> [!abstract] Short answer
> All three schedule a dependent step on a **`CompletionStage`** — the chaining half of [[What is CompletableFuture]]. **`thenApply`** transforms the value — a **map**: `T → U`. **`thenCompose`** is the **flatMap**: the function itself returns a **`CompletionStage<U>`**, so you get `CompletableFuture<U>`, not a nested `CompletableFuture<CompletableFuture<U>>`. **`thenCombine`** merges **two already-running, independent** stages: when **both** complete normally, a **`BiFunction`** receives both results. Each has `*Async` twins, optionally taking an explicit executor. Deeper mechanics: [[How would you explain CompletableFuture]].

## Signatures

```java
<U> CompletableFuture<U> thenApply(
        Function<? super T, ? extends U> fn);

<U> CompletableFuture<U> thenCompose(
        Function<? super T, ? extends CompletionStage<U>> fn);

<U, V> CompletableFuture<V> thenCombine(
        CompletionStage<? extends U> other,
        BiFunction<? super T, ? super U, ? extends V> fn);
```

**Listing 1.** The three contracts (Java 8+). Note what each lambda is allowed to return — that is the whole difference.

```d2
direction: right
apply: "thenApply\nvalue -> new value" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
compose: "thenCompose\nvalue -> next stage\n(flattened)" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
combine: "thenCombine\nthis + other -> pair" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
cf1: "stage A" {
  width: 140
  height: 50
  style.fill: "#eeeeee"
}
cf2: "stage B" {
  width: 140
  height: 50
  style.fill: "#eeeeee"
}
out: "one result CF" {
  width: 180
  height: 60
  style.fill: "#ffebee"
}
cf1 -> apply -> out
cf1 -> compose -> out
cf1 -> combine -> out
cf2 -> combine
```

**Fig. 1.** `thenApply`/`thenCompose` extend one chain; `thenCombine` is the only one that consumes **two** sources.

## Choosing between them

**Transform synchronously → `thenApply`.** The lambda is a plain function of the completed value (`order -> order.total()`). It runs on normal completion only, possibly inline on the thread that completed the stage.

**Next step is itself asynchronous → `thenCompose`.** Typical shape: `id -> fetchProfileAsync(id)`, where `fetchProfileAsync` already returns a `CompletableFuture`. Composing flattens the chain so the final type is `CompletableFuture<Profile>`; the same lambda under `thenApply` would compile to `CompletableFuture<CompletableFuture<Profile>>` — the classic nested-future smell. Whole pipelines of such steps: [[How would you explain CompletableFuture for composing async work]].

**Two independent results are both needed → `thenCombine`.** Run user lookup and order lookup **concurrently**, then zip: `users.thenCombine(orders, (u, o) -> render(u, o))`. If either source completes exceptionally, the combined stage completes exceptionally and the `BiFunction` never runs.

```java
CompletableFuture<String> page =
    fetchUser(id)                                   // CF<User>
        .thenCompose(u -> fetchOrders(u))           // CF<Orders>, flattened
        .thenCombine(fetchRecommendations(id),      // independent CF<Recs>
                     (orders, recs) -> render(orders, recs))
        .thenApply(Html::escape);                   // sync final touch
```

**Listing 2.** The canonical mix: compose for dependent calls, combine for parallel ones, apply for the local transform.

> [!warning] thenCombine does not start anything
> A popular lie is that `thenCombine` "runs two tasks in parallel". It only **waits** for both stages — you must submit the two tasks yourself (e.g. two `supplyAsync` calls). Calling `a.thenCombine(b, fn)` where `b` has not started yet just registers a dependent on it; nothing new is executed.

> [!example] Where the lambda runs
> Non-async variants may run on the thread that completed the stage. `thenApplyAsync(fn)` switches to `ForkJoinPool.commonPool()` (a new thread per task when its parallelism is below two), and `thenApplyAsync(fn, executor)` uses the executor you pass — the same policy all three methods share. Pool internals: [[What is the Java ForkJoin framework]].

> [!tip] Interview answer
> **`thenApply` maps the value synchronously; `thenCompose` is its flatMap twin for lambdas that already return a `CompletionStage`, sparing you nested futures; `thenCombine` zips two independent stages once both finish normally, feeding both results to a `BiFunction`. None of them start work by themselves, all have `Async` variants with an optional executor, and an upstream exception skips straight past them until a recovery stage like `exceptionally` or `handle`.**
