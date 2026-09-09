<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus decide which thread runs your code?

> [!abstract] Short answer
> Quarkus REST runs on two thread kinds: **event-loop (IO) threads** that perform all IO asynchronously, and a pooled **worker thread** pool for blocking work. Dispatch is decided by the endpoint signature: a method returning `Uni`, `Multi`, `CompletionStage`, a Reactive Streams `Publisher` (or a Kotlin suspend function) is considered non-blocking and runs on the event loop; a method returning a plain type runs on a worker thread. `@Blocking` and `@NonBlocking` override the guess at method, class or `Application` level.

## The dispatch decision

The event loop reads request bytes and writes responses; it must never be blocked, because every other connection multiplexes over the same small set of threads. Since blocking code cannot be statically detected, Quarkus uses the return type as a best guess: reactive types signal "I will complete later, do not hold a thread", plain types signal "run me on a worker and hand the result back". The explicit `@Blocking` annotation (from `io.smallrye.common.annotation`) forces a worker even for a method returning `Uni` — the classic case is a reactive signature that internally calls JDBC ([[Which libraries does the Quarkus HTTP layer build on]]).

The same model extends beyond REST: reactive routes, the gRPC server and messaging run on event loops by default, and CDI methods called from them inherit that thread until something switches pools ([[How does Quarkus unify imperative and reactive programming]]).

```java
// src/main/java/org/acme/check/MixedEndpoints.java (JDK 21, Quarkus 3.39.2, mvn test green)
package org.acme.check;

import io.smallrye.common.annotation.Blocking;
import io.smallrye.mutiny.Uni;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;

@Path("/mixed")
public class MixedEndpoints {

    @GET                              // returns Uni -> dispatched on the IO thread
    @Path("/eventloop")
    public Uni<String> eventLoopEndpoint() {
        return Uni.createFrom().item("eventloop on: " + Thread.currentThread().getName());
    }

    @GET                              // returns String -> dispatched to a worker thread
    @Path("/blocking")
    public String blockingEndpoint() {
        return "blocking on: " + Thread.currentThread().getName();
    }

    @GET                              // Uni return type but @Blocking -> worker anyway
    @Blocking
    @Path("/forced")
    public Uni<String> forcedWorker() {
        return Uni.createFrom().item("forced on: " + Thread.currentThread().getName());
    }
}
// Requests (verbatim, quarkus:run, prod profile):
// GET /mixed/eventloop -> eventloop on: vert.x-eventloop-thread-0
// GET /mixed/blocking  -> blocking on:  executor-thread-1
// GET /mixed/forced    -> forced on:    executor-thread-1
```

**Listing 1.** Three endpoints, three dispatch outcomes — the Vert.x event loop thread and executor worker names are visible in the responses. The `@Blocking` case matters in real code: a `Uni` signature for API consistency, worker execution because the body calls a blocking driver.

```d2
direction: down
req: "HTTP request" {
  width: 200
  height: 45
}
decide: "Quarkus REST dispatch\nby method signature" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
io: "Event loop (IO) threads\nUni / Multi / CompletionStage /\nPublisher / @NonBlocking" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
worker: "Worker thread pool\nplain return types,\n@Blocking" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
resp: "Response written back\non the event loop" {
  width: 260
  height: 50
}
req -> decide
decide -> io
decide -> worker: "@Blocking overrides"
io -> resp
worker -> resp
```

**Fig. 1.** Whatever thread produced the result, the bytes go back out on the event loop — the worker only computes the value.

## Where this bites

JDBC, JPA/Hibernate, filesystem IO and `synchronized`-heavy code are blocking. Calling them from an event-loop context (a reactive endpoint, a Mutiny operator chain, an `@Incoming` method) stalls every connection on that loop. The fixes: mark the endpoint `@Blocking`, move the work into a bean method dispatched to a worker, or switch to the reactive client stack ([[What is Hibernate Reactive in Quarkus]]). The reverse mistake exists too: wrapping a blocking call in `Uni` does not make it non-blocking — the call still executes wherever the chain started.

> [!warning] A Uni wrapper is not an amulet
> The popular lie is "I return `Uni` now, so my endpoint is reactive". Dispatch reads the signature, but the body still runs where it started: `Uni.createFrom().item(jdbcCall())` executes `jdbcCall()` on the event loop and only *wraps* its result. With `@Blocking` absent and a blocking body, you have built an endpoint that starves the IO thread under load — the exact scenario interviewers describe with "server froze at 50 concurrent requests".

> [!tip] Interview answer
> Quarkus separates IO threads from a worker pool and dispatches endpoint methods by signature: returning Uni, Multi, CompletionStage or Publisher means the event loop; returning a plain value means a worker; @Blocking and @NonBlocking override the guess. The trap to name out loud: wrapping a JDBC call in Uni does not unblock it — the body still runs on the event loop unless you mark @Blocking, so blocking work belongs on workers or on the reactive driver stack.
