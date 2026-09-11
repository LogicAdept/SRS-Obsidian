<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the Message Sequence pattern?

> [!abstract] Short answer
> A **Message Sequence** transmits an arbitrarily large data set by splitting it into **message-size chunks**, each marked with three identification fields — sequence identifier, position, and size or end indicator — so the receiver can reassemble or process them in order.

## Three fields make chunks a whole

Whenever a large body may not fit in a single message — a big document, a bulk reply — the data is sent as a sequence: every chunk carries a **sequence identifier** distinguishing this cluster from others, a **position identifier** ordering chunks within it, and a **size or end indicator** saying how many chunks to expect or which one is last. The receiver buffers chunks and reconstructs the whole (or feeds them, in order, to processing). The pattern is the data-plane twin of the [[What is the Splitter pattern]], which produces such sequences from one composite message, and it feeds the [[What is the Resequencer pattern]], which repairs arrival order; both rely on the same fields. Size limits that force sequencing are everywhere: broker max message size (RabbitMQ default policy limits, Kafka `message.max.bytes`), memory of thin clients, or protocol caps like the 16 MB MongoDB document limit.

```d2
direction: down
src: "Huge dataset\n(1000 rows)" {
  width: 200
  height: 65
  style.fill: "#e3f2fd"
}
c1: "seq=7 pos=1 size=1000" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
c2: "seq=7 pos=2 size=1000" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
c3: "seq=7 pos=1000 size=1000\nend indicator" {
  width: 250
  height: 65
  style.fill: "#fff3e0"
}
rx: "Receiver reassembles\nwhen complete" {
  width: 240
  height: 65
  style.fill: "#e8f5e9"
}
src -> c1
src -> c2
src -> c3
c1 -> rx
c2 -> rx
c3 -> rx```

**Fig. 1.** Chunk headers identify the cluster, the position, and the expected total — reassembly becomes a bookkeeping problem.

## Chunk headers in practice

```text
headers:
  seq-id:      7f3c...      # unique per sequence (uuid)
  seq-pos:     2            # 1-based position
  seq-size:    1000         # or seq-end: true on the last chunk
body:  <one row / one piece of the payload>
```

**Listing 1.** Prefer an explicit size over a bare end marker when the receiver needs progress or completeness checks; the end indicator alone cannot distinguish "last chunk" from "chunks still missing".

> [!warning] A sequence is only as reliable as its reassembly policy
> Chunks arrive out of order, some never arrive (TTL, dead-lettering), and duplicates occur under at-least-once delivery. A receiver that reassembles without a timeout on incomplete sequences leaks memory per abandoned sequence, and one that processes positionally without dedup will double-apply duplicate chunks.

> [!tip] Interview answer
> Message Sequence splits oversized data into chunks, each carrying a sequence id, its position, and the total size or an end marker, so the receiver can reassemble or process in order. It exists because brokers cap message sizes and big payloads need chunking anyway. The hard part is not splitting but completion: reassembly needs timeouts, dedup, and a plan for chunks that never arrive.
