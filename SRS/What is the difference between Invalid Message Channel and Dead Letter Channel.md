<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

An Invalid Message Channel is for messages that the messaging system did deliver and a receiver did receive, but the receiver cannot process them (bad type, bad format, unexpected body or headers the application cares about). The receiver itself moves the message there.

A Dead Letter Channel is for messages the messaging system cannot deliver: expired TTL, misconfigured destination, no consumer in time. The broker evaluates headers and moves the message. To the receiver that handling looks automatic; invalid-message handling is application code.

Dead messages are typically parked on a local per-machine dead-letter queue so the move does not depend on the network. Invalid-message handling is designed by the application, including cases the broker does not treat as dead.
> [!warning] Unverified traps from the dump
> - Many interview dumps call every failure queue a Dead Letter Queue and put malformed payloads there, collapsing the two patterns.
> - On some brokers both patterns are implemented as one dead-letter sub-queue; the pattern split is who decided and why, not the physical destination name.
