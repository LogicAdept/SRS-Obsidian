<!--
reps: 0
priority: 0
-->
#Java/Library/Reactor/Mono #Java/Library/Reactor/Flux #SRS

# What is the difference between Project Reactor Mono and Flux?

> [!abstract] Short answer
> **`Flux<T>` is an asynchronous sequence of 0..N items; `Mono<T>` is 0..1.** Both are Reactive Streams `Publisher`s emitting the same three signals — `onNext`, `onComplete`, `onError` — so the choice between them encodes **cardinality** in the method signature, not a different engine.

## One contract, two cardinalities

A `Flux` is the general-purpose type: a stream of items, optionally terminated by completion or error. A `Mono` exists for single-result work: a lookup, an insert, a config value. `Mono<Void>` carries no item at all — only the completion signal, the reactive equivalent of `void`. The pair keeps APIs honest: `findById` returning `Mono<User>` says "at most one user" before any code runs, while `Flux<User>` promises a stream ([[What are data streams in reactive programming]]).

They interoperate because the contract is shared. `flux.next()` takes the first item as a `Mono`; `mono.flux()` widens back to a sequence; combinator operators accept either side.

```java
Flux<String> flux = Flux.just("a", "b", "c");
flux.subscribe(
        v -> System.out.println("next: " + v),
        e -> {},
        () -> System.out.println("flux complete"));
// next: a / next: b / next: c / flux complete

Mono<String> mono = Mono.just("one");
mono.subscribe(v -> System.out.println("mono next: " + v),
               e -> {},
               () -> System.out.println("mono complete"));
// mono next: one / mono complete

Mono.<String>empty().subscribe(v -> {},
        e -> {},
        () -> System.out.println("empty complete"));
// empty complete — completion with no item

flux.next().subscribe(v -> System.out.println("next() saw: " + v));
// next() saw: a — first item of the Flux as a Mono
```

**Listing 1.** Verified on Reactor Core 3.6: same signals for both types; `Mono` is 0..1, `Flux` 0..N; `next()` narrows a `Flux` to its first item.

## Where the split shows up in real APIs

Reactive repositories return `Mono<User>` for `findById` and `Flux<User>` for `findAll`. `Mono<Void>` marks fire-and-forget writes whose only outcome is "done" or an error. Collection-returning reactive APIs force a decision: `Mono<List<T>>` materializes everything into one delivery, `Flux<T>` streams items as they arrive — different latency and memory profile for the same data.

> [!warning] A `Mono` is not a nullable and not a hidden `List`
> A completed-empty `Mono` is a legitimate "no result", but calling `null` through operators still errors — `map` receiving `null` fails the sequence rather than producing an empty `Mono`. And wrapping a big collection in `Mono<List<T>>` does not make it streaming: the consumer gets nothing until the whole list exists. Choose `Flux<T>` when items can be delivered as they are produced ([[What operators exist in Project Reactor and what are they for]], [[What is the difference between Project Reactor and WebFlux]]).

```d2
direction: down
flux: "Flux<T>  0..N" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
sig1: "onNext ... onNext   (0 or more)" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
term: "onComplete | onError   (exactly one terminal)" {
  width: 340
  height: 60
  style.fill: "#fff3e0"
}
mono: "Mono<T>  0..1" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
sig2: "onNext (0 or 1)  ->  same terminal" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
flux -> sig1 -> term
mono -> sig2 -> term
```

**Fig. 1.** Both publishers emit `onNext` signals and exactly one terminal signal; they differ only in how many `onNext` are allowed.

> [!tip] Interview answer
> **Both are Reactive Streams publishers with the same onNext/onComplete/onError contract; `Flux` allows 0..N items, `Mono` allows 0..1.** `Mono<Void>` is the completion-only case. The types are freely convertible — `next()`, `flux()`, `from()` — so the choice is documentation: pick `Mono` for single results and `Flux` for streams, and remember `Mono<List<T>>` is a batch, not a stream.

> [!example] Verified behavior
> Reactor Core 3.6: `Flux.just("a","b","c")` delivered three `onNext` then complete; `Mono.just("one")` delivered one; `Mono.empty()` delivered complete only; `flux.next()` delivered only `"a"` as a `Mono`.
