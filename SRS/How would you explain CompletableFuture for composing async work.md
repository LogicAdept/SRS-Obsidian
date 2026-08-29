<!--
reps: 0
priority: 0
-->
#Java/Async #Java/Concurrency/Executors #SRS

# How would you explain CompletableFuture for composing async work?

> [!abstract] Short answer
> A **`CompletableFuture`** is a **`Future` you can complete** and a **`CompletionStage`**: dependents run **when this stage completes**. Chain **`thenApply`** (map a value), **`thenCompose`** (flatten a function that returns another stage), **`thenCombine`** (wait for **two** stages). `*Async` without an executor uses **`ForkJoinPool.commonPool()`** (or a new `Thread` if parallelism is below two). Non-async dependents may run on the **completing** thread. Apply vs compose vs combine: [[How would you explain CompletableFuture thenApply vs thenCompose vs thenCombine]]. Async vs threads: [[How does multithreading differ from parallelism and async work]].

## Stages, not `Thread` objects

`supplyAsync(supplier)` completes with the supplier’s value on the common pool; `supplyAsync(supplier, executor)` uses that executor. `runAsync` is the `Runnable` form (`Void`).

**`thenApply(fn)`:** when this stage completes **normally**, run `fn` on the result; the new stage holds `fn`’s value. **`thenCompose(fn)`:** `fn` returns a **`CompletionStage`**; the composed stage completes with **that** stage’s value (no nested future). **`thenCombine(other, fn)`:** when **this and other** both complete normally, `fn` gets **both** results. Either-side: `applyToEither` / `acceptEither`. Both then ignore values: `runAfterBoth`.

Exceptional completion skips normal `then*` dependents. Use **`exceptionally`**, **`handle`**, or **`whenComplete`**. `get` wraps in `ExecutionException`; **`join`** throws **`CompletionException`**. `cancel` is **exceptional** completion (`CancellationException`), not `FutureTask`-style task control.

`allOf` / `anyOf` combine many stages. `copy()` / `minimalCompletionStage()` hide completion APIs from clients. What the type is: [[What is CompletableFuture]].

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class ComposeAsync {
    public static void main(String[] args) {
        ExecutorService exec = Executors.newVirtualThreadPerTaskExecutor();
        CompletableFuture<Integer> n =
                CompletableFuture.supplyAsync(() -> 2, exec)
                        .thenApply(x -> x + 1)
                        .thenCompose(x -> CompletableFuture.supplyAsync(() -> x * 10, exec));
        CompletableFuture<Integer> m = CompletableFuture.supplyAsync(() -> 5, exec);
        int sum = n.thenCombine(m, Integer::sum).join();
        exec.close();
        System.out.println(sum);
    }
}
```

**Listing 1.** Map (`thenApply`), flatten (`thenCompose`), then join two pipelines (`thenCombine`). `join` waits; the work is not three named `Thread`s you `start`.

```d2
direction: down
s: "supplyAsync" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
ap: "thenApply — T → U" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
co: "thenCompose — T → Stage<U>" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
cb: "thenCombine — (T,U) → V" {
  width: 240
  height: 40
  style.fill: "#e8f5e9"
}
s -> ap -> co
s -> cb
```

**Fig. 1.** Compose along one pipeline or wait for two stages. `*Async` picks the pool; plain `thenApply` may run on whoever completed the previous stage.

> [!warning] `thenApply(x -> otherFuture)` nests a `CompletableFuture`
> You wanted **`thenCompose`**. `thenApply` of a stage gives `CompletableFuture<CompletableFuture<T>>`.

> [!warning] Default `*Async` is the common pool
> CPU-heavy work there starves parallel streams and other CF tasks. Pass an **`Executor`** for I/O.

> [!tip] Interview answer
> I start with `supplyAsync`, then `thenApply` to transform a value, `thenCompose` when the next step returns another future, and `thenCombine` when I need two results. I pass an executor for I/O and use `handle` when the chain can fail.
