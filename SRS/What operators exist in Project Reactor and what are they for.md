<!--
reps: 0
priority: 0
-->
#Java/Library/Reactor #SRS

# What operators exist in Project Reactor and what are they for?

> [!abstract] Short answer
> **Reactor's operators fall into a handful of working groups: creation, transformation, filtering, combination, error handling, threading, backpressure shaping, and terminal consumption.** Learning the groups beats memorizing names — the Reactor reference has an appendix that routes "I need to do X" to the operator.

## The working groups

**Creation** builds a publisher: `Flux.just`, `fromIterable`, `fromStream`, `range`, `generate`/`create` for programmatic feeding, `Mono.fromCallable` to wrap blocking one-shots. **Transformation** changes items: `map` for a synchronous 1-to-1 step, `flatMap` for an async step that fans out to 1..N inner publishers. **Filtering** trims: `filter`, `take`, `distinct`, `limitRate`. **Combination** merges streams: `zip` pairs elements by position, `merge` interleaves as they come, `concat` waits for one source to finish before the next. **Error handling** recovers: `onErrorResume`, `onErrorReturn`, `retry`, `timeout`. **Threading** moves execution: `subscribeOn` picks where subscription runs, `publishOn` where downstream signals run — via `Schedulers`. **Backpressure** operators reshape demand (`limitRate`, `onBackpressureBuffer/Drop/Latest/Error`). **Terminals** pull the trigger: `subscribe`, `block`, `collectList`, `toIterable` ([[What is backpressure in reactive programming]], [[What is the difference between Project Reactor Mono and Flux]]).

```java
// creation + transform + filter
Flux.range(1, 6)
    .map(i -> i * 10)
    .filter(i -> i != 30)
    .subscribe(v -> System.out.print(v + " "));
// 10 20 40 50 60

// zip pairs elements by position
Flux.zip(Flux.just("a", "b", "c"), Flux.just(1, 2, 3))
    .subscribe(t -> System.out.print(t.getT1() + t.getT2() + " "));
// a1 b2 c3

// flatMap fans out: one input can produce several outputs, asynchronously
Flux.just("x", "y")
    .flatMap(s -> Flux.just(s + "1", s + "2"))
    .subscribe(s -> System.out.print(s + " "));
// x1 x2 y1 y2

// recovery: a failed item switches to a fallback publisher
Flux.just(1, 0, 3)
    .map(i -> 10 / i)
    .onErrorResume(e -> Mono.just(-1))
    .subscribe(v -> System.out.print(v + " "),
               e -> {},
               () -> System.out.println("| done"));
// 10 -1 | done  (the error skipped 0's division result and 3)
```

**Listing 1.** Verified on Reactor Core 3.6: one operator per group — map/filter, zip, flatMap, onErrorResume.

## Nothing runs until a terminal operator subscribes

Assembling a chain only builds an execution plan; the machinery starts at `subscribe()`. `block()`, `blockFirst()`, `blockLast()`, `collectList()` and `toIterable()` are also subscriptions — with the twist that they request **unbounded** demand and block the calling thread ([[What is backpressure in reactive programming]]).

> [!warning] flatMap does not preserve order, and block is banned on event loops
> `flatMap` subscribes to inner publishers eagerly, so results interleave in *completion* order — when order matters use `concatMap`. `block()` on a WebFlux/Netty event-loop thread stalls the loop that serves all requests on it; it is for tests and adapters, never inside a reactive pipeline. And `map` that throws kills the whole sequence — put recovery (`onErrorResume`) downstream of the risky step ([[What are the disadvantages of using reactive streams with WebFlux]], [[What is the Java Stream API]]).

```d2
direction: right
src: "Source\njust / range / fromCallable" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
mid: "Intermediate operators\nmap / flatMap / filter / zip\nonErrorResume / publishOn / limitRate" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
term: "Terminal\nsubscribe / block / collectList" {
  width: 270
  height: 80
  style.fill: "#e8f5e9"
}
src -> mid -> term
```

**Fig. 1.** The chain is a plan: a source, any number of intermediate operators, exactly one subscription that starts it.

> [!tip] Interview answer
> **Group the operators, don't memorize them: creation (`just`, `fromIterable`, `create`), transformation (`map` 1-to-1, `flatMap` async fan-out), filtering, combination (`zip`/`merge`/`concat`), error handling (`onErrorResume`, `retry`), threading (`subscribeOn`/`publishOn`), backpressure (`limitRate`, `onBackpressure*`), and terminals (`subscribe`, `block`, `collectList`).** Nothing runs before subscription; `flatMap` is unordered, `concatMap` preserves order, and `block` never belongs on an event loop.

> [!example] Verified behavior
> Reactor Core 3.6: `range(1,6).map(*10).filter(!=30)` printed `10 20 40 50 60`; `zip` paired `a1 b2 c3`; `flatMap` produced `x1 x2 y1 y2`; `map(10/i)` on `1,0,3` with `onErrorResume` printed `10 -1` and completed.
