<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# How does Spring WebFlux handle backpressure?

> [!abstract] Short answer
> WebFlux is a **Reactive Streams** stack: the **subscriber `request(n)`s** demand so a fast publisher cannot flood a slow consumer **without blocking**. Reactor implements that for `Mono`/`Flux`. If a source **cannot slow down**, it must **buffer, drop, or fail** — WebFlux does not magically cap every hot producer.

## Subscriber demand, not thread blocking

Spring WebFlux *Overview*: in imperative code, **blocking waits** are natural backpressure. Non-blocking code needs an explicit rate signal. **Reactive Streams** (also Java 9 `Flow`) lets the subscriber control how fast the publisher produces. Example: a repository `Publisher` feeds an HTTP server `Subscriber` that writes the response.

Reactor is WebFlux’s library: operators honor non-blocking backpressure. Demand is `request(n)`; `Long.MAX_VALUE` means unbounded (“as fast as you can”).

Writing a `Flux` to the HTTP response (SSE, NDJSON, streaming JSON) is that subscriber: as the socket/codec consumes bytes, demand flows back — Reactor Netty’s HTTP engine is **backpressure-ready**. That is TCP/HTTP flow control **coupled to** Reactive Streams, not a second ad-hoc protocol.

```d2
direction: right
pub: "Publisher\n(Flux / repository)" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
sub: "Subscriber\n(HTTP write / codec)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
req: "request(n)" {
  width: 140
  height: 50
  style.fill: "#fff3e0"
}

sub -> pub: "request(n)"
pub -> sub: "onNext"
```

**Fig. 1.** Backpressure is demand from the subscriber, not `Thread.sleep`. SSE streams: [[How do you implement Server-Sent Events in WebFlux]].

## When the publisher cannot slow down

Spring: Reactive Streams only **defines the mechanism**. A source that ignores demand still must **buffer, drop, or fail**.

Reactor operators (tune at the boundary of a hot source):

| Operator | Role |
| --- | --- |
| `onBackpressureBuffer(maxSize)` | Park up to N; overflow strategy or error |
| `onBackpressureDrop` | Discard extras |
| `onBackpressureLatest` | Keep only the newest item |
| `onBackpressureError` | Fail with overflow |
| `limitRate(N)` | Split downstream demand into smaller upstream batches |
| `limitRequest(N)` | Cap **total** demand, then complete |

```java
Flux<Tick> ticks = market.ticks() // hot, cannot pause the exchange
        .onBackpressureBuffer(256)
        .limitRate(32);

@GetMapping(path = "/ticks", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<Tick> stream() {
    return ticks;
}
```

**Listing 1.** Conceptual: bounded buffer + `limitRate` so a 10k/s source does not unbounded-queue toward a 100/s consumer. Blocking JDBC on the loop is a different failure — [[Why should you not use JDBC on the WebFlux event loop]].

> [!warning] Backpressure is not automatic for every `Flux`
> `Flux.interval`, `Flux.create` without a strategy, or a generator that ignores demand can still OOM. Operators must sit **between** the hot source and the slow sink.

> [!warning] `onBackpressureBuffer()` without a size is unbounded
> Unbounded parking is still a memory bomb. Prefer a `maxSize` and an overflow strategy.

> [!warning] `request(Long.MAX_VALUE)` disables the signal
> Some subscribers request unbounded demand. Then only your buffer/drop/error operators protect memory.

> [!tip] Interview answer
> **WebFlux uses Reactive Streams: the HTTP write (subscriber) `request`s more as it can send.** Reactor operators carry that demand. If a producer cannot slow down, you buffer, drop, or fail — Spring says so explicitly. `limitRate` batches demand; `onBackpressureBuffer`/`Drop`/`Latest` handle overflow.
