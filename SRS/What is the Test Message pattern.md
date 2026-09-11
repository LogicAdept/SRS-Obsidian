<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages/TestMessage #SRS

# What is the Test Message pattern?

> [!abstract] Short answer
> A **Test Message** is a synthetic message **injected into the live stream** to verify that a component is not just alive but **correct**: a generator creates test data, an injector tags and inserts it, a separator extracts it from the output, and a verifier compares actual against expected results.

## Heartbeats do not catch a garbler

Control-bus heartbeats prove a component is processing and reporting — they say nothing about correctness: a component can be busy, healthy-looking, and garbling every outgoing message. The test message pattern exercises the real component with known inputs: a **test data generator** produces messages (constant, file-driven, or random); a **test message injector** inserts them into the regular stream, tagged so test data is distinguishable — via a dedicated header field, because smuggling the flag through application fields (like `OrderID = 999999`) overloads business semantics and is a last resort only; a **test message separator** extracts test results from the output — usually a [[What is the Content-Based Router pattern]] keying on the tag; and a **test data verifier** compares actual against expected and flags discrepancies. This is the correctness upgrade to the liveness signals of the [[What is the Control Bus pattern]], and a scheduled, non-invasive complement to the interactive [[What is the Detour pattern]].

```d2
direction: down
gen: "Test data generator" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
inj: "Injector\n+ header: isTest=true" {
  width: 230
  height: 65
  style.fill: "#fff3e0"
}
comp: "Component under test\nprocesses live + test" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
sep: "Separator (CBR)\npeel test results" {
  width: 230
  height: 65
  style.fill: "#fff3e0"
}
ver: "Verifier\nexpected vs actual" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
gen -> inj -> comp -> sep -> ver```

**Fig. 1.** Test data rides the real path end to end; only the header tag separates it from business traffic.

## Tag via infrastructure, not business fields

```text
Do:     set header "test-message" = true; CBR routes it out of band
Avoid:  OrderID = 999999 (overloads business meaning; one collision
        and a real order is swallowed by the verifier)
```

**Listing 1.** The tag is control information — it belongs in a header the application code never inspects.

> [!warning] Test messages in a live system need blast-radius control
> The component under test cannot always tell test from real: side effects (emails sent, shipments booked) do not know about your header. Use inert test payloads where possible, target side-effect-free paths, and rate-limit injection; a verifier bug or a lost tag must degrade to noise, not to corrupted business data.

> [!tip] Interview answer
> A Test Message verifies correctness, not just liveness: a generator creates known inputs, an injector tags them with a header and slips them into the live stream, a content-based separator peels the results out, and a verifier compares expected against actual. It is the scheduled, non-invasive complement to heartbeat monitoring — as long as payloads are inert and tags live in headers, not business fields.
