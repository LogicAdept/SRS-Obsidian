<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# What is the Invalid Message Channel pattern?

> [!abstract] Short answer
> An **Invalid Message Channel** is a separate channel where a **receiver** parks messages it **received but cannot process** — wrong type, missing required header, unparsable body. The original payload moves unchanged to the quarantine channel, and an error handler consumes it there for diagnosis or replay.

## Receiver-side quarantine, not broker plumbing

The receiver — not the broker and not the messaging system — decides that a delivered message "makes no sense" and moves it to the invalid channel. The administrator designing the system defines one or more such channels up front; they stay empty during normal operation, so clutter is not a problem, and an error-handler endpoint can consume them as soon as bad messages appear. Typical triggers: schema evolution broke a payload, a required header such as a correlation id is missing, or a message arrives on a channel whose contract it violates. This pattern pairs with [[What is the Datatype Channel pattern]] (which prevents most type mismatches) and contrasts with broker-side dead-lettering — see [[What is the difference between Invalid Message Channel and Dead Letter Channel]]. In Spring Integration, a filter's `discard-channel` is a direct implementation of the idea, described in [[How does a Spring Integration filter discard-channel implement Invalid Message Channel]].

```d2
direction: down
ok: "Valid messages" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
rcv: "Receiver\nparses + validates" {
  width: 220
  height: 65
  style.fill: "#e3f2fd"
}
imc: "Invalid Message Channel\noriginal payload, unchanged" {
  width: 300
  height: 75
  style.fill: "#ffebee"
}
eh: "Error handler\ninspect, log, replay" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
ok -> rcv: "process"
rcv -> eh: "cannot process:\nmove message"
eh -> imc: "consume from quarantine" {
  style.stroke-dash: 4
}```

**Fig. 1.** The receiver diverts the bad message itself; the error handler watches the quarantine channel, not the main flow.

## What lands on an invalid channel

```text
Trigger                                   Payload kept?
----------------------------------------  -------------
Unparsable body (broken JSON/XML)         yes, raw bytes
Schema v2 event on v1 consumer            yes, as delivered
Missing required header (correlation id)  yes, headers intact
Wrong type on a Datatype Channel          yes, for inspection
```

**Listing 1.** In every case the delivered message — body and headers — is preserved for a human or a replayer to judge, which is exactly why the pattern is a debugging lifeline.

> [!warning] Not the same as a broker DLQ
> A dead letter queue is what the **messaging system** does with a message it **could not deliver**; an Invalid Message Channel is what a **receiver** does with a message it **did deliver but could not process**. Glossaries that list "DLQ / error channel" as synonyms of Invalid Message Channel conflate three different contracts — the divergence is worked out in [[What is the difference between Invalid Message Channel and an error channel]].

> [!tip] Interview answer
> An Invalid Message Channel is a receiver-side quarantine: when an endpoint gets a message it cannot parse, validate, or type-check, it moves the intact message to a dedicated channel instead of crashing or discarding it. An error-handler endpoint consumes that channel to log, diagnose, and optionally replay. The broker never decides — the receiver does, which is what separates this pattern from dead-lettering.
