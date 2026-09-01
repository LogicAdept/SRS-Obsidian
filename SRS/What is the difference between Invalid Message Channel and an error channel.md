<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Java/Spring/Integration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pattern glossaries list Error Channel, Dead Letter Channel, and Dead Letter Queue as also-known-as names for Invalid Message Channel. They are not the same destination contract.

Invalid Message Channel is the receiver parking a delivered message whose type, format, or expected headers it cannot process; the payload on that channel is the improper message. Spring Integration errorChannel is a different dump: on asynchronous handling the exception is wrapped as a MessagingException / ErrorMessage and published to errorChannel (or an errorChannel header), defaulting to a publish-subscribe channel with a logging subscriber. One Spring dump then uses ErrorMessageExceptionTypeRouter to map InvalidOrderException onto a channel named invalidChannel, which is a later split, not the original payload move.
> [!warning] Unverified traps from the dump
> - An ErrorMessage payload is the exception, not the original invalid body; triage that expects the raw message will not find it without failedMessage.
> - Synchronous DirectChannel dumps propagate the exception to the caller instead of publishing to errorChannel.
