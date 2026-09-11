<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Transformation/Normalizer #SRS

# What is the Normalizer pattern?

> [!abstract] Short answer
> A **Normalizer** routes messages that are **semantically equivalent but differently formatted** — one per partner, one per format — through a dedicated **Message Translator** each, so everything leaving it matches one common internal format.

## One meaning, N formats, one internal standard

A pay-per-view provider received viewership data from 1700 affiliates, essentially the same facts in essentially different formats. Processing each format downstream is unmanageable; converting pairwise is combinatorial. The normalizer inserts a shape at the boundary: a router detects the incoming format and forwards each message to the translator specialized for that format; every translator outputs the same canonical shape, and downstream sees one format forever. Adding a partner means adding one translator, not touching the consumers. The hard engineering is **format detection**: a type header when you are lucky (root element name for schema-less XML, XPath probes for ambiguity, field-count and data-type heuristics for CSV, file naming conventions as a surrogate datatype channel for file feeds). The normalizer is the router-plus-translator composition — [[What is the Message Router pattern]] feeding per-format [[What is the Message Translator pattern]]s — and the canonical shape it produces is the [[What is the Canonical Data Model pattern]]; a [[What is the Format Indicator pattern]] header from partners removes most of the guessing.

```d2
direction: down
p1: "Partner A\nCSV" {
  width: 150
  height: 55
  style.fill: "#e3f2fd"
}
p2: "Partner B\nXML" {
  width: 150
  height: 55
  style.fill: "#e3f2fd"
}
p3: "Partner C\nEDI" {
  width: 150
  height: 55
  style.fill: "#e3f2fd"
}
r: "Router\ndetect format" {
  width: 180
  height: 60
  style.fill: "#fff3e0"
}
t1: "Translator A" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
t2: "Translator B" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
t3: "Translator C" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
canon: "Canonical format" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
p1 -> r
p2 -> r
p3 -> r
r -> t1
r -> t2
r -> t3
t1 -> canon
t2 -> canon
t3 -> canon```

**Fig. 1.** Detection once per format, translation once per format, one canonical output for everyone downstream.

## Detection strategies, best to worst

```text
Signal                     Reliability    Example
-------------------------  -------------  ------------------------------
Type header / indicator    best           fmt: affiliate-b.v2
Root element / filename    good           <viewership> / *_b_2026.csv
XPath probe                fair           existence of <v2:extra> node
Field count + data types   last resort    12 columns, col 3 numeric
```

**Listing 1.** Every fallback below the first row is guesswork in production; require indicators where you control the partner contract.

> [!warning] Normalization hides partner drift until it bites
> Because consumers only ever see the canonical format, a partner changing their CSV silently fails (or silently mis-translates) at one translator — and everything downstream keeps working, so nobody notices for weeks. Contract-test each translator against partner samples, and alert on detection fallbacks: every message that needed a heuristic is a contract violation in progress.

> [!tip] Interview answer
> A Normalizer handles semantically equal messages in different formats: a router detects each incoming format and sends it to a dedicated Message Translator, and all translators emit one canonical internal format. Consumers see a single shape; each new partner costs one translator. The real engineering is format detection — prefer explicit indicators, treat heuristics as a monitored fallback.
