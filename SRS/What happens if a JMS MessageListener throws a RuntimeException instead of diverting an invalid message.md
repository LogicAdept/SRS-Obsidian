<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# What happens if a JMS MessageListener throws a RuntimeException instead of diverting an invalid message

> [!abstract] Short answer
> The specification calls it a client programming error. What follows depends on the session's acknowledgment mode: automatic-ack modes redeliver immediately, `CLIENT_ACKNOWLEDGE` moves on and needs a manual `recover()` to redeliver, and a transacted session just delivers the next message — no automatic rollback. Providers are expected to flag such listeners as malfunctioning.

## Session mode decides the damage

The specification spells out all four outcomes for a `RuntimeException` escaping `onMessage`. With `AUTO_ACKNOWLEDGE` or `DUPS_OK_ACKNOWLEDGE` the message is **immediately redelivered**; how many times a provider redelivers before giving up is provider-dependent, and each redelivery sets `JMSRedelivered` and increments `JMSXDeliveryCount`. With `CLIENT_ACKNOWLEDGE` the listener simply gets the next message — the failed one stays unacknowledged, and redelivering it requires the client to call `recover()` on the session explicitly. In a transacted session the next message is delivered too, and the `RuntimeException` does **not** roll the session back by itself; the client chooses commit or rollback. Because an exception-throwing listener usually indicates a bug, the spec adds that providers should flag such clients as possibly malfunctioning — the advisory sits right next to the divert-to-unprocessable-destination recommendation in [[What is the JMS unprocessable message destination]].

```text
Session mode            After a RuntimeException escapes onMessage
----------------------  --------------------------------------------------
AUTO_ACKNOWLEDGE        immediate redelivery; give-up count is
DUPS_OK_ACKNOWLEDGE     provider-dependent; JMSRedelivered + JMSXDeliveryCount
CLIENT_ACKNOWLEDGE      next message delivered; manual session recover()
                        required for redelivery
Transacted              next message delivered; no automatic rollback —
                        the client must roll back itself
```

**Listing 1.** The specification's per-mode consequences, verbatim in structure: only the auto-ack modes redeliver on their own.

> [!warning] Throwing is a poison loop, not error handling
> For a structurally bad message, auto-ack redelivery replays the identical failure until the provider gives up — the loop the Invalid Message Channel exists to break, and the reason the receiver should park on first detection as in [[What happens if a receiver puts an invalid message back on the original channel]]. On transacted sessions the trap is subtler: developers who expect the exception to roll the transaction back get the next message committed instead.

> [!tip] Interview answer
> A `RuntimeException` out of `onMessage` is a client programming error per the spec. Auto-ack modes immediately redeliver — provider-dependent give-up, `JMSRedelivered` set, `JMSXDeliveryCount` incremented; `CLIENT_ACKNOWLEDGE` delivers the next message and needs a manual recover; a transacted session does not roll back automatically. The spec's own advice: catch and divert to an unprocessable-message destination instead.
