<!--
reps: 0
priority: 0
-->
#API/RPC #API/GRPC #SRS

# What is the difference between RPC and gRPC

> [!abstract] Short answer
> RPC is the general pattern — invoking a remote procedure through a local-looking call, with IDL, stubs, and marshalling. gRPC is a concrete, open-source RPC framework (Google, now CNCF) that implements the pattern over HTTP/2 with Protocol Buffers as IDL and serialization, adding four call kinds, deadlines and cancellation, standardized status codes, and first-class multi-language codegen.

## Pattern versus product — and what the product adds

Classic RPC systems (CORBA, Java RMI, XML-RPC, JSON-RPC) each solved the same puzzle with the transport and serialization of their era; their shared weaknesses were proprietary or awkward transports, weak deadlines/timeouts semantics, and brittle or platform-locked contracts. gRPC's answer, piece by piece: HTTP/2 gives one persistent connection with multiplexed concurrent calls, binary framing, and native streaming (no connection-per-call scaling ceiling); Protocol Buffers give a typed, schema-evolvable contract compiled to any language ([[What is Protocol Buffers and why does gRPC use it]]); deadlines propagate end-to-end and cancel work downstream rather than abandoning it; the status-code model (OK, INVALID_ARGUMENT, NOT_FOUND, UNAVAILABLE...) is standardized across languages; interceptors, TLS, and auth are pluggable but standard. Where Java RMI serialized live Java objects — coupling both ends to the JVM and to class versions — gRPC messages are language-neutral data ([[What is RPC and what are its pitfalls]] — the pattern's pitfalls persist inside the product).

```d2
classic: classic RPC (CORBA, RMI,
XML-RPC, JSON-RPC) {
  c1: transport of its era
(IIOP, JRMP, HTTP/1.1)
  c2: ad-hoc serialization
  c3: weak deadline semantics
  c4: platform-locked contracts
}
g: gRPC {
  g1: HTTP/2 multiplexed streams
  g2: protobuf IDL + wire
  g3: deadlines propagate, cancel
  g4: 17 standard status codes
  g5: 4 call kinds incl streaming
  g6: polyglot codegen
}
pattern: same RPC pattern
(IDL, stubs, marshalling)
classic -> pattern
g -> pattern
```

**Fig. 1.** Both implement the RPC pattern; gRPC's contributions are the transport (HTTP/2), the contract (protobuf), and operational semantics (deadlines, statuses, streaming).

## What stays the same and how to choose

Everything RPC teaches still applies over gRPC: timeouts leave outcomes unknown, retries need idempotence, chatty interfaces die by round-trip, and contract evolution is a discipline ([[What changes are breaking for a REST API]] maps to proto field-number rules). Against minimal JSON-RPC specifically, gRPC trades human-readable payloads and zero-friction curl debugging for typed contracts, streaming, and performance. Choose gRPC for internal, high-volume, polyglot service-to-service calls — especially streaming ones; choose REST-style HTTP for public and browser-facing surfaces; the two coexist behind one gateway ([[What is gRPC and when is it useful]] for the deployment shape; [[What is the difference between REST and gRPC]] for the style-level comparison).

```text
JSON-RPC 2.0 (text RPC):
  {"jsonrpc":"2.0","method":"GetOrder","params":[7],"id":1}
  -> {"jsonrpc":"2.0","result":{...},"id":1}

gRPC (typed RPC):
  proto: service OrderService { rpc GetOrder (OrderId) returns (Order); }
  -> generated stubs, HTTP/2 transport, protobuf wire, grpc-status trailers,
     propagating deadlines, four streaming kinds
```

**Listing 1.** Two implementations of one pattern: minimal JSON text versus typed schema with operational semantics (conceptual).

> [!warning] gRPC is not "RPC but safe"
> The framework fixes the mechanics — transport, typing, deadlines — not the distributed-systems physics: unknown outcomes after timeouts, duplicate deliveries on retry, and version coupling remain your design obligations. Teams that treat gRPC as immunity inherit the pitfalls with better tooling.

> [!tip] Interview answer
> RPC is the pattern — local-looking calls across a network via IDL, stubs, and marshalling; CORBA, RMI, and JSON-RPC were its implementations. gRPC is the modern framework version: HTTP/2 for multiplexing and streaming, protobuf for typed evolvable contracts, propagating deadlines, standard status codes, and polyglot codegen. The pattern's pitfalls survive — idempotent retries and contract evolution are still mine — but the operational semantics finally match production needs.
