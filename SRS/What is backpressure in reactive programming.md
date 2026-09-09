<!--
reps: 0
priority: 0
-->
#Java/Library/Reactor #SRS

# What is backpressure in reactive programming?

> [!abstract] Short answer
> **Backpressure is the consumer telling the producer how much it can accept right now, via `Subscription.request(n)`.** It is built into the Reactive Streams contract: nothing flows upstream of a request. Demand is a running sum capped at `Long.MAX_VALUE` — which is the "unbounded, produce as fast as you can" value.

## Demand drives emission

The protocol: `onSubscribe` hands the subscriber a `Subscription`; the subscriber calls `request(n)`; the publisher emits **at most** n items, and more only after further requests. The pressure is propagated backward operator by operator — each operator forwards its downstream demand upstream ([[What is the role of a Subscription in reactive programming]]).

The catch: the common ways of subscribing immediately request unbounded. `subscribe()` and most lambda variants, `block()`, `blockFirst()`, `blockLast()`, and iterating `toIterable()`/`toStream()` all trigger a `Long.MAX_VALUE` request. To subscribe with bounded demand you override `BaseSubscriber.hookOnSubscribe` and call `request(...)` yourself.

```java
Flux.range(1, 10)
    .subscribe(new BaseSubscriber<Integer>() {
        @Override
        protected void hookOnSubscribe(Subscription s) { request(2); }
        @Override
        protected void hookOnNext(Integer value) {
            System.out.println("got " + value);
            if (value == 2) cancel(); // demand exhausted, stop the source
        }
        @Override
        protected void hookOnCancel() { System.out.println("cancelled"); }
    });
// got 1 / got 2 / cancelled — the source never emits 3..10
```

**Listing 1.** A `BaseSubscriber` that requests two items and cancels: the source stops at 2.

## Reshaping demand

Operators sit between source and consumer to adapt two mismatched rates. `limitRate(k)` splits a large downstream request into upstream batches of k. When the source can push faster than the consumer accepts, an overflow strategy decides the fate of surplus items: `onBackpressureBuffer` queues them until demand arrives, `onBackpressureDrop` discards them, `onBackpressureLatest` keeps only the newest value, and `onBackpressureError` fails the sequence with an overflow error. `Flux.create`/`FluxSink.OverflowStrategy` expose the same choices for programmatically fed sources.

```java
// limitRate: upstream sees batches of 3, downstream still gets 1..8 in order
Flux.range(1, 8)
    .doOnRequest(r -> System.out.println("upstream request: " + r))
    .limitRate(3)
    .subscribe();
// upstream request: 3 (repeated until 8 delivered)

// DROP: with demand 1, items 2..5 are discarded
Flux.<Integer>create(e -> { for (int i = 1; i <= 5; i++) e.next(i); e.complete(); },
                     FluxSink.OverflowStrategy.DROP)
    .subscribe(new BaseSubscriber<Integer>() {
        protected void hookOnSubscribe(Subscription s) { request(1); }
        protected void hookOnNext(Integer v) { System.out.println("drop saw: " + v); }
    });
// drop saw: 1

// LATEST: burst with zero demand, one request -> only item 5 is delivered
BaseSubscriber<Integer> latestSub = new BaseSubscriber<Integer>() {
    protected void hookOnSubscribe(Subscription s) { } // zero demand during burst
    protected void hookOnNext(Integer v) { System.out.println("latest saw: " + v); }
};
Flux.<Integer>create(e -> { for (int i = 1; i <= 5; i++) e.next(i); e.complete(); },
                     FluxSink.OverflowStrategy.LATEST)
    .subscribe(latestSub);
latestSub.request(1); // after the burst: delivers the retained item 5
// latest saw: 5
```

**Listing 2.** Verified on Reactor Core 3.6: `limitRate` batches, DROP keeps the first item, LATEST keeps the newest.

> [!warning] Default subscribe means no backpressure at all
> The plain `subscribe(v -> ...)` you write in every demo requests **unbounded** — backpressure is silently disabled and a slow consumer of a hot source will accumulate everything. Overflow is also not one fixed behavior: buffer, drop, latest, and error are *chosen per operator*, and pushing into a best-effort Sinks with zero demand reports `FAIL_OVERFLOW` (or throws under `FAIL_FAST`) rather than magically queuing. "Reactive handles overload for me" is true only if the pipeline says what to drop ([[How does Spring WebFlux handle backpressure]], [[How do you protect a slower downstream service from overload]]).

```d2
direction: right
down: "Slow consumer\nrequest(n)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
op: "Operator reshapes demand\nlimitRate / onBackpressure*" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
up: "Fast source\nemits at most n" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
down -> op: "request(n)"
op -> up: "request(batch)"
up -> op: "onNext <= batch"
op -> down: "onNext <= n"
```

**Fig. 1.** Demand flows upstream, data flows downstream; the middle operator is the valve where overflow is decided.

> [!tip] Interview answer
> **Backpressure is the consumer's `request(n)` propagated upstream — the producer never outpaces the granted demand.** The sum of outstanding requests is the demand, capped at `Long.MAX_VALUE` for unbounded. Regular `subscribe()` requests unbounded, so real control comes from `BaseSubscriber`, `limitRate`, or overflow operators — buffer, drop, latest, error. That is what makes a fast producer meet a slow consumer without drowning it.

> [!example] Verified behavior
> With Reactor Core 3.6: `request(2)` + `cancel()` stopped `Flux.range(1,10)` after two items; `limitRate(3)` made upstream log batches of 3; DROP with demand 1 delivered only item 1; LATEST after a zero-demand burst delivered only item 5.
