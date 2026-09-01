<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The same Advent dump's invalid_message helpers inspect DLQ stats and replay_all messages from a DLQ back onto their original exchanges. It lists retry capability and fix-and-replay as characteristics of the Invalid Message Channel it equates with a DLQ.

A TypeScript DIY in that dump stores failed items with error text and attempts so they can be inspected or replayed later. The stated pattern is: try to process, catch failures, route to a separate channel, then review and replay.
> [!warning] Unverified traps from the dump
> - Replaying a structurally invalid payload onto the original channel recreates the poison loop the pattern is meant to stop.
> - Replay is a Dead Letter Queue operational feature; dumps that equate Invalid Message Channel with a DLQ import it.
