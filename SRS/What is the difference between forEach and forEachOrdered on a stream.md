<!--
reps: 0
priority: 0
-->
#Java/Streams/Operations/Terminal #Java/Versions/8 #SRS

# What is the difference between `forEach` and `forEachOrdered` on a stream?

> [!abstract] Short answer
> **Both are eager terminals that run a `Consumer` on each element and consume the stream.** `forEach` is **explicitly nondeterministic** on **parallel** pipelines: no encounter-order promise; any thread, any time; you synchronize shared state. `forEachOrdered` walks **one at a time in encounter order** if the stream has one, with happens-before between actions — still any thread per element. Sequential `forEach` is not the method JavaDoc calls unordered. Neither is `collect`. Side effects here are **not** elided (unlike `peek` / `count`).

## Same terminal, different order contract

`Stream.forEach(Consumer)` “performs an action for each element.” Terminal. On **parallel** pipelines it **does not guarantee** encounter order — that would sacrifice parallelism. The action may run at whatever time, on whatever thread the library chooses. If it touches shared state, **you** synchronize ([[How would you explain parallel streams in Java]], [[What terminal stream operations do you know in Java]]).

`Stream.forEachOrdered(Consumer)` performs the action for each element **in the stream’s encounter order if one exists**. It processes elements **one at a time** in that order. Action *N* happens-before action *N+1*. The thread for a given element is still the library’s choice.

Package doc lists `forEach()` among terminals that **may ignore** encounter order. `List` / array sources are ordered; `HashSet` is not — then `forEachOrdered` has no encounter order to keep ([[What is the Java Stream API]]).

Both take a **non-interfering** action. They start the pipeline; afterward the stream is consumed. Stream JavaDoc: behavioral-parameter side effects may be skipped **except** where specified — **`forEach` and `forEachOrdered` are the exceptions** (along with the `count()` API note for the opposite case). `peek` is intermediate and **may** be skipped ([[What is the peek method on stacks queues or streams in Java]], [[How do you print 10 random numbers using forEach]]).

Do not `forEach(list::add)` — that is the mutable-reduction anti-pattern; use `collect` ([[What is the collect terminal operation in Java streams]]).

```d2
direction: down
fe: "forEach (parallel)\nany order, any thread" {
  width: 280
  height: 55
  style.fill: "#fff8e1"
}
feo: "forEachOrdered\nencounter order, one-at-a-time\n(happens-before)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Parallel `forEach` may scramble encounter order. `forEachOrdered` keeps it when the stream is ordered.

```java
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

class Demo {
    static List<Integer> scramble(List<Integer> nums) {
        List<Integer> seen = new CopyOnWriteArrayList<>();
        nums.parallelStream().forEach(seen::add);
        return seen; // order need not match nums
    }

    static void printInOrder(List<Integer> nums) {
        nums.parallelStream().forEachOrdered(System.out::println);
    }
}
```

**Listing 1.** `forEach` on `parallelStream()` is allowed to ignore list order. `forEachOrdered` prints in encounter order. `CopyOnWriteArrayList` only makes the add thread-safe — it does not restore order.

> [!warning] `forEachOrdered` is still a side-effect sink, and “any thread” remains
> Happens-before does not mean “the caller’s thread.” Shared mutation still needs a thread-safe structure or, better, `collect`. On a sequential ordered stream, `forEach` vs `forEachOrdered` is rarely the interesting distinction — the interview trap is **parallel**. `Iterable.forEach` is a different method on the collection, not a stream terminal.

> [!tip] Interview answer
> **`forEach` = terminal per-element action; parallel ⇒ no encounter-order guarantee.** **`forEachOrdered` = same, but one-at-a-time in encounter order when the stream has one.** Use `forEachOrdered` to print an ordered parallel stream. Use `collect` to build a list.
