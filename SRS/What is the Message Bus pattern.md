<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messaging #SRS

# What is the Message Bus pattern?

> [!abstract] Short answer
> A **Message Bus** is an **architecture** for the connecting middleware of an enterprise: a shared messaging infrastructure plus a common command set and common data model, so systems join and leave the integration without the others caring — the software analogue of a computer's backplane bus.

## Infrastructure, command set, data model

The bus is a combination of three things: a common communication infrastructure (a messaging system acting as the universal cross-platform adapter, often including routing capability), a common command set covering the operations every connected application understands, and a common data model so messages mean the same thing everywhere. Applications plug in through adapters that map their private interfaces onto the bus contracts — which is why adding or removing a system affects only its own adapter, not the other participants. The bus idea is the architectural umbrella over [[What is the Message Channel pattern]]-based communication, with [[What is the Message Broker pattern]] providing the central routing and the [[What is the Channel Adapter pattern]] providing per-system on-ramps.

```d2
direction: down
bus: "Message Bus\nshared infra + commands + data model" {
  width: 330
  height: 75
  style.fill: "#fff3e0"
}
a1: "CRM" {
  width: 120
  height: 55
  style.fill: "#e3f2fd"
}
a2: "Billing" {
  width: 120
  height: 55
  style.fill: "#e3f2fd"
}
a3: "Inventory" {
  width: 130
  height: 55
  style.fill: "#e3f2fd"
}
a4: "Partner gateway" {
  width: 170
  height: 55
  style.fill: "#e3f2fd"
}
a1 -> bus
a2 -> bus
a3 -> bus
a4 -> bus```

**Fig. 1.** Every application connects to the same backbone through its own adapter; peers never point at each other.

## Why the bus is more than "a broker"

```text
Bus ingredient              What it standardizes
--------------------------  ---------------------------------------------
Communication infra         one messaging system for all participants
Common command set          verbs every app reacts to (Create, Cancel, ...)
Common data model           one canonical shape of shared entities
Adapters                    per-system mapping onto the two contracts above
```

**Listing 1.** Without the command-set and data-model layers you only have shared plumbing; with them, a new application can join by implementing a known contract instead of learning every peer's API.

> [!warning] "Bus" is an architecture, not a product checkbox
> Installing a message broker does not give you a Message Bus: without a shared command set and data model you get point-to-point spaghetti over middleware, and every new system multiplies pairwise translations. The cost shows up exactly when a bus was supposed to pay off — onboarding the fifth system.

> [!tip] Interview answer
> A Message Bus structures the whole integration middleware as a shared backbone: common messaging infrastructure, a common command set, and a common data model, with each system connected via an adapter. Applications can be added or removed without affecting the others, like devices on a hardware bus. It is an architectural pattern — the broker and channel adapters are its implementation pieces.
