<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is snapshotting in event sourcing?

> [!abstract] Short answer
> Snapshotting is an optimization for event-sourced aggregates: instead of replaying every event from the beginning of the stream to rebuild current state, you periodically store a serialized image of the aggregate's state, and on the next load you read the latest snapshot and replay only the events that came after it. The event stream remains the source of truth - a snapshot is cache, not history, and can be deleted or regenerated from the stream at any time.

## Mechanism

Rehydration without snapshots is O(stream length): an aggregate with thousands of events replays all of them on every load, and both time and memory grow with history. With snapshots the flow becomes: append events; every N events (or on a size/time threshold) write a snapshot tagged with the stream position it covers; on load, fetch the newest snapshot, deserialize it, then replay the events after that position. The rule of thumb: snapshot at intervals - every N events, or on a size or time threshold - balancing the storage cost of snapshots against the time saved during rehydration. Snapshots are an optimization, not a replacement for the event stream: the stream stays the source of truth, and a corrupt snapshot is simply rebuilt from it.

```d2
direction: down
stream: "Event stream (source of truth)" {
  width: 320
  height: 55
  style.fill: "#e3f2fd"
}
snap: "Latest snapshot @ seq 1000" {
  width: 300
  height: 55
  style.fill: "#fff3e0"
}
tail: "Replay events 1001..now" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
state: "Current aggregate state" {
  width: 300
  height: 55
}
stream -> snap: "load last image"
snap -> tail
tail -> state
```

**Fig. 1.** The snapshot replaces the prefix of the replay; the tail - events after the snapshot position - is still replayed to reach current state.

## What belongs in the snapshot and what does not

A snapshot is the aggregate's state, not its identity crisis: it typically stores field values plus the sequence number it covers, in a format owned by the same code that owns the events. Because it is derived data, you can change its format, drop all snapshots, and rebuild them by replaying - which is exactly why the stream, not the snapshot, holds the truth. Snapshots pair naturally with projections: a read model is a query-side materialization ([[What is a projection in CQRS and event sourcing]]), while a snapshot serves the write-side aggregate itself. Consistency rule: write the snapshot in the same transaction (or immediately after) the events it covers, and stamp it with the exact stream position, or a load can silently skip events.

> [!warning] "Snapshots make event sourcing unnecessary" and other lies
> No - without the stream, snapshots cannot be trusted: they are single images with no audit trail and no way to answer "how did we get here". The second trap: snapshotting too eagerly. If aggregates are short-lived or streams stay short, snapshots add writes, versioning, and a second serialization format for zero replay savings. And a stale snapshot that was written after later events (position mismatch) can corrupt state on load - the position check is mandatory, not optional hygiene ([[How would you explain the event sourcing pattern]]).

> [!tip] Interview answer
> Snapshotting stores a serialized image of the aggregate every N events so rehydration loads the image and replays only the tail instead of the whole stream. It is a pure optimization: the event stream stays the source of truth, snapshots are regenerable derived data, and I stamp them with the stream position they cover. I add them when streams or load paths actually get long, not by default.
