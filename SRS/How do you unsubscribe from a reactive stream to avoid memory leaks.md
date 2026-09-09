<!--
reps: 0
priority: 0
-->
#Java/Library/Reactor #SRS

# How do you unsubscribe from a reactive stream to avoid memory leaks?

> [!abstract] Short answer
> **Keep the `Disposable` returned by `subscribe()` and call `dispose()` when the stream is no longer needed.** Disposal is Reactor's cancellation: the source is told to stop producing and release resources. Infinite or hot sources — `Flux.interval`, schedulers, Sinks — leak if nobody ever disposes.

## What dispose actually does

Every lambda variant of `subscribe()` returns a `Disposable`. Calling `dispose()` sends the **cancel** signal upstream: the source should stop emitting and clean up. It is a request, not a synchronous stop — a source that is mid-emission may complete before it honors the cancel ([[What is the role of a Subscription in reactive programming]]).

`doFinally` observes how the stream ended, which makes disposal visible in tests: after a dispose it reports the **cancel** signal. The `Disposable.isDisposed()` flag flips once cancellation is processed.

```java
Disposable controlled = Flux.interval(Duration.ofMillis(50))
        .doFinally(sig -> System.out.println("terminated with: " + sig))
        .subscribe(i -> {});
// ...later, e.g. when the UI screen closes
controlled.dispose();
// prints: terminated with: cancel
```

**Listing 1.** Store the `Disposable` from `subscribe()` and dispose on teardown; `doFinally` reports `cancel`.

With `BaseSubscriber` instead of lambdas, the equivalent handle is the subscriber itself: `cancel()` sends the same signal ([[What is backpressure in reactive programming]]).

## Many subscriptions at once

Two utilities in `Disposables` cover the common lifecycle patterns. `Disposables.swap()` is an atomically replaceable slot — dispose the current stream and put a new one in its place, which is the "user clicked again" pattern. `Disposables.composite()` collects many `Disposable` instances so a teardown path can dispose all of them in one call; after the composite itself is disposed, every later `add` is disposed immediately.

```java
Disposable.Composite scope = Disposables.composite();
Disposable d1 = Flux.interval(Duration.ofMillis(50)).subscribe(i -> {});
Disposable d2 = Flux.interval(Duration.ofMillis(50)).subscribe(i -> {});
scope.add(d1);
scope.add(d2);
scope.dispose();
System.out.println("both disposed: " + (d1.isDisposed() && d2.isDisposed()));
// both disposed: true
```

**Listing 2.** A composite scope cancels all in-flight streams in one call.

> [!warning] The leak is the never-disposed infinite source
> A finite stream (`Flux.just`, a bounded `Flux.range`) ends by itself and cannot leak. The classic leak is a long-lived source — `Flux.interval`, a hot Sinks feed, a persistent connection — subscribed from a short-lived component and never disposed: the pipeline keeps running and pinning memory for the lifetime of the JVM. And `dispose()` is **not guaranteed to take effect instantly**: a fast source may still push a few more signals before it stops.

```d2
direction: right
sub: "subscribe()" {
  width: 170
  height: 60
  style.fill: "#e3f2fd"
}
run: "stream running\ndemand -> onNext" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}
disp: "dispose()\n(cancel signal)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
stop: "source stops\nresources released\ndoFinally: cancel" {
  width: 250
  height: 90
  style.fill: "#ffebee"
}
sub -> run
run -> disp: "no longer needed"
disp -> stop
```

**Fig. 1.** Disposal sends cancel upstream; the source stops producing and cleans up — eventually, not atomically.

> [!tip] Interview answer
> **`subscribe()` returns a `Disposable`; store it and call `dispose()` when the owner's lifecycle ends.** Dispose cancels the subscription, so the source stops and releases resources — visible in `doFinally` as cancel. For many streams use `Disposables.composite()`, for replace-on-click `swap()`. Leaks come from infinite sources — timers, hot feeds — that nobody ever disposes.

> [!example] Verified behavior
> An `Flux.interval` stream left subscribed keeps ticking; a twin stream disposed after ~140 ms stops, `isDisposed()` is `true`, and `doFinally` printed `terminated with: cancel`. A composite disposed two interval streams with one call.
