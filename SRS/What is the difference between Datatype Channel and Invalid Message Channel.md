<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #Messaging #SRS

# What is the difference between Datatype Channel and Invalid Message Channel

> [!abstract] Short answer
> Datatype Channel is the **preventive** contract: every message on a channel has one type, so receivers know how to process it. Invalid Message Channel is the **corrective** quarantine for the moment that contract breaks after delivery. One says "this is what belongs here"; the other says "this is where it goes when it does not".

## Agreement and its enforcement

The book derives Datatype Channel from a simple observation: a messaging system needs many channels because if any type could travel on one pipe, two applications would need only a single channel in each direction — and receivers could no longer assume anything about the payload. The typing is an application convention layered over the transport, which is why the broker happily transmits a byte payload on a text channel and only the receiver's check notices — the mechanics of that failure are in [[What happens when a message of the wrong type arrives on a Datatype Channel]]. When the check fails, the receiver moves the message to the Invalid Message Channel: the working channel stays a typed pipe, the quarantine receives whatever breached it, and the two never swap roles — the invalid channel is not used for successful communication and is not itself a "second datatype".

```d2
direction: right
prod: "Sender" {
  width: 170
  height: 55
  style.fill: "#e3f2fd"
}
dt: "Datatype Channel\none agreed type" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
rcv: "Receiver\nchecks the contract" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
imc: "Invalid Message Channel\ncontract breaches only" {
  width: 280
  height: 75
  style.fill: "#ffebee"
}
prod -> dt
dt -> rcv: "typed traffic"
rcv -> imc: "breach found\nafter delivery" {
  style.stroke-dash: 4
}
```

**Fig. 1.** The quarantine hangs off the receiver, not off the channel: a Datatype Channel carries no invalid traffic by definition — until a sender breaks the agreement.

> [!warning] Sorting in the consumer is not a Datatype Channel
> Putting mixed types on one pipe and branching on type inside the consumer abandons the contract while keeping the channel shape; every receiver now needs every type, and the invalid channel turns into a dumping ground for whatever did not match this consumer's case. How the pattern split degrades when roles are merged is the theme of [[What is the difference between an Invalid Message Channel and a broker queue or topic]].

> [!tip] Interview answer
> Datatype Channel prevents: one type per channel so receivers can assume the payload's shape. Invalid Message Channel corrects: when a delivered message breaks that agreement — wrong type, bad format, missing headers — the receiver parks it on a dedicated quarantine channel. They are two halves of one design: the contract, and where messages go when the contract fails.
