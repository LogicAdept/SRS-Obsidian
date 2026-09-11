<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Routing/RoutingSlip #SRS

# What is the Routing Slip pattern?

> [!abstract] Short answer
> A **Routing Slip** is a **list of processing steps attached to the message** itself. Each step's wrapper reads the slip, executes, and forwards the message to the next step — so the sequence is chosen **per message at runtime**, not fixed in the wiring.

## The itinerary travels with the payload

Pipes-and-filters wires steps statically; the slip makes the itinerary data. A component at the start computes the required steps for this message — this type needs credit-card validation, that one does not; VPN customers skip decryption — attaches the list, and dispatches to the first step. Every step then looks at the slip, does its work, and routes to the next entry. Two assumptions make slips the right tool: the step sequence is decided **up front** (before processing begins) and it is **linear** — no branches on intermediate results, no parallel legs. When either assumption fails, the answer is a [[What is the Process Manager pattern]], which keeps state centrally instead of carrying it. Slip state itself needs hygiene: mark completed steps to survive reprocessing, because at-least-once delivery will replay a step. The slip is the data-driven cousin of the [[What is the Dynamic Router pattern]]; both avoid hard-wiring routes, see [[What is the Message Router pattern]] for the base case.

```d2
direction: right
m: "Message + slip\n[decrypt, auth, credit-check]" {
  width: 270
  height: 75
  style.fill: "#e3f2fd"
}
s1: "Step: decrypt\nmark done" {
  width: 170
  height: 60
  style.fill: "#fff3e0"
}
s2: "Step: authenticate" {
  width: 190
  height: 60
  style.fill: "#fff3e0"
}
s3: "Step: credit check" {
  width: 190
  height: 60
  style.fill: "#fff3e0"
}
done: "Done\n(empty slip)" {
  width: 150
  height: 55
  style.fill: "#e8f5e9"
}
m -> s1 -> s2 -> s3 -> done```

**Fig. 1.** Each hop consumes one entry from the slip; when the list is empty the message has finished its journey.

## Slip as data

```json
{
  "body": { "orderId": "O-9", "amount": 250 },
  "slip": ["decrypt", "authenticate", "credit-check"],
  "slip-state": { "decrypt": "done" }
}
```

**Listing 1.** The slip is part of the message: read next step, execute, mark, forward. `slip-state` makes redelivery idempotent per step.

> [!warning] A slip is linear and editable by everyone who touches it
> The moment a step needs to branch on results, the slip model collapses into ad-hoc state machinery — switch to a process manager. And because the itinerary rides in the message, any component (or attacker with access to the channel) can alter the route; slips carrying security-relevant steps need integrity protection on the slip fields.

> [!tip] Interview answer
> A Routing Slip attaches the ordered list of processing steps to the message itself; each step executes and forwards to the next entry, so the itinerary is computed per message at runtime instead of being fixed in wiring. It fits linear, known-up-front sequences; conditional or parallel flows need a Process Manager. Mark completed steps so redeliveries do not re-execute them.
