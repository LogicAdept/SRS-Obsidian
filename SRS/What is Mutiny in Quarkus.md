<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is Mutiny in Quarkus?

> [!abstract] Short answer
> Mutiny is Quarkus' reactive programming library — an **event-driven** API built around two types: **`Uni`** (emits 0 or 1 event: an item or a failure) and **`Multi`** (emits 0..n items, then a failure or completion). Pipelines are declared as chains of operators and are **lazy**: nothing executes until something subscribes. Quarkus standardizes on Mutiny across its reactive surface — Quarkus REST, reactive SQL clients, REST client, gRPC stubs and Reactive Messaging all speak `Uni`/`Multi`.

## The event model

With Mutiny you react to events: `onItem()`, `onFailure()`, `onSubscription()`, `onOverflow()`. A `Uni` models an asynchronous action with at most one result (an HTTP call, a row lookup); a `Multi` models a stream, potentially unbounded (Kafka messages, tick events). Both are lazy and subscription-driven: wiring operators builds a graph, and subscribing triggers execution — the "define actions, process on subscribe" model ([[How does Quarkus decide which thread runs your code]]). Errors are first-class events in the chain: `onFailure().recoverWithItem(...)`, `recoverWithUni(...)`, retry policies — no try/catch plumbing through callbacks.

Compared with `CompletableFuture`, Mutiny gives cancellation, back-pressure on `Multi`, event grouping instead of nested `thenCompose` chains, and non-blocking-first operators. Compared with Reactor (`Mono`/`Flux`), the roles match — `Uni`≈`Mono`, `Multi`≈`Flux` — but the API is organized around events rather than around `Flux` composition; Quarkus integrates both worlds but documents and tests Mutiny natively.

```java
// Standalone demo: java -cp mutiny-3.3.0.jar MutinyDemo.java (JDK 21.0.12, Mutiny 3.3.0)
import io.smallrye.mutiny.Multi;
import io.smallrye.mutiny.Uni;

public class MutinyDemo {
    public static void main(String[] args) {
        Uni<String> uni = Uni.createFrom().item("payload");
        String v = uni
                .onItem().transform(String::toUpperCase)
                .await().indefinitely();
        System.out.println("uni result: " + v);

        Multi<Integer> multi = Multi.createFrom().items(1, 2, 3, 4)
                .filter(i -> i % 2 == 0)
                .map(i -> i * 10);
        multi.subscribe().with(i -> System.out.println("onItem: " + i),
                f -> System.out.println("onFailure: " + f));

        Uni<Object> failed = Uni.createFrom().failure(new IllegalStateException("boom"))
                .onFailure().recoverWithItem(-1L);
        System.out.println("recovered: " + failed.await().indefinitely());
    }
}
// Output (verbatim):
// uni result: PAYLOAD
// onItem: 20
// onItem: 40
// recovered: -1
```

**Listing 1.** Declaration then subscription: the `Multi` emitted only after `subscribe().with(...)`, the filter kept 2 and 4, and the failed `Uni` was recovered into `-1` by an `onFailure` branch — errors flow as events through the same chain.

```d2
direction: down
src: "Source\nUni / Multi" {
  width: 220
  height: 55
  style.fill: "#e3f2fd"
}
op1: "onItem().transform(...)\nonFailure().recoverWithItem(...)\nonOverflow().drop()" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
sub: "subscribe()\nnothing ran before this" {
  width: 250
  height: 55
  style.fill: "#e8f5e9"
}
ev: "events: item(s), failure,\ncompletion, subscription" {
  width: 300
  height: 55
}
src -> op1: "operators wired lazily"
op1 -> sub: "graph built"
sub -> ev: "events flow"
```

**Fig. 1.** The pipeline is a declarative graph; execution time is subscription time. That is what "lazy" means in a Mutiny interview answer.

## Where you meet it in Quarkus

Endpoint methods return `Uni`/`Multi` for non-blocking dispatch; REST client methods return `Uni<Response>`; Hibernate Reactive and the reactive SQL clients return `Uni` rows or `Multi` streams; Reactive Messaging pipelines are `Multi` under the hood ([[How does reactive messaging work in Quarkus]]). Inside CDI beans on the event loop you must stay non-blocking: `await().indefinitely()` blocks the calling thread and is only for tests or imperative boundaries ([[How does Quarkus unify imperative and reactive programming]]).

> [!warning] Lazy means "never ran", not "runs immediately"
> A built but unsubscribed pipeline performs zero work — a common production bug is constructing a `Uni` chain and dropping it without subscribing or returning it to the framework, then wondering why the database call never happened. The mirrored trap: `await()` blocks, so calling it inside an event-loop context stalls every connection on that loop. And `Multi` without back-pressure handling (`onOverflow`) can drop or fail under load — say "I handle overflow explicitly" in an interview.

> [!tip] Interview answer
> Mutiny is the reactive library Quarkus standardizes on: event-driven, with Uni for 0..1 results and Multi for streams of 0..n. Everything is lazy — you declare a chain of operators like onItem, onFailure, onOverflow, and it executes only on subscription; failures are events recovered inside the chain. Quarkus REST, the reactive clients, gRPC stubs and Reactive Messaging all speak Uni and Multi, so one event model covers the whole reactive surface.
