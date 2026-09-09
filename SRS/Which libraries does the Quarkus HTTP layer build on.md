<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# Which libraries does the Quarkus HTTP layer build on?

> [!abstract] Short answer
> The default Quarkus HTTP stack is **Eclipse Vert.x on top of Netty**, packaged through the `quarkus-vertx-http` core extension: Netty provides the async IO and the event loops, Vert.x (`vertx-core`, `vertx-web`) the routing and server model, and Quarkus REST, reactive routes, websockets and the Dev UI all sit on that layer. It is **not** Tomcat, Jetty or Undertow — a servlet stack (Undertow) exists only as an opt-in extension for traditional WAR-style applications.

## The layering, with evidence from a built app

Netty owns the transport: non-blocking sockets, byte buffers, the event loop groups whose threads show up in responses as `vert.x-eventloop-thread-N`. Vert.x wraps it into a server with routing, request/response abstractions and context handling. `quarkus-vertx-http` integrates that into Quarkus — config (`quarkus.http.*`), the route registry, TLS registry, Dev UI pages — and Quarkus REST (formerly RESTEasy Reactive) dispatches Jakarta REST endpoints onto the same event loops ([[How does Quarkus decide which thread runs your code]]). A fast-jar build of a plain REST application proves the stack by inspection: its `lib/` directory contains `io.netty.netty-codec-http-4.1.137.Final.jar`, `io.vertx.vertx-core-4.5.33.jar`, `io.vertx.vertx-web-4.5.33.jar`, `io.quarkus.quarkus-vertx-http-3.39.2.jar` and `resteasy-reactive-vertx-3.39.2.jar` — and no Undertow or Tomcat jar at all.

The interview point behind the layering: HTTP handling is asynchronous end to end by default, so a small number of event loop threads serves many connections — but code that blocks must be dispatched to the worker pool, which is exactly what the `@Blocking` machinery exists for ([[What is Mutiny in Quarkus]]).

```java
// No user HTTP server code exists - Quarkus starts Vert.x/Netty during recorded boot.
// The stack is visible in the packaged artifact and in thread names (JDK 21, Quarkus 3.39.2).
//
// $ ls target/quarkus-app/lib/main | grep -iE 'netty-http|vertx-core|vertx-web|undertow'
// io.netty.netty-codec-http-4.1.137.Final.jar     <- Netty transport + HTTP codec
// io.vertx.vertx-core-4.5.33.jar                  <- Vert.x core
// io.vertx.vertx-web-4.5.33.jar                   <- Vert.x routing
// io.quarkus.quarkus-vertx-http-3.39.2.jar        <- Quarkus integration layer
// (no undertow / tomcat / jetty jar - servlet stack is opt-in, not default)
//
// GET /mixed/eventloop returned "eventloop on: vert.x-eventloop-thread-0":
// the responding thread IS a Netty/Vert.x event loop thread.
```

**Listing 1.** Library inspection of the fast-jar plus a live response. The absence of Undertow/Tomcat jars and the presence of `vert.x-eventloop-thread-0` in application output identify the stack without reading any config.

```d2
direction: down
netty: "Netty 4.1.x\nasync IO, event loops, HTTP codecs" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
vertx: "Vert.x 4.5 (vertx-core, vertx-web)\nserver, routing, contexts" {
  width: 320
  height: 65
  style.fill: "#e3f2fd"
}
qvh: "quarkus-vertx-http\nconfig, routes registry, TLS, Dev UI" {
  width: 320
  height: 65
  style.fill: "#fff3e0"
}
rest: "Quarkus REST (RESTEasy Reactive),\nreactive routes, websockets, gRPC" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
app: "Your endpoints" {
  width: 200
  height: 45
}
netty -> vertx -> qvh -> rest -> app
```

**Fig. 1.** Each layer delegates IO downward: your endpoint code runs on a thread owned by Netty, scheduled through Vert.x, wired by Quarkus extensions ([[What are the bootstrapping phases of a Quarkus application]]).

## When the answer changes

Add the Undertow servlet extension and the story changes deliberately: servlet, `web.xml` and servlet-filter based applications get a traditional blocking container, at the cost of the reactive dispatch model. That is a migration path for Jakarta EE-style apps, not the default. Also version-precise: Quarkus 3.x tracks Vert.x 4.5.x and Netty 4.1.x — naming specific majors signals you have actually looked at the dependency tree.

> [!warning] "Quarkus is a servlet framework" — the classic mix-up
> The default stack has no servlets in it: Jakarta REST endpoints are dispatched as callback methods on Vert.x event loops, not through a servlet container. Consequences interviewers check: `HttpServletRequest` is unavailable by default, Servlet API filters do not exist, and threading rules follow the event-loop/worker model rather than the servlet spec. Quoting "it is like Spring Boot, just faster" loses the thread-model question immediately.

> [!tip] Interview answer
> Quarkus HTTP is Vert.x on Netty — Netty provides the async transport and event loops, Vert.x the server and routing, and quarkus-vertx-http integrates it; Quarkus REST, reactive routes, websockets and the Dev UI run on top. You can verify it in a built fast-jar: netty and vertx jars in lib, no Tomcat or Undertow unless you deliberately add the servlet stack. So HTTP is asynchronous by default, with worker threads only for blocking endpoints.
