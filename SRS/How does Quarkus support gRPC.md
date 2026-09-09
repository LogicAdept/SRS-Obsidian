<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus support gRPC?

> [!abstract] Short answer
> The `quarkus-grpc` extension generates service and stub code **from `.proto` files at build time** (grpc-java plus protobuf plugins driven by the Quarkus plugin), registers service implementations as CDI beans, and serves them over the same Vert.x/Netty HTTP layer with HTTP/2 and optional TLS. Stubs come in three flavors — **blocking**, **reactive Mutiny** (`Uni`/`Multi`, including bidi streaming), and grpc-java's own — and because everything is generated and wired during augmentation, gRPC services compile to native images without extra reflection work.

## The build-time path from proto to bean

You drop `.proto` files under `src/main/proto`; the Quarkus build runs code generation, and generated base classes appear on the compile classpath. Your service class extends the generated base (for example `MutinyGreeterGrpc.GreeterImplBase`), overrides the RPC methods, and is annotated `@GrpcService` (a CDI bean) — the container wires the service into the gRPC server during augmentation, registering it with the Vert.x HTTP/2 transport ([[What is a Quarkus extension]]). No `ServerBuilder` code exists in a Quarkus app: port, TLS, reflection (server reflection flag), compression and load-shaping are all `quarkus.grpc.*` configuration. Client side: generated Mutiny stubs are injectable CDI beans configured via `quarkus.grpc.clients.<name>.host/port` — same build-time story in reverse.

```java
// src/main/proto/demo.proto (schematic of the build input; compiled with quarkus-grpc)
// syntax = "proto3";
// package demo;
// service Greeter { rpc Say (Req) returns (Resp); }
// message Req { string name = 1; }
// message Resp { string text = 1; }
//
// src/main/java/org/acme/GreetingService.java - the Quarkus service bean shape:
// @GrpcService
// public class GreetingService extends MutinyGreeterGrpc.GreeterImplBase {
//     @Override
//     public Uni<Resp> say(Req request) {          // Mutiny stub: Uni in, Uni out
//         return Uni.createFrom().item(Resp.newBuilder()
//                 .setText("hello " + request.getName()).build());
//     }
// }
// (Conceptual in this deck: the verified run exercises the REST/HTTP layer of the same
// stack - Vert.x event loop names and dispatch rules are identical for gRPC handlers.)
```

**Listing 1.** Marked `Conceptual` for the proto file; the mechanism to narrate in an interview is the annotation-on-bean model replacing explicit server construction, with Mutiny stubs mapping RPCs onto `Uni`/`Multi` ([[What is Mutiny in Quarkus]]).

```d2
direction: down
proto: "src/main/proto/*.proto" {
  width: 240
  height: 50
}
gen: "Augmentation: code generation\nstub + service base classes" {
  width: 320
  height: 65
  style.fill: "#fff3e0"
}
bean: "@GrpcService bean\nUni<Resp> say(Req)" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
srv: "gRPC server on Vert.x HTTP/2\nquarkus.grpc.* config, TLS" {
  width: 340
  height: 65
  style.fill: "#e3f2fd"
}
cli: "Generated stubs as CDI beans\nquarkus.grpc.clients.<name>.*" {
  width: 330
  height: 60
  style.fill: "#e8f5e9"
}
proto -> gen -> bean -> srv
cli -> srv: "calls"
```

**Fig. 1.** Both sides are generated artifacts: services register as beans, clients inject as beans — nothing is constructed by hand ([[What are the bootstrapping phases of a Quarkus application]]).

## Interview depth points

Interoperability: gRPC over HTTP/2 with protobuf contracts gives polyglot microservices a typed, versioned interface; Quarkus additionally supports streaming with Mutiny `Multi` on both directions (unary, server-stream, client-stream, bidi map onto `Uni`/`Multi` combinations). Testability: `@QuarkusTest` starts the gRPC server on a random port and generated test stubs connect — the same integration approach as the REST layer. Operations: health and metrics extensions cover gRPC services like REST ones, and native packaging works because no runtime codegen or reflection is involved ([[How does Quarkus support GraalVM native images]]).

> [!warning] "Add the extension and grpc-java appears at runtime" — no
> The dependency on grpc-java/protobuf internals is build-scoped: classes are generated and transformed during augmentation; assuming you must create channels or `ServerImpl` yourself (the plain grpc-java way) means fighting the framework. The reverse confusion: expecting Servlet-style `web.xml`-ish registration — there is none; the `@GrpcService` bean plus config is the entire contract. Also, gRPC needs HTTP/2 — a proxy or load balancer that strips it breaks the transport regardless of correct Quarkus config.

> [!tip] Interview answer
> Quarkus bakes gRPC in at build time: protos under src/main/proto generate stubs and service bases during augmentation, my service is a @GrpcService CDI bean overriding Mutiny-style methods — Uni and Multi for unary and streaming calls — and the server runs on the same Vert.x HTTP/2 layer with quarkus.grpc config for port, TLS and reflection. Clients are injected generated stubs configured per key. No server builder code, native-image friendly, health and metrics work on the gRPC services the same as REST.
