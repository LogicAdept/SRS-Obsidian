<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump titled what belongs in a DLQ / invalid-message queue answers from WebSphere MQ. Dead Letter Queue is where messages that could not be delivered to their destination go. Queue managers, message channel agents, and applications can put there. Every DLQ message must be prefixed with MQDLH. The queue manager or MCA adds that header; an application that puts to the DLQ must prefix MQDLH itself.

If the application received the message but cannot handle it (format not understood), that dump says put it on a BACKOUT queue, not the DLQ. BACKOUT is an ordinary per-queue destination for application-rejected messages and does not require MQDLH. A helper can read BACKOUT and route the message back to the target queue as-is. DLQ messages need the dead-letter header stripped first.
> [!warning] Unverified traps from the dump
> - Interview lists that say every unhandleable message belongs on the DLQ collapse delivery failure with receiver-invalid.
> - The same dump still says that if the app already knows it cannot process anything (database down), it should stop accepting rather than reject into BACKOUT in a loop.
