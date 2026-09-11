<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# How does the Invalid Message Channel pattern work

> [!abstract] Short answer
> The receiver receives a message, runs its own validation (type, format, schema, required headers), and on failure **moves the intact message to a dedicated channel** that is not used for successful traffic. An error-handler endpoint consumes that channel and diagnoses or replays the payload.

## The move is a send, not a broker action

The messaging system has already done its job when the problem appears: the message was delivered to the receiver. Everything after that decision is application code. The receiver that cannot process the message sends it — body and headers unchanged — to the invalid channel, which the administrator defines at design or deployment time together with the working channels. Because the channel carries no successful traffic, its contents never slow the happy path down.

The Jakarta Messaging specification describes exactly this move: a listener that cannot process a message should divert it to "some form of application-specific 'unprocessable message' destination" instead of throwing. The EIP book's JMS example names that destination `jms/InvalidMessages` and resends the message to it, copying the original id onto the correlation id first — the mechanics are in [[How do you preserve the original Message ID when parking an invalid JMS message]]. The full decision flow, including the exception case of throwing instead of diverting, is in [[What is the JMS unprocessable message destination]] and [[What happens if a JMS MessageListener throws a RuntimeException instead of diverting an invalid message]].

```d2
direction: down
recv: "Receiver gets a\ndelivered message" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
check: "Processable?\ntype · format · schema · headers" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
work: "Process normally" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
move: "Send unchanged to\nInvalid Message Channel" {
  width: 300
  height: 75
  style.fill: "#ffebee"
}
eh: "Error handler consumes:\nlog, diagnose, replay" {
  width: 300
  height: 75
  style.fill: "#ffebee"
}
recv -> check
check -> work: yes
check -> move: no
move -> eh
```

**Fig. 1.** Only the receiver can make the call, because only it knows the contract; the broker considered the message deliverable at this point.

## What the error handler is for

> [!warning] Throwing is not diverting
> If the receiver requeues the message or lets an exception escape instead of moving it, the payload comes straight back — a poison loop. The pattern's value only materializes when the message leaves the working channel; the monitoring duty that follows is the same error-log discipline as [[How does an error handler consume from the Invalid Message Channel]].

The message stays parked on the invalid channel until an error handler consumes it, works out the cause — usually a coding or configuration mistake on the sender side — and the underlying problem is fixed. Why a parked payload must not simply be retried is [[Why should you not retry a structurally invalid message]].

> [!tip] Interview answer
> A receiver validates after delivery; on failure it sends the untouched message to a dedicated invalid channel instead of requeueing or dropping it. That channel is provisioned up front, carries no successful traffic, and is watched by an error handler that logs, diagnoses, and possibly replays. The key split: the broker delivered the message, so this is application-level quarantine, not broker dead-lettering.
