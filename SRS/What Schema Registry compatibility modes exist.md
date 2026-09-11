<!--
reps: 0
priority: 0
-->
#Messaging/Tools/Kafka #Serialization #SRS

# What Schema Registry compatibility modes exist?

> [!abstract] Short answer
> Seven: NONE, BACKWARD, BACKWARD_TRANSITIVE, FORWARD, FORWARD_TRANSITIVE, FULL, and FULL_TRANSITIVE. BACKWARD is the default — new consumers can read old data. Each mode defines how far back the check reaches: plain modes compare against the previous version only; TRANSITIVE modes check against all registered versions ([[What is a Schema Registry for in Kafka]]).

## The three directions and their reach

```d2
direction: right
bw: "BACKWARD\nnew consumer reads\nold producer's data" {
  width: 250
  height: 100
  style.fill: "#e8f5e9"
}
fw: "FORWARD\nold consumer reads\nnew producer's data" {
  width: 250
  height: 100
  style.fill: "#e3f2fd"
}
full: "FULL\nboth directions" {
  width: 200
  height: 90
  style.fill: "#f3e5f5"
}
bw -> full
fw -> full
```

**Fig. 1.** Compatibility is directional: backward protects consumers being upgraded, forward protects consumers not yet upgraded, and FULL demands both at every step.

The docs' canonical example: schemas for one subject evolve in order X-2, X-1, X. Under BACKWARD, a consumer using the new schema X can process data written with X or X-1, but not necessarily X-2; BACKWARD_TRANSITIVE guarantees reading X, X-1, and X-2. FORWARD mirrors this: data written with the new schema X is readable by consumers still on X or X-1 — TRANSITIVE extends to all history. FULL means both directions at once. The Registry checks the mode when a new version is registered and rejects breaking changes there, so the mode is a property of the subject, configured per subject, not of the client ([[How does Kafka version messages]]).

```properties
compatibility=BACKWARD              # registry default, per subject
compatibility=BACKWARD_TRANSITIVE   # check against all history
compatibility=FORWARD               # old consumers read new data
compatibility=FORWARD_TRANSITIVE
compatibility=FULL                  # both directions
compatibility=FULL_TRANSITIVE
compatibility=NONE                  # no check at registration
```

**Listing 1.** The subject-level settings; with plain modes only the last version constrains a new one, with TRANSITIVE modes the whole version history does.

## Why BACKWARD is the default for Kafka

The documented reasoning: BACKWARD compatibility lets you rewind consumers to the beginning of the topic and read the whole log with the new schema — old messages stay readable as consumers upgrade, which matches Kafka's replay model. FORWARD is harder in practice because it requires anticipating every future change (in Protobuf you cannot even add new message types under it). Two documented wrinkles are worth knowing: for Protobuf, BACKWARD_TRANSITIVE is the recommended practice because adding new message types is not forward compatible; and Kafka Streams supports only BACKWARD compatibility for its internal deserialization path ([[What is the Kafka Streams API for]]).

> [!warning] Changing the mode does not re-validate history retroactively
> The check runs at registration of each new version against whatever reach the mode then had. A subject that evolved under NONE can later be set to FULL_TRANSITIVE, but nothing re-checks the versions already stored — the first registration after the switch is the first thing that gets tested. Setting a strict mode on a messy history does not clean the history.

> [!tip] Interview answer
> Three directions — BACKWARD, FORWARD, FULL — each with a TRANSITIVE variant, plus NONE, seven modes total, configured per subject and enforced when a new version registers. BACKWARD is the default because old messages must stay readable when consumers upgrade and rewind. Plain modes check only the previous version, TRANSITIVE ones check all history, and Protobuf is best with BACKWARD_TRANSITIVE.

