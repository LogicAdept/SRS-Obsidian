<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages/FormatIndicator #SRS

# What is the Format Indicator pattern?

> [!abstract] Short answer
> A **Format Indicator** is a field in the message that says **what format the body uses** — a version number, a reference to a schema document, or the embedded schema itself — so a receiver supporting several formats picks the right parser instead of guessing.

## Designing for the format change that will come

Messages agree on a format today; integration solutions live for years; formats change. The indicator lets the sender declare which format it used, and lets a receiver that understands several formats — during a migration window — interpret each message correctly. Three implementation styles exist: a **version number** or string naming the format (both sides must agree what `v2` means), a **foreign key** pointing at a format document (filename, registry subject, URL — both sides must agree on the mapping), and a **format document** embedded in the message (a schema traveling with the data; both sides must agree on the schema language). In practice: Kafka's Schema Registry subject-and-version is the foreign-key style; a `JMSType` or `eventType=order.v2` header is the version style. The indicator is what lets a [[What is the Message Translator pattern]] or [[What is the Normalizer pattern]] be selected automatically — the router reads the indicator, not the payload.

```d2
direction: down
msg: "Message\nformat: order.v2" {
  width: 210
  height: 65
  style.fill: "#e3f2fd"
}
r: "Receiver\nsupports v1 + v2" {
  width: 210
  height: 65
  style.fill: "#fff3e0"
}
p1: "v1 parser" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
p2: "v2 parser" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}
msg -> r
r -> p1: "indicator = v1"
r -> p2: "indicator = v2"```

**Fig. 1.** One consumer, multiple supported formats; the header — not payload sniffing — chooses the parser.

## Indicator styles side by side

```text
Style           Header looks like            Cost
--------------  ---------------------------  -------------------------------
Version number  fmt: order.v2                registry discipline; agree on names
Foreign key     schema: orders-2.json        lookup hop at receiver
Format doc      embedded XSD/JSON Schema     big headers; parsing schema each time
```

**Listing 1.** Version numbers dominate in production because they are cheap and registry-managed; embedded documents are rare outside self-describing B2B payloads.

> [!warning] An indicator nobody migrates on is decoration
> If consumers "support" v2 but the migration has no end date, you pay dual-parser complexity forever. The indicator also must change **only** when the format truly changes — bumping it for cosmetic edits trains consumers to ignore it, and then a real format change ships to the wrong parser.

> [!tip] Interview answer
> A Format Indicator is a message field declaring which format the body uses — a version number, a pointer to a schema document, or an embedded schema. It lets receivers that support several formats pick the right parser and makes format migrations explicit. Version numbers backed by a schema registry are the common production choice; the field is only valuable if you actually plan and retire old versions.
