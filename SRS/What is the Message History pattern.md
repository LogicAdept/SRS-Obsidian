<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages #SRS

# What is the Message History pattern?

> [!abstract] Short answer
> **Message History** attaches to each message a **list of the components it has passed through** — originator first, every processing step appending an entry — turning loose coupling's "we never know where a message was" into recorded lineage stored in the header.

## Debugging lineage in a system designed to forget

Loose coupling is an architectural strength: senders and recipients make no assumptions about each other, messages are self-contained. It is also a debugging nightmare: nobody can say which path a message took, so impact analysis ("who consumes this format?") and problem correction ("who published this?") become guesswork. The history pattern makes the journey part of the message: every component that processes it — including the originator — appends one entry to the history list, which lives in the **header** because it is system control information, not application data. Aggregators complicate the picture: one output message summarizes many inputs, each with its own history — either grow the history into a hierarchical tree preserving all branches, or keep a flat list carrying only the dominant input's path. The history pairs naturally with the audit copy taken by a [[What is the Wire Tap pattern]] and with persistence in a [[What is the Message Store pattern]]; an [[What is the Envelope Wrapper pattern]] is often the component that carries the header safely across systems.

```d2
direction: down
s: "Originator\nhistory: [originator]" {
  width: 240
  height: 65
  style.fill: "#e3f2fd"
}
f1: "Filter A\n+ [router-a]" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
f2: "Translator B\n+ [translator-b]" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
r: "Receiver\nreads full path" {
  width: 190
  height: 60
  style.fill: "#e8f5e9"
}
s -> f1 -> f2 -> r```

**Fig. 1.** Each hop appends one entry; the arriving message carries its own resume.

## Where the entries live

```text
Header: msg-history:
  1. originator: orders-api          (component, timestamp)
  2. router:      orders-cbr
  3. transformer: crm-to-canonical
  4. channel:     canonical.customers
```

**Listing 1.** Component identity plus timestamp per hop is enough for impact analysis; anything richer belongs in the store, not the header.

> [!warning] History headers grow, leak, and lie when tampered
> Long flows make history headers a measurable fraction of the message; hop data can expose internal topology to receivers who should not see it (strip or truncate at trust boundaries); and nothing forces components to append honestly — a history you rely on for security decisions needs integrity protection, or at least the caveat that it is diagnostic data, not proof.

> [!tip] Interview answer
> Message History keeps a running list — in the header — of every component a message has passed through, each hop appending an entry. It restores debuggability and impact analysis to loosely coupled systems at the cost of header growth and topology exposure; aggregated messages either build a tree of histories or keep the dominant branch. Treat it as diagnostic metadata, not tamper-proof evidence.
