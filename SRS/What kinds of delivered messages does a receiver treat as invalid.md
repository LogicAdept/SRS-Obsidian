<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump: everything on a Message Channel is just a message, but a receiver can process it only if it can interpret the data and understand its meaning. That is not always possible. The body may cause parsing errors, lexical errors, or validation errors. The header may be missing needed properties, or the property values may not make sense. A sender might put a perfectly good message on the wrong channel. A malicious sender could send an incorrect message on purpose. The receiver therefore needs some other way to handle messages it does not consider valid.

A Message Channel should be a Datatype Channel. If the sender puts the wrong datatype on it, the messaging system still transmits the message successfully; the receiver will not recognize it. Examples in the same dump: a byte message on a channel that is supposed to contain text, and XML that is not well formed or not valid for the agreed DTD or schema. Those messages are fine as far as the broker is concerned. They are invalid for the receiver, so it moves them to an Invalid Message Channel.
> [!warning] Unverified traps from the dump
> - Delivery success does not mean the payload is processable; dumps treat type, format, and header-contract failures as invalid-message cases after delivery.
> - A well-formed message on the wrong channel is still invalid for the receiver that actually got it.
