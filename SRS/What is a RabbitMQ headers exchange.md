<!--
reps: 0
priority: 0
-->
#Messaging/Tools/RabbitMQ #SRS

# What is a RabbitMQ headers exchange

> [!abstract] Short answer
> A headers exchange routes by the message's header table instead of the routing key. Each binding carries an arguments map and an `x-match` rule — `all` means every listed header must match, `any` means at least one — so routing can depend on several independent attributes.

## Matching mechanics

Publishers set application headers such as `format: pdf`, `tenant: acme`, `version: 2`. Bindings declare which header values they require plus `x-match: all` (logical AND) or `any` (logical OR). The special argument `x-match: all-with-x`/`any-with-x` also considers headers starting with the `x-` prefix in the comparison. The routing key is ignored entirely, so a publish whose headers satisfy several bindings produces a copy per binding — this is attribute-based routing rather than string addressing.

```d2
direction: down
msg: "headers:\nformat=pdf, tenant=acme" {
  width: 240
  height: 100
  style.fill: "#e3f2fd"
}
b1: "binding A\nx-match all\nformat=pdf, tenant=acme" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
b2: "binding B\nx-match any\nformat=xml" {
  width: 240
  height: 100
  style.fill: "#ffebee"
}
b3: "binding C\nx-match all\nformat=pdf" {
  width: 230
  height: 100
  style.fill: "#e8f5e9"
}
msg -> b1
msg -> b2
msg -> b3
```

**Fig. 1.** all requires every header value to match, any requires one; this publish matches A (both) and C (pdf), not B (xml missing).

## When it earns its cost

Headers matching is heavier than direct or topic key comparison, so it pays off when routing criteria are genuinely multi-dimensional — content format plus tenant plus schema version — and would otherwise force combinatorial topic keys. Single-attribute routing belongs to direct or topic; see [[What RabbitMQ exchange types exist]] for the comparison, [[What is a RabbitMQ routing key]] for why the key is unused here, and [[What is a RabbitMQ binding]] for the argument map a headers binding carries.

```java
Map<String, Object> bindArgs = Map.of(
        "x-match", "all",
        "format", "pdf",
        "tenant", "acme");
ch.exchangeDeclare("docs", "headers", true);
ch.queueBind("acme-pdf", "docs", "", bindArgs);
```

**Listing 1.** A binding that requires both header values; `queueBind`'s routing-key argument is empty by design.

> [!warning] Headers values are matched as stored
> Header values are typed AMQP values — the string "2" does not match the integer 2, and a missing header simply fails the binding. Interviews catch candidates who assume case-insensitive or stringified comparison; the broker compares values as published.

> [!tip] Interview answer
> A headers exchange ignores the routing key and matches the message header table against binding arguments: x-match all means every pair matches, any means at least one. It is the tool for multi-attribute routing — format, tenant, version — at the cost of heavier per-publish matching than direct or topic.
