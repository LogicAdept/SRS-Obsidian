<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Messaging Mapper pattern?

> [!abstract] Short answer
> A **Messaging Mapper** is a separate class holding the **mapping logic between domain objects and messages**: it turns domain objects into message data and updates domain objects from message data, while neither the domain objects nor the messaging infrastructure know the mapper exists.

## Keeping objects and messages strangers

Message data is usually derived from domain objects — a Document Message may directly represent one, command fields are extracted from several. But objects rely on references, inheritance, and behavior; messaging infrastructures must exchange data with any platform and understand none of that. Bridging in place would pollute one side: domain classes growing serialization fields they should not know about, or infrastructure layer learning business semantics. The mapper is a specialization of the Mapper pattern (as in Data Mapper): it references both worlds so neither references the other. The trade is a real one — mappers add a layer with bidirectional conversion logic that must be kept in sync on both directions, which is why teams often co-locate simpler cases in a [[What is the Messaging Gateway pattern]] and reserve the mapper for rich domain models; the pure-format equivalent between systems is the [[What is the Message Translator pattern]].

```d2
direction: down
dom: "Domain objects\nOrder, Customer" {
  width: 210
  height: 65
  style.fill: "#e8f5e9"
}
mm: "Messaging Mapper\ndomain <-> message fields" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
inf: "Messaging infrastructure\nmessages, channels" {
  width: 220
  height: 65
  style.fill: "#e3f2fd"
}
dom -> mm
mm -> inf```

**Fig. 1.** The mapper is the only component aware of both sides; each side stays ignorant of the other.

## What belongs in the mapper

```java
class OrderMessagingMapper {
    OrderCreatedEvent toMessage(Order o) {          // domain -> message
        return new OrderCreatedEvent(o.id(), o.total(), o.updatedAt());
    }
    void apply(Order o, OrderShippedEvent e) {      // message -> domain
        o.markShipped(e.shipmentId(), e.deliveredAt());
    }
}
```

**Listing 1.** Both directions in one place: conversion is the mapper's whole job, with no I/O and no channel decisions inside.

> [!warning] Two directions, one truth — or none
> The domain-to-message and message-to-domain paths are maintained independently but must agree on semantics; teams evolve one side, forget the other, and the mismatch surfaces as silent data loss on the inbound path. Version message contracts, and property-test the round trip (`apply(o, toMessage(o))` preserves the domain meaning) — the mapper is the one place this invariant is checkable.

> [!tip] Interview answer
> A Messaging Mapper is a dedicated class that converts between domain objects and messages in both directions, while the objects and the infrastructure each stay unaware of the other. It is the messaging sibling of Data Mapper. The risks are drift between the two conversion directions, so message contracts need versioning and round-trip tests; simpler cases often live inside a gateway instead.
