<!--
reps: 0
priority: 0
-->
#API/GRPC #SRS

# What is Protocol Buffers and why does gRPC use it

> [!abstract] Short answer
> Protocol Buffers (protobuf) is Google's language-neutral interface-definition and serialization format: you declare messages in a .proto schema, codegen produces typed classes for your languages, and the wire format is compact binary — field numbers plus wire types, not field names. gRPC builds on it because it supplies both halves in one artifact: the typed IDL for contracts and the fast, schema-evolvable wire encoding.

## The schema and the wire

A .proto file declares messages (typed fields: scalars, enums, nested messages, repeated, maps, oneof), services (the rpc methods — [[What are the four kinds of gRPC RPCs]]), and options; protoc generates Java, Go, Python, and more. On the wire each field is a tag — field number shifted plus wire type — followed by the value; varints encode integers compactly; strings/bytes/submessages are length-delimited. The demo below hand-rolls a small message per those rules: 38 bytes against 69 for the equivalent JSON. Field numbers are the compatibility mechanism: the wire never carries names, so renaming a field is free, adding a field with a new number is non-breaking (old readers skip unknown tags), and reusing or renumbering a number corrupts — hence the rule: never change a field number, reserve numbers of deleted fields. That is what "schema evolution" means concretely: old binaries read new messages and vice versa ([[What is the difference between RPC and gRPC]] for where this sits in the stack).

```text
binary wire bytes  : 38
json utf8 bytes    : 69
ratio              : 1.82x
parsed back id     : 123456789
```

**Listing 1.** Verified on JDK 21 with protobuf-java 4.33: the same Customer encoded per protobuf wire rules (varint id, length-delimited email and tags) and parsed back sequentially — tag, wire type, length, value (out/A15_Protobuf.txt).

```d2
p: .proto contract
p.msg: message Customer {
  m1: int64 id = 1
  m2: string email = 2
  m3: repeated string tags = 3
}
wire: wire format {
  w1: tag = field_number << 3 | wire_type
  w2: varint (id)
  w3: length-delimited (email, tags)
}
gen: protoc -> typed classes
(Java, Go, ...)
p.msg -> wire
p -> gen
ev: evolution: add new numbers,
never renumber, reserve removed
wire -> ev: unknown tags skipped
by old readers
```

**Fig. 1.** The schema drives codegen and wire encoding; field numbers — not names — are the contract that evolution rules protect.

## The trade-offs against JSON

Wins: size and parse speed (binary tags, no field-name repetition), typed codegen as the shared contract (gRPC's main reason), explicit evolution semantics. Costs: binary is not human-readable — debugging needs grpcurl/protoc decoding and reflection enabled; no browser-native support without shims; schema governance becomes mandatory (a .proto registry, review discipline for field numbers — the same governance REST applies to documented shapes, [[What changes are breaking for a REST API]]); and dynamic or schemaless consumers prefer JSON's flexibility ([[What is content negotiation in REST APIs]] — the JSON ecosystem's negotiation story is why REST stayed textual). proto2 versus proto3 matters at the edges: proto3 removed required and made scalar presence implicit (zero equals absent) until "optional" returned in 3.15 — presence semantics are a classic interview probe ([[What is the difference between RPC and gRPC]] context).

> [!warning] Field numbers are forever
> Renumbering or reusing a field number silently reinterprets old data — string fields decode as garbage, not errors. Delete a field: reserve its number (and name) forever; add a field: new number. Teams that skipped reserving have shipped corruption that only surfaces with old data.

> [!tip] Interview answer
> Protocol Buffers is a schema-first IDL and binary serialization: messages declared in .proto, codegen to typed classes, and a compact wire of field-number tags with wire types — varints and length-delimited values. gRPC uses it because one artifact gives both the typed contract and a fast wire that evolves safely: new fields with new numbers are non-breaking, old readers skip unknown tags, and numbers are never reused. It costs human readability and schema governance, which JSON trades away.
