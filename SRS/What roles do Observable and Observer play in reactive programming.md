<!--
reps: 0
priority: 0
-->
#Paradigms/Reactive #Patterns/GoF/Behavioral/Observer #SRS

# What roles do Observable and Observer play in reactive programming

> [!abstract] Short answer
> Reactive programming reuses the Observer roles over asynchronous streams: the **Observable** is the publisher that owns state and pushes items, the **Observer** is the subscriber that consumes them through callbacks — `onNext` per item, then exactly one `onError` or `onComplete` — and a **Subscription** connects and cancels the two.

## How the GoF roles map onto the stream API

In the classic pattern the publisher calls `update` on each subscriber synchronously; reactive libraries stretch the same shape onto time and failure. The Observable emits zero or more items, each delivered to the observer's `onNext`. Instead of "notify and forget", the stream has a defined end: either `onError` with the failure or `onComplete` with a normal finish — never both. The subscription object replaces the naive listener list entry: it carries cancellation (`dispose` in Reactor, `cancel` in Reactive Streams) and, in `org.reactivestreams`, the backpressure contract, where the observer's side signals demand with `request(n)` so a fast producer cannot drown a slow consumer. This is why the pattern is push-based: state changes flow from the source outward, while the observer never polls the source.

```d2
direction: right
obs: "Observable\nsource of items" { width: 200; height: 80; style.fill: "#e3f2fd" }
onnext: "onNext(item)\n0..n times" { width: 190; height: 80; style.fill: "#fff3e0" }
term: "onError(e) or\nonComplete()\nexactly one" { width: 200; height: 80; style.fill: "#ffebee" }
consumer: "Observer\nconsumes signals" { width: 200; height: 80; style.fill: "#e8f5e9" }
obs -> onnext -> term -> consumer: signal order
```

**Fig. 1.** The observer contract: any number of `onNext` signals, then exactly one terminal signal, error or completion.

## What reactive adds beyond the classic pattern

Three extensions matter in interviews. First, timing: a cold observable starts emitting when subscribed, so a subscriber sees the whole sequence, while a hot one emits regardless — the split is detailed in [[What is the difference between hot and cold Observables]]. Second, failure is a first-class signal rather than an exception thrown into the publisher loop. Third, demand flows upstream: the GoF publisher just fires updates, while a Reactive Streams publisher must respect `request(n)`, which is the practical difference between the pattern and the protocol. The classic half of the pair is described in [[What is Observer]], and the Spring-shaped publisher in [[How does ApplicationContext publish events]].

> [!warning] Three name collisions to keep apart
> `java.util.Observable` is the obsolete GoF-style JDK class, not the reactive one. Reactor's `Mono.just(value)` evaluates its argument at assembly time, so side effects run even with zero subscribers — a favorite trap question. And an Observer in the reactive sense is not a listener registered on a list; it receives a terminal signal, which a plain GoF `update` loop never delivers.

> [!tip] Interview answer
> Reactive programming keeps the Observer roles: the Observable pushes items it owns to the Observer, which consumes them via onNext, then gets exactly one terminal signal — onError or onComplete. Reactive adds what the classic pattern lacks: a subscription that can cancel, backpressure through request(n), and guaranteed completion signals, turning the synchronous notification loop into an asynchronous stream protocol.
