<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/CQRS #Patterns/Enterprise/Integration/Messages/EventMessage #SRS

# What is the difference between a command and an event?

> [!abstract] Short answer
> A **command** is an instruction addressed to a specific receiver to **do** something (`ShipOrder`); an **event** is a **fact** announcing that something already happened (`OrderShipped`). The sender of a command knows the outcome is pending; the sender of an event already knows the outcome and takes no interest in what listeners do.

## Intent, audience, and timing

Both are ordinary messages at the transport level — the difference is semantics. A command names an operation and its parameters, goes to **the** endpoint that owns the operation, and can be **rejected**: the receiver validates and may refuse, so nothing has happened yet. An event describes an occurrence in the past, goes to **any number of subscribers**, and cannot be refused: it is already true. Commands therefore ride point-to-point channels, events ride publish-subscribe channels. Timing differs too — an event's value decays (its timestamp is essential; see [[What is the Event Message pattern]]), while a command usually must eventually execute or fail loudly, even if it is late. In CQRS terms, commands change state through the write model and events record that the state changed ([[What is a command in CQRS]] defines the write-side message; [[What is a projection in CQRS and event sourcing]] is the event's read-side consumer), which is why event-sourced systems treat the event log as the truth. The EIP view of both message types is in [[What is the Command Message pattern]].

```d2
direction: right
c: "Command\nShipOrder(orderId)" {
  width: 230
  height: 65
  style.fill: "#e3f2fd"
}
cq: "Point-to-Point channel" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
h: "Shipping service\nvalidates, may reject" {
  width: 230
  height: 65
  style.fill: "#e8f5e9"
}
e: "Event\nOrderShipped(orderId, at)" {
  width: 240
  height: 65
  style.fill: "#e8f5e9"
}
eq: "Pub-Subscribe channel" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
subs: "N subscribers\nreact independently" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
c -> cq -> h
e -> eq -> subs```

**Fig. 1.** Same wire format, different grammar: imperative to one owner versus past-tense fact to anyone interested.

## Grammar test for a codebase

```text
Naming                Command smell              Event smell
--------------------  -------------------------  ---------------------------
OrderShippedCommand   imperative verb in name    past-tense verb in name
Can be rejected?      yes (validation)           no (already happened)
Interest in result?   yes (reply, status)        no (notification only)
Channel semantics     point-to-point             publish-subscribe
Timestamp needed?     optional                   essential
```

**Listing 1.** If a "command" has no single owner or the sender does not care whether it ran, it is an event wearing the wrong name — and vice versa.

> [!warning] The hybrid "SendEmailEvent" lies about both halves
> A message named like an event but phrased as an instruction produces gossip that assigns duties: every subscriber might "send the email", and nobody is responsible when it does not happen. Either emit a fact (`EmailRequested`) plus an owner for the action, or send a genuine command to the owning endpoint — mixing the two vocabularies is how event-driven systems accumulate unowned behavior.

> [!tip] Interview answer
> A command is an imperative addressed to one receiver that can validate and reject it — nothing has happened until it executes. An event is a past-tense fact broadcast to subscribers who react on their own; it cannot be refused and its timestamp matters. Commands go point-to-point, events go pub-sub, and in CQRS commands drive the write side while events record what changed.
