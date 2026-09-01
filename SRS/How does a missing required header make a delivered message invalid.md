<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The messaging system can deliver a message whose body is fine and still leave the receiver unable to process it. Dumps of the pattern list missing header properties as invalid-message cases: a Correlation Identifier, Message Sequence identifiers, a Return Address, and similar fields the receiver expects.

The broker still delivered the message. The receiver cannot complete its contract without those properties, so it treats the message as invalid and moves it to the Invalid Message Channel rather than putting it back on the working channel or dropping it.
> [!warning] Unverified traps from the dump
> - A missing Return Address on a request is an invalid message even though the payload parsed.
> - Header-field checks are the receiver's job; dumps contrast this with Dead Letter Channel, where the messaging system evaluates its own delivery headers.
