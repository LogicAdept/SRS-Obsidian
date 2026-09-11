<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Content Enricher pattern?

> [!abstract] Short answer
> A **Content Enricher** takes a message that lacks required data and **fetches the missing items from an external source** — a database, directory, environment, or computation — then appends them, producing a message the target system can actually consume.

## The sender cannot know everything

An order message carries an order number; the customer-management system downstream requires the customer id, name, and address. The sender's designers did not know, or deliberately omitted, the extra fields — duplicating them would have been redundant or untrustworthy. The enricher uses what is in the message (key fields) to look up what is missing and appends it; the original fields may be carried over or dropped, per the receiver's needs. The book's taxonomy of enrichment sources is a good interview frame: **computation** (derive values — a state code from a ZIP, a message length; essentially a pure translator), **environment** (timestamps, host, tenant — nothing external is called), and **another system** (the common case: DB, LDAP, file, or a human). The third case is the dangerous one: the enricher now has an external dependency on the hot path of every message, which is the difference from a pure [[What is the Message Translator pattern]]; the reverse operation — removing data — is the [[What is the Content Filter pattern]].

```d2
direction: down
in: "Order message\norderNo only" {
  width: 200
  height: 65
  style.fill: "#e3f2fd"
}
en: "Content Enricher\nlookup by orderNo" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
src: "External source\n(customer DB)" {
  width: 220
  height: 65
  style.fill: "#ffebee"
}
out: "Enriched message\n+ customerId, name" {
  width: 230
  height: 65
  style.fill: "#e8f5e9"
}
in -> en
en -> src: "read"
en -> out: "append"```

**Fig. 1.** Key fields in the message drive the lookup; missing attributes join the message before it moves on.

## The lookup that defines the pattern

```java
Order o = parse(in);
Customer c = customerDb.findById(o.customerId())   // the dependency
        .orElseThrow(NoSuchElementException::new);
EnrichedOrder out = new EnrichedOrder(
        o.orderNo(), c.id(), c.name(), c.address());
producer.send(crmChannel, out);
```

**Listing 1.** One external read per message: the enricher's latency, availability, and cache policy are now part of the integration contract.

> [!warning] The enricher inherits every failure of its source
> If the customer DB slows down, the whole flow slows down; if it is down, orders stop — a coupling the original sender never had. Cache aggressively where staleness is tolerable, define behavior for lookups that miss (dead letter, not block), and be honest that "just enrich it in the middle" added a distributed join to the architecture.

> [!tip] Interview answer
> A Content Enricher augments messages that lack required data by looking the missing fields up externally and appending them. Sources range from pure computation and environment values — which make it just a translator — to another system, which makes it a distributed join with a real dependency. Design for lookup misses and source latency, and distinguish it from its inverse, the Content Filter.
