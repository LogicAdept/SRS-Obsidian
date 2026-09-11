<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# How does an error handler consume from the Invalid Message Channel

> [!abstract] Short answer
> With a receiver attached to the invalid channel that picks up improper messages as they become available and works out what to do — exactly like a utility monitoring an error log. Ideally the cause gets fixed; often it needs a developer or analyst; at minimum, the channel is watched and someone is alerted whenever it is not empty.

## The error-log discipline, in messaging terms

The pattern statement pairs the channel with its consumer: the administrator defines the channel, and "an error handler that wants to diagnose improper messages can use a receiver on the invalid channel to detect messages as they become available". The book develops the analogy directly — the error handler behaves like the program that watches an error log: pick up the strange entry, figure out the cause, and repair it. Since messages parked here usually reflect a coding or configuration mistake on the sender side, full automation is often impossible; the realistic baseline is a process that watches the channel and alerts administrators whenever it contains messages, plus a receiver that preserves the payload intact for a human. If the reason a message is invalid will not be obvious from the payload alone, the receiver should also log details at parking time — the validator-driven variant is in [[How do you use XML or EDI validators with an Invalid Message Channel]].

```d2
direction: down
recv: "Receivers move bad\nmessages to quarantine" {
  width: 290
  height: 75
  style.fill: "#ffebee"
}
ch: "Invalid Message Channel" {
  width: 250
  height: 60
  style.fill: "#fff3e0"
}
consumer: "Error handler consumes\nas messages arrive" {
  width: 280
  height: 75
  style.fill: "#e3f2fd"
}
fix: "Fix cause: sender bug,\nconfig, contract change" {
  width: 300
  height: 75
  style.fill: "#e8f5e9"
}
alert: "Alert when depth > 0\n(nobody reads = no use)" {
  width: 290
  height: 75
  style.fill: "#fff3e0"
}
recv -> ch
ch -> consumer
consumer -> fix
ch -> alert
```

**Fig. 1.** Two obligations come out of the same channel: consume and diagnose, and alert on depth — the second survives even when the first is manual.

> [!warning] An unconsumed channel is an unread log
> Parking is only triage's first step; a quarantine that fills quietly still consumes storage and can hit queue quotas until the broker refuses traffic. What happens next after diagnosis — moving a corrected message back through the flow — is the replay procedure in [[How do you replay messages from an Invalid Message Channel]], and the sender-side mirror of the same monitoring duty is [[Why would senders monitor the Invalid Message Channel]].

> [!tip] Interview answer
> You attach a receiver to the invalid channel — the pattern says the error handler detects improper messages as they become available. It works like an error-log watcher: diagnose, fix the underlying sender or configuration problem, and because the cause is usually a code or config mistake, at minimum run an automated watcher that alerts whenever the channel is non-empty. Log details at parking time when the payload alone will not explain the failure.
