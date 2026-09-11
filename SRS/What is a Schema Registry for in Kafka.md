<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #SRS

# What is a Schema Registry for in Kafka?

> [!abstract] Short answer
> A separate service next to the brokers that stores and validates schemas for topic message data — Avro, JSON Schema, Protobuf — hands out schema IDs, and enforces compatibility rules when schemas evolve. Kafka itself carries only bytes: the Registry is what turns raw payloads into a governed, evolvable contract between producers and consumers ([[What core Kafka APIs exist]]).

## The mechanism: IDs on the wire, schemas at the registry

```d2
direction: right
p: "Producer\nserializer" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
reg: "Schema Registry\nREST: store, validate,\nversion schemas" {
  width: 250
  height: 110
  style.fill: "#e8f5e9"
}
topic: "Kafka topic\nbytes = payload + schema ID" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
c: "Consumer\ndeserializer" {
  width: 200
  height: 80
  style.fill: "#e3f2fd"
}
p -> reg: register schema\nget ID
p -> topic: payload + ID
topic -> c: read
c -> reg: fetch schema by ID\n(cached locally)
```

**Fig. 1.** The payload optimization: messages carry a schema ID instead of the schema, and clients fetch the definition once and cache it — the Registry never sits in the data path.

A producer's serializer takes the application object, registers (or looks up) its schema under a subject, and writes the payload with that schema's ID; a consumer's deserializer reads the ID, retrieves the schema — from its local cache after the first fetch — and reconstructs the object. The Registry exposes this as a REST service for storing, retrieving, and validating schemas, with the client serializers and deserializers plugging into the standard Kafka client configuration ([[What is the Kafka Consumer API for]]). Every schema version gets a unique ID and an incremented version number per subject, and new versions are checked for compatibility with previous ones before being accepted — the registration call is the contract checkpoint ([[What Schema Registry compatibility modes exist]]).

## What it buys, and what it costs

Without a Registry, format evolution is tribal: a renamed field silently becomes null for every consumer written against the old layout. With one, the compatibility policy is enforced centrally — a producer cannot register a breaking schema, so the failure moves from runtime decode errors at 3 a.m. to a rejected registration at build time. It also gives governance a home: subjects mirror topics, versions are auditable, and brokers can even validate that produced data carries a valid schema ID when the broker-side validation feature is on ([[How does Kafka version messages]]). The cost is an operational dependency: the Registry is a stateful service backed by its own Kafka topic, and clients that cannot reach it can still consume with cached schemas but cannot register or resolve new ones ([[What Kafka topic settings matter in practice]]).

> [!warning] The Registry is not part of Apache Kafka
> Kafka the broker knows nothing about schemas — this is a separate product in the Confluent ecosystem with its own deployment, availability, and security story. Interviewers probe exactly this: the Registry adds a contract layer on top of Kafka's byte transport; it does not change broker behavior, and a plain Kafka client that ignores the ID bytes will happily read raw garbage.

> [!tip] Interview answer
> Schema Registry is the contract layer over Kafka's byte-only topics: a REST service storing Avro, JSON Schema, and Protobuf schemas per subject, assigning each version an ID that rides in the payload so clients fetch and cache schemas instead of shipping them. It enforces compatibility checks at registration, which is what makes schema evolution controlled rather than hopeful — and it is a separate service, not a Kafka feature.

