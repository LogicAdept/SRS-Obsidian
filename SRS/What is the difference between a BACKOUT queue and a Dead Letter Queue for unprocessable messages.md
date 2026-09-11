<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS

# What is the difference between a BACKOUT queue and a Dead Letter Queue for unprocessable messages

> [!abstract] Short answer
> In IBM MQ terms: the **Dead Letter Queue** is where messages that **could not be delivered** go, always prefixed with the `MQDLH` header. A **backout requeue queue** is where a **delivered but unprocessable** (poison) message goes after repeated rollbacks — an ordinary local queue named by `BOQNAME`, no `MQDLH` required. The first is delivery failure; the second is the Invalid Message Channel role.

## Delivery failure versus application-rejected

IBM's administering guide defines the DLQ as a local queue where messages that cannot be delivered to their correct destination are stored; queue managers, message channel agents, and applications put messages there, and **every** message on the DLQ must be prefixed with a dead-letter header `MQDLH` — the queue manager and MCA always add it, and an application putting a message on the DLQ must supply it itself. The bundled `runmqdlq` handler (or the `amqsdlq` sample) processes the DLQ by matching messages against a rules table.

The backout path is receiver-side and driven by delivery attempts. The JMS guide documents it: whenever an application rolls a message back, the queue manager increments the message's `BackoutCount`; the IBM MQ classes for JMS compare that count with the queue's `BOTHRESH` (backout threshold) attribute, and once `BackoutCount` is greater than or equal to `BOTHRESH`, the message is considered poison and moved to the queue named by `BOQNAME`. If it cannot be put on the backout queue, it goes to the queue manager's dead-letter queue or is discarded depending on the message's report options. With `BOTHRESH` at its default of 0, poison handling is disabled and messages just return to the input queue.

```text
ALTER QLOCAL(APP.WORK) BOTHRESH(3) BOQNAME(APP.UNPROCESSABLE)
```

**Listing 1.** The MQSC wiring from the JMS poison-message guide: three strikes, then the delivered-but-unprocessable message parks on the backout queue.

```text
                  BACKOUT queue            Dead Letter Queue
Put by            JMS client on threshold  queue manager · MCA · app
Required header   none (plain message)     MQDLH with reason
Means             delivered, rolled back   could not be delivered
Replay            route back as-is         strip MQDLH first
```

**Listing 2.** The consequence for triage: a backout message can be forwarded to the target queue unchanged; a DLQ message needs its dead-letter header removed first.

> [!warning] BOTHRESH(0) is not "safe"
> Leaving the threshold at 0 disables the move entirely: an unprocessable message bounces between queue and application indefinitely. And `BOTHRESH` without `BOQNAME` hands the decision to the message's report options — discard or dead-letter — so the quarantine you planned silently becomes the DLQ. The pattern-level reading of both queues is [[What is the difference between Invalid Message Channel and Dead Letter Channel]], the poison-loop context is [[How does a receiving application move a poison message to an Invalid Message Channel]], and what a triage process should do with parked messages is [[How does an error handler consume from the Invalid Message Channel]].

> [!tip] Interview answer
> The DLQ is for messages the messaging system could not deliver; everything on it carries an MQDLH header stating the reason, and it is filled by queue managers, channel agents, and applications. The backout queue is for messages that were delivered but kept failing in the application — after `BOTHRESH` rollbacks the JMS client moves them to `BOQNAME`, no special header needed. That mirrors the pattern split: delivery failure versus receiver-invalid.
