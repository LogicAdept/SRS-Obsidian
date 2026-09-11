<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# How do you replay messages from an Invalid Message Channel

> [!abstract] Short answer
> Fix the cause first, then re-submit — from the quarantine back to the original destination, ideally by tooling that preserves the message. Replay is a deliberate operator action after repair, never an automatic loop: replaying a message whose cause is not fixed simply recreates the failure.

## The repair-then-resubmit loop

Replay is the third act of the pattern: park (the receiver's move), diagnose (the error handler's job, [[How does an error handler consume from the Invalid Message Channel]]), and finally re-introduce once the sender or configuration problem is fixed. Product machinery supports each act. IBM MQ ships the dead-letter queue handler `runmqdlq`, which matches DLQ messages against a user-written rules table and forwards matched messages onward — the mechanism teams also adapt for backout-queue traffic, with the caveat that DLQ messages must carry `MQDLH` and the handler's forwarding authority is explicit. Azure Service Bus documents the drain pattern for its dead-letter sub-queue: a receiver on `<queue>/$deadletterqueue` inspects `DeadLetterReason` and `DeadLetterErrorDescription`, resubmits the message to the main queue, and completes the dead-lettered message so the sub-queue empties. Both flows keep the original payload; only the reason metadata distinguishes what happened — and only a *fixed* cause makes a resubmission succeed, which is the boundary against pointless redelivery in [[Why should you not retry a structurally invalid message]].

```text
Park -> inspect (reason/payload) -> fix cause -> resubmit -> complete/park-free
       \__ without the fix step, resubmit == poison loop again __/
```

**Listing 1.** Replay as a gate: the fix is the precondition, the resubmit is the action, the completion is the hygiene.

> [!warning] Replay is not a retry policy
> "Some systems can replay after a fix" is a DLQ-operations feature that dumps often import wholesale into the Invalid Message Channel concept. Two rules keep it honest: replay only payloads whose *cause* changed, and record the attempt — an unrepaired message that gets replayed lands right back in quarantine, but now with wasted cycles and confused history, the loop of [[What happens if a receiver puts an invalid message back on the original channel]]. When the destination is a shared dead-letter sub-queue, keep the role split of [[What is the difference between Invalid Message Channel and Dead Letter Channel]] visible in the reason codes.

> [!tip] Interview answer
> Replay means: diagnose the parked message, fix the sender or configuration problem, then resubmit the intact payload to its original destination and complete it off the quarantine — with tooling like IBM's rules-table DLQ handler or a Service Bus drain receiver on the dead-letter sub-queue. The precondition is the fix; replaying an unrepaired message is just the poison loop with extra steps.
