<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use it when a message can be delivered to the receiver but cannot be processed because of its contents, and you need a place for developers to inspect those payloads. Typical dump example: missing Authorization or Cookie headers that the receiver requires.

Do not use it for application errors raised while handling a well-formed message. Dumps that follow this split say messages on the invalid channel usually reflect a coding or configuration mistake in the sender or the messaging system, so they cannot usefully be retried until that mistake is fixed. The pattern is especially useful when many senders share one channel: a new sender that omits required headers shows up immediately on the invalid channel.
> [!warning] Unverified traps from the dump
> - The same dump says a message with an invalid field value should not go to the Invalid Message Channel, which conflicts with other lists that park schema and value failures there.
