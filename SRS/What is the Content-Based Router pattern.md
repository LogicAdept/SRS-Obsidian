<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Routing #SRS

# What is the Content-Based Router pattern?

> [!abstract] Short answer
> A **Content-Based Router** inspects **message content** — field existence, field values, structure — and routes each message to the channel whose recipient can handle it. It answers the case where one logical function is implemented by several physical systems.

## Route by what the message says

The order flow validates an order, then needs an inventory check — but the warehouse is split across systems, each handling specific items. Something must look inside the message and pick the right inventory system; that is the CBR. Routing can key off existence of fields, specific values, or structure, and in sophisticated setups becomes a configurable rules engine computing the destination from a rule set. Two operational truths come with it: the routing function is a **point of frequent maintenance** (item catalogs and systems change), so keep the rules data-driven and testable; and since the router reads content, it couples itself to the message schema — another reason the [[What is the Canonical Data Model pattern]] and a [[What is the Format Indicator pattern]] header make CBR rules stable. It is the best-known specialization of the [[What is the Message Router pattern]]; Apache Camel's `choice()`/`when()` DSL exists precisely to express it.

```d2
direction: down
in: "Validated order" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
cbr: "Content-Based Router\nitem category field" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
s1: "Furniture inventory" {
  width: 210
  height: 60
  style.fill: "#e8f5e9"
}
s2: "Electronics inventory" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
s3: "Perishables inventory" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
in -> cbr
cbr -> s1: "category=furniture"
cbr -> s2: "category=electronics"
cbr -> s3: "category=food"```

**Fig. 1.** One logical check, three physical systems: the payload's category field decides the lane.

## Declarative rules, not imperative spaghetti

```java
from("orders.validated")
    .choice()
        .when(simple("${body.category} == 'electronics'"))
            .to("inventory.electronics")
        .when(simple("${body.category} == 'food'"))
            .to("inventory.perishables")
        .otherwise()
            .to("inventory.general");
```

**Listing 1.** A Camel content-based route: conditions are declarative expressions over the content, and the `otherwise` branch handles unknowns explicitly.

> [!warning] Unknown content needs a designed destination
> A CBR without an `otherwise` path either drops or dead-letters every message that does not match a rule — often discovered the week a new category ships. Rule drift is the second trap: when rules are duplicated in code and config, one side silently wins, and messages start landing on systems that no longer want them.

> [!tip] Interview answer
> A Content-Based Router looks inside each message — fields, values, structure — and routes it to the channel of the system that can handle it, solving the one-logical-function-many-systems problem. It is a Message Router specialized on payload content, usually expressed as configurable rules, like Camel's choice-when DSL. Keep rules data-driven, always design the no-match path, and expect the rule set to change often.
