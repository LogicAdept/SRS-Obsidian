<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Content Filter pattern?

> [!abstract] Short answer
> A **Content Filter** removes data items from a message — or flattens its structure — leaving only what matters downstream: less payload to move, store, and parse, and nothing sensitive where it does not belong.

## Shrink, flatten, and hide

Three motivations dominate. **Volume**: messages from packaged systems mirror normalized database shapes — deep nested repeating groups — while the consumer needs three fields; stripping the rest cuts bandwidth, broker memory, and consumer CPU. **Clarity**: flattening a normalized tree into a simple list makes the message match the receiving system's model instead of the sending system's storage. **Privacy and security**: dropping fields the receiver has no right to see (PII, internals) limits exposure in every downstream store and log the message will touch. The pattern is the inverse operation of the [[What is the Content Enricher pattern]] and works on fields **inside** one message — which is exactly what distinguishes it from the [[What is the Message Filter pattern]], whose job is to discard whole messages; and when the removed data must come back later via a stored copy, that combination is the [[What is the Claim Check pattern]].

```d2
direction: down
in: "Message\n20 fields, 4 levels deep" {
  width: 240
  height: 65
  style.fill: "#e3f2fd"
}
f: "Content Filter\nkeep, flatten, strip PII" {
  width: 250
  height: 75
  style.fill: "#fff3e0"
}
out: "Message\n3 fields, flat" {
  width: 210
  height: 60
  style.fill: "#e8f5e9"
}
in -> f -> out```

**Fig. 1.** Same business fact, one tenth of the bytes: fields removed, structure flattened.

## Removal with an allow-list

```java
public Map<String, Object> filter(Map<String, Object> msg) {
    return Map.of(
        "orderId", msg.get("orderId"),          // keep
        "amount",  msg.get("amount"),           // keep
        "status",  msg.get("status"));          // keep
    // everything else (customer PII, internals) is gone by construction
}
```

**Listing 1.** An allow-list beats a deny-list: forgetting to remove a new sensitive field is a data leak, while forgetting to keep one is a loud parse error downstream.

> [!warning] Filtering data you will need later is a one-way door
> Once the message is stripped, the data exists only in the source system — debugging, auditing, and reprocessing all get harder retroactively. If the removed data has any future use, pair the filter with an archived full copy (a claim-check store or a Wire Tap into storage) **before** deciding that removal is cheap.

> [!tip] Interview answer
> A Content Filter removes unimportant or sensitive fields from a message and can flatten nested structures, so downstream systems receive less data shaped to their needs — the inverse of a Content Enricher. It differs from a Message Filter, which drops entire messages. Prefer allow-lists over deny-lists, and archive the full payload first if anything might need it later.
