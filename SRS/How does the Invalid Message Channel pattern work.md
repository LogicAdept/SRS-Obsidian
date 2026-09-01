<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When a receiver cannot process a delivered message (wrong datatype or format, malformed XML, payload that fails the agreed schema), it must not leave that message on the input channel and must not drop it silently. It moves the improper message to an Invalid Message Channel: a dedicated channel for messages the receivers could not process.

The administrator defines one or more such channels. They are not used for successful traffic, so they can hold junk without hurting the happy path. An error handler subscribes to the invalid channel to inspect those messages as they arrive. If the reason the message is invalid will not be obvious from the payload alone, the receiver should also log details.

JMS describes the same idea: a well-behaved MessageListener that cannot process a message should divert it to an application-specific unprocessable-message destination.
> [!warning] Unverified traps from the dump
> - Validity is not a property of the message itself; it is the receiver's expectations that make a payload invalid.
> - A byte message on a text Datatype Channel is an invalid message even though the broker delivered it successfully.
