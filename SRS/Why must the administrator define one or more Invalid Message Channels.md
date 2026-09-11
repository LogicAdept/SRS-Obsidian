<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# Why must the administrator define one or more Invalid Message Channels

> [!abstract] Short answer
> Because a quarantine destination only works if it is agreed **before** it is needed. The pattern statement says the administrator, designing the messaging system for applications, must define one or more Invalid Message Channels — receivers then have a known place to move improper messages instead of inventing private junk piles or dropping traffic.

## Why up-front, and why "one or more"

The channels are part of the messaging system's design-time topology, exactly like the working channels: applications agree at design or deployment time which invalid channel they use, just as they agree on their Datatype Channels. Defined up front, the channel has three properties that make the pattern work: it is **known** to every receiver, so the move-on-failure code is uniform instead of improvised per endpoint; it is **not used for successful communication**, so its being cluttered with improper messages causes no problem for the happy path; and it is **consumable** — an error handler can attach a receiver and detect messages as they become available, the monitoring duty in [[How does an error handler consume from the Invalid Message Channel]]. The "one or more" matters too: unrelated contract families may want separate quarantines so triage ownership stays clear — a payment platform invalid channel and an IoT telemetry one serve different on-call teams, and per-family channels keep the splitting logic of [[What is the difference between Datatype Channel and Invalid Message Channel]] mirrored on the quarantine side.

```d2
direction: right
adm: "Administrator designs\ntopology" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
work: "Working channels\nagreed per contract" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
imc: "Invalid Message Channel(s)\nagreed, empty in normal use" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
eh: "Error handler\nattached from day one" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}
adm -> work
adm -> imc
imc -> eh
```

**Fig. 1.** The invalid channel is provisioned with the same act of design as the working channels — not improvised when the first bad message arrives.

> [!warning] Defining the queue is not the pattern
> A provisioned channel that no receiver moves to and no error handler watches is just an empty queue with a promising name. The administrator's definition only sets the stage; receivers must still divert ([[What is the Invalid Message Channel pattern]]) and someone must consume — an ignored quarantine is the ignored-error-log failure, and senders watching their own traffic is the complement in [[Why would senders monitor the Invalid Message Channel]].

> [!tip] Interview answer
> The invalid channel is part of the designed topology: the administrator defines it together with the working channels so every receiver knows where improper messages go, the happy path is never affected since the channel carries no success traffic, and an error handler can consume it from day one. More than one is normal — quarantine ownership follows contract families.
