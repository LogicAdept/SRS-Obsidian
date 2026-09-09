<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus unify imperative and reactive programming?

> [!abstract] Short answer
> Quarkus builds everything HTTP- and messaging-facing on a **common Vert.x layer**, so one service can host **both styles**: an endpoint returns a plain type and runs on a **worker thread**, or returns a Mutiny `Uni`/`Multi` and runs on the **event loop** — chosen per method, overridable with `@Blocking` / `@NonBlocking`. The reactive core never goes away underneath; "unify" means the two models interoperate in one stack with one threading model, not that blocking code becomes non-blocking for free.

## The threading rules

Quarkus REST (formerly RESTEasy Reactive, renamed in Quarkus **3.9**; artifact `quarkus-rest`) dispatches each Jakarta REST method by its shape: methods returning **plain/blocking types** run on a worker thread; methods returning **`Uni`/`Multi`** without `@Blocking` run on the event loop and must not block it. The defaults shift for integrated stacks — where JDBC and Hibernate are involved, the framework assumes blocking unless told otherwise. Annotating the `Application` subclass sets a global default.

```java
import io.smallrye.common.annotation.Blocking;
import io.smallrye.mutiny.Uni;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@Path("/mixed")
public class MixedEndpoints {

    @GET
    @Path("/blocking")
    @Blocking
    public String blockingEndpoint() {
        return "runs on a worker thread";
    }

    @GET
    @Path("/eventloop")
    public Uni<String> eventLoopEndpoint() {
        return Uni.createFrom().item("never blocks the loop");
    }
}
```

**Listing 1.** Both styles in one resource (compiled on Quarkus 3.39.2, JDK 21). `@Blocking` forces the worker pool even though the second method returns `Uni`; without it, `Uni` dispatches to the event loop.

```d2
direction: down
req: "HTTP request" {
  width: 170
  height: 50
  style.fill: "#e3f2fd"
}
disp: "Quarkus REST dispatcher\nreads return type + @Blocking" {
  width: 280
  height: 75
  style.fill: "#fff3e0"
}
loop: "Event loop\nUni / Multi, no blocking allowed" {
  width: 290
  height: 75
  style.fill: "#e8f5e9"
}
work: "Worker thread pool\n@Blocking, JDBC, Hibernate" {
  width: 290
  height: 75
  style.fill: "#ffebee"
}
resp: "Response" {
  width: 150
  height: 45
  style.fill: "#e3f2fd"
}
req -> disp
disp -> loop
disp -> work
loop -> resp
work -> resp
```

**Fig. 1.** One dispatcher, two execution contexts. The worker pool is the escape hatch for code that cannot be non-blocking; the event loop is the low-overhead path for reactive pipelines.

## Mutiny in one paragraph

Mutiny is Quarkus' reactive API: **`Uni`** emits one event — an item or a failure (the 0..1 case, like a single async response); **`Multi`** emits n items, then completion or failure (streams, possibly unbounded). You compose with events (`onItem()`, `onFailure()`) instead of `CompletableFuture` gymnastics, and the rest of the stack speaks it: the reactive REST client, reactive datasources and Reactive Messaging expose or consume `Uni`/`Multi`. The shape maps onto familiar reactive concepts — [[What is the difference between Project Reactor Mono and Flux|Reactor Mono and Flux]] are the Spring-world counterparts, and the same caution applies about which context runs your code ([[What are the disadvantages of using reactive streams with WebFlux]]).

> [!warning] The event loop is shared and unforgiving
> A single blocked event loop stalls **all** requests currently multiplexed on it — CPU-bound work or a synchronous JDBC call on the loop is the classic outage. Conversely, `@Blocking` on everything throws away the latency advantages. Debug the dispatch model by asking "what context executes this method" first, and remember thread-local state (e.g. request-scoped data) does not automatically follow a `Uni` across async boundaries.

> [!tip] Interview answer
> Quarkus runs one Vert.x-based core: Quarkus REST dispatches each endpoint by its shape — plain return types and @Blocking methods go to worker threads, Uni/Multi endpoints run on the event loop. Mutiny models the reactive side: Uni is 0..1, Multi is 0..n, and integrations like the REST client speak it. So imperative and reactive coexist in one service with one dispatcher — the point is interoperation, not free non-blocking magic, and blocking the event loop remains the failure mode to respect.
