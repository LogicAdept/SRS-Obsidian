<!--
reps: 0
priority: 0
-->
#Java/Library/Reactor #SRS

# What is the difference between hot and cold Observables?

> [!abstract] Short answer
> **Cold publishers run the pipeline anew for each subscriber — nothing happens before subscription. Hot publishers emit on their own schedule — a subscriber joining late sees only the items emitted after it subscribed.** "Observable" is the RxJava name; Reactor's publishers are `Flux`/`Mono`, but the hot/cold split is the same.

## Cold: one run per subscriber

A cold `Flux` built from `just`, `fromIterable`, `range`, or a deferred HTTP call is a *recipe*: each `subscribe()` executes the whole chain from the start, so two subscribers get two independent runs — including two network calls. If nobody subscribes, nothing executes at all. This is the default for almost everything in Reactor ([[What are data streams in reactive programming]]).

`Mono.just(x)` is the famous nuance: the value is captured **at assembly time**, so it is shared by every later subscriber — technically a replay of one captured item. `defer(() -> ...)` pushes that work to subscription time, restoring true per-subscriber behavior.

## Hot: the stream moves with or without you

A hot publisher does not depend on subscriber count: it may start publishing right away and continues regardless of who is listening. Late subscribers see only what arrives after they joined. Reactor makes hot sources with `Sinks` (programmatic emission), or by converting a cold source with `share()` or `replay()` — the `ConnectableFlux` family, where `connect()`/`autoConnect()` starts the flow and `replay()` additionally keeps history for latecomers ([[What roles do Observable and Observer play in reactive programming]]).

```java
// Cold: every subscriber triggers its own full run
Flux<String> cold = Flux.fromIterable(List.of("blue", "green", "orange", "purple"))
        .map(String::toUpperCase);
cold.subscribe(d -> System.out.println("Subscriber 1: " + d));
cold.subscribe(d -> System.out.println("Subscriber 2: " + d));
// both subscribers see all four colors, each in its own run

// Hot: Sinks feed, subscribers see only what comes after they joined
Sinks.Many<String> hotSource = Sinks.unsafe().many().multicast().directBestEffort();
Flux<String> hotFlux = hotSource.asFlux().map(String::toUpperCase);
hotFlux.subscribe(d -> System.out.println("Sub1 to hot: " + d));
hotSource.emitNext("blue", Sinks.EmitFailureHandler.FAIL_FAST);
hotFlux.subscribe(d -> System.out.println("Sub2 to hot: " + d));
hotSource.emitNext("orange", Sinks.EmitFailureHandler.FAIL_FAST);
// Sub1: BLUE, ORANGE   — Sub2: only ORANGE ("blue" happened before it subscribed)
```

**Listing 1.** Verified on Reactor Core 3.6: cold runs per subscriber; the late hot subscriber missed `blue`.

> [!warning] "Nothing happens before you subscribe" is a cold-publisher rule
> Treating it as universal is the classic interview trap: a hot source — a market feed, sensor stream, or a `Sinks` in a long-running service — is emitting whether or not anyone subscribed, and a subscriber that arrives later cannot rewind. The replay exception: `replay()` retains history, `share()` does not. Also `Mono.just(value)` already holds its captured value at assembly time — side effects in the argument happen even with zero subscribers ([[What is Observer]]).

```d2
direction: down
cold: "Cold Flux" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
s1: "subscribe() -> own run" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
s2: "subscribe() -> another run" {
  width: 250
  height: 55
  style.fill: "#e8f5e9"
}
hot: "Hot source (Sinks)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
early: "early subscriber\nsees blue, orange..." {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
late: "late subscriber\nsees only new items" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
cold -> s1
cold -> s2
hot -> early
hot -> late
```

**Fig. 1.** Cold fans out into independent runs; hot is one shared flow where the entry point decides what you see.

> [!tip] Interview answer
> **Cold publishers are recipes — each subscription runs the pipeline from scratch and nothing executes until one arrives; hot publishers emit regardless of subscribers, so late joiners only see new items.** Reactor is cold by default; hot comes from `Sinks`, `share()`, or `replay()` (which also retains history). Watch the `Mono.just` nuance — its value is captured at assembly time, and `defer` restores per-subscription laziness.

> [!example] Verified behavior
> Reactor Core 3.6: two cold subscribers each received all four colors; against a hot Sinks source, the first subscriber received `BLUE` and `ORANGE` while the second — subscribed after `blue` was emitted — received only `ORANGE`.
