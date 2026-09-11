<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Serialization #SRS

# How does Kafka version messages?

> [!abstract] Short answer
> Kafka stores opaque bytes, so versioning is a producer/consumer contract: the payload carries an identifier of its schema version — a schema ID resolved through a Registry, or an explicit version field in the envelope — and compatibility rules decide which evolutions are legal. Consumers then branch on version and decode accordingly ([[What is a Schema Registry for in Kafka]]).

## Where the version lives

```d2
direction: right
msg: "Record value\n(bytes)" {
  width: 210
  height: 80
  style.fill: "#e3f2fd"
}
id: "Schema ID prefix\nregistry-resolved" {
  width: 230
  height: 90
  style.fill: "#e8f5e9"
}
env: "Envelope field\nversion = 3" {
  width: 230
  height: 90
  style.fill: "#fff3e0"
}
branch: "Consumer logic\nselects decoder\nper version" {
  width: 250
  height: 100
  style.fill: "#f3e5f5"
}
msg -> id
msg -> env
id -> branch
env -> branch
```

**Fig. 1.** Two documented placement strategies: a schema ID prefix that the deserializer resolves transparently, or an explicit version field inside an envelope that application code switches on.

The Registry path is the standard one: each schema version registered under a subject receives a unique ID, serializers write the payload with that ID, and deserializers fetch and cache the matching schema — the wire carries an identifier instead of the definition, which keeps payloads small and version resolution automatic ([[What is a Schema Registry for in Kafka]]). The envelope path puts versioning inside the data: a wrapping structure with a version field, with per-version decoding logic in consumers; it needs no extra service but makes the branching your code's job. In both cases the broker stays ignorant of versions — a version change is just different bytes in the same partition log, which is why old messages retain their old version until retention removes them ([[How does Kafka process messages]]).

## Evolution is governed by compatibility, not by the version number

The version field is bookkeeping; the actual safety property is compatibility between consecutive (or all) schema versions — which fields may be added or dropped with defaults, which type widenings are allowed. That policy is enforced when a new schema version is registered: a breaking schema is rejected before any producer can emit it, which turns evolution from a deploy-time gamble into a gate ([[What Schema Registry compatibility modes exist]]). In practice versions advance per subject alongside topics: consumers must be able to read every version that can still be in the log — including versions written before their restart, which is exactly the rewind scenario the BACKWARD default protects ([[How do you replay Kafka messages from an older offset]]). Records that remove a key entirely are tombstones: a deletion event with a null value that compacted topics keep until the retention window passes ([[What is a Kafka tombstone record]]).

> [!warning] A version number alone guarantees nothing
> Bumping `version: 2` in an envelope breaks nothing by itself — and fixes nothing either. If the new layout is incompatible and consumers still hold old schemas for the log's lifetime, the failure is a decode error at read time, not at write time. Versioning without a compatibility gate just documents the breakage in advance.

> [!tip] Interview answer
> Since Kafka only transports bytes, message versioning means embedding schema identity in the payload — a Registry-assigned schema ID or an envelope version field — and gating evolution with compatibility rules enforced at schema registration. Consumers read whatever versions can exist in the log, branching or deserializing accordingly, and deletions are null-valued tombstones. The registry is the contract layer; the broker stays byte-blind.

