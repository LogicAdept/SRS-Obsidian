<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How does a receiving application move a poison message to an Invalid Message Channel

> [!abstract] Short answer
> Validate first, then act: try the payload against the receiver's checks; if it can never pass, move it once — an explicit dead-letter API call with a reason, or a send to the quarantine — instead of abandoning it into an unbounded redelivery loop. The broker's delivery counter is a safety net, not the design.

## The receiver's decision loop

A poison message is a delivery whose content always fails — a bad payload, data that divides by zero, an unknown region code. The receiver that catches the failure and abandons (or requeues, or lets the lock expire) will meet the same message again immediately; that loop is why the two wrong behaviors — requeue and silent drop — are forbidden by the pattern ([[What happens if a receiver puts an invalid message back on the original channel]]). The working loop has stages: validate at the top; for plausibly transient faults retry a bounded number of times, which on Azure Service Bus increments the delivery count on every abandon or lock expiry; once the failure is clearly structural, call the explicit move — `Deadletter` with a reason and description, which stamps `DeadLetterReason`/`DeadLetterErrorDescription` on the parked message — or send to the dedicated invalid channel. The broker's `MaxDeliveryCount` (default 10 on Service Bus) then only catches applications that keep abandoning past the app's own policy, and IBM MQ's JMS client implements the same shape with `BackoutCount` compared against the queue's `BOTHRESH`, moving the message to `BOQNAME` at threshold — the comparison of that queue with the DLQ is in [[What is the difference between a BACKOUT queue and a Dead Letter Queue for unprocessable messages]].

```d2
direction: down
recv: "Receive (peek-lock)" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
val: "Validate payload" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
tr: "Transient? retry\nbounded times" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
dead: "Deadletter(reason, description)\nor send to invalid channel" {
  width: 340
  height: 80
  style.fill: "#ffebee"
}
net: "Broker cap:\nMaxDeliveryCount / BOTHRESH" {
  width: 290
  height: 70
  style.fill: "#fff3e0"
}
recv -> val
val -> tr: "may pass later"
val -> dead: "never passes"
tr -> net: "abandon loop\n(safety net)"
```

**Fig. 1.** The explicit move is the designed path; the broker counter only exists for applications that keep abandoning.

> [!warning] Abandoning is a retry, not a decision
> An abandon makes the message available again at once (and an expired lock does the same, with reordering risk), so catch-and-abandon without a cap is the poison loop in slow motion; teams that set the delivery count absurdly high have merely disabled the net. The parked message still needs a consumer and replay discipline — [[How do you replay messages from an Invalid Message Channel]] — and classification discipline against business failures ([[Why should you not treat an application error as an invalid message]]).

> [!tip] Interview answer
> The receiver validates, retries bounded times only for plausibly transient faults, and then makes one explicit move: dead-letter the message with a reason — Service Bus `Deadletter` stamping DeadLetterReason — or send it to the invalid channel, as IBM MQ does at the BOTHRESH threshold. MaxDeliveryCount is the safety net for apps that keep abandoning, not the mechanism you design around.
