<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# How does validity of a message depend on the receiver

> [!abstract] Short answer
> A message is not inherently valid or invalid. The **receiver's expectations** — its datatype, schema, and required headers — decide. The same bytes can be valid for one endpoint and garbage for another, so validity is a property of the message-receiver pair, not of the message alone.

## Consequences of the receiver-relative definition

The definition drives three rules the book states explicitly. First, it is the **sender's responsibility** to publish messages that every receiver of the channel will consider valid; a sender that breaks the contract is "ignored" by the receivers, which reroute its messages to the Invalid Message Channel instead of processing them. Second, if a message is valid for one receiver on a channel, it should be valid for **every** receiver on that channel — a channel is an agreement, and receivers that disagree about validity expose a broken agreement. Third, receivers with genuinely different contracts should **not share the channel** at all; that is the Datatype Channel discipline described in [[What is the Datatype Channel pattern]].

```d2
direction: right
sender: "Sender publishes\none payload" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
ch: "Channel with one\nagreed contract" {
  width: 250
  height: 70
  style.fill: "#fff3e0"
}
r1: "Receiver A\nparses, processes" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
imc: "Receiver B cannot process\n-> Invalid Message Channel" {
  width: 300
  height: 80
  style.fill: "#ffebee"
}
sender -> ch
ch -> r1
ch -> imc: "contract mismatch\n= agreement broken"
```

**Fig. 1.** When two receivers on one channel disagree about validity, the fix is splitting the channel, not arguing about which receiver is right.

> [!warning] The dumping-ground failure
> One channel shared across endpoints with different contracts turns the invalid channel into a landfill of messages that were valid for somebody else. The symptom is a quarantine that never empties while every receiver claims it is not its problem — the mixed-types anti-shape is the mirror image of [[What is the difference between Datatype Channel and Invalid Message Channel]].

What counts as "cannot process" in practice — parsing, schema, headers, wrong channel — is cataloged in [[What kinds of delivered messages does a receiver treat as invalid]], and the case where the message is actually fine but the business fails is separated in [[Why should you not treat an application error as an invalid message]].

> [!tip] Interview answer
> Validity is judged by the receiver against its own contract, so it is relative, not absolute. The sender owes every receiver on the channel a processable message; if one receiver parks a payload as invalid, all receivers sharing that contract would. Two receivers that disagree should never share a channel — split it — and receivers "ignore" contract-breaking senders by moving their traffic to the invalid channel.
