<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# Why should you not retry a structurally invalid message

> [!abstract] Short answer
> Because its failure is deterministic: the same validation — missing values, wrong types, schema mismatch, wrong channel contract — fails identically on every attempt. Redelivery buys nothing, burns broker capacity, and delays detection. The receiver should park it once, visibly, and fix the sender.

## Deterministic failure makes redelivery a no-op

A message can be invalid because required values are missing, values have the wrong type, the structure does not match the agreed schema, or the payload type does not belong on that channel. All four are pure functions of the message and the receiver's contract — no external state changes between attempts, so attempt two is guaranteed to repeat attempt one. That is the defining contrast with transient failures (a downstream timeout, a connection blip), which can genuinely succeed on a later attempt and therefore deserve a capped retry, the split laid out in [[What is the difference between the Retry Pattern and Invalid Message Channel]]. The correct move for the deterministic case is immediate: take the message off the working channel and park it on the Invalid Message Channel, where it is neither lost nor in anyone's way — leaving it on the channel just recreates the loop described in [[What happens if a receiver puts an invalid message back on the original channel]].

```d2
direction: down
in: "Message delivered" {
  width: 200
  height: 55
  style.fill: "#e3f2fd"
}
cls: "Classify the failure" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
tr: "Transient (timeout, blip)" {
  width: 270
  height: 65
  style.fill: "#e8f5e9"
}
st: "Structural (schema, headers,\ntype, channel contract)" {
  width: 280
  height: 75
  style.fill: "#ffebee"
}
rt: "Retry with backoff,\nthen dead-letter" {
  width: 260
  height: 65
  style.fill: "#e8f5e9"
}
pk: "Park once on the\nInvalid Message Channel" {
  width: 270
  height: 65
  style.fill: "#ffebee"
}
in -> cls
cls -> tr: "depends on the world"
cls -> st: "pure function of payload"
tr -> rt
st -> pk
```

**Fig. 1.** One classification decision decides the whole policy — and it is the receiver, which knows the contract, that makes it.

> [!warning] Retry-then-park is imported from DLQ-land
> Guidance that bolts "retry N times, then park" onto structural failures comes from Dead Letter Channel practice, where the broker cannot tell transient from permanent and hedges with a redelivery counter. A receiver that already knows the failure is a contract violation has no reason to hedge — and every reason to make the failure visible immediately instead of after a retry window.

> [!tip] Interview answer
> Structural invalidity is deterministic: the same header check, type check, or schema validation fails on every redelivery, so retrying just amortizes the same failure while clogging the channel. Transient failures — timeouts, connection issues — are the opposite case and do deserve capped retries. Classify first; park the deterministic ones on the invalid channel immediately.
