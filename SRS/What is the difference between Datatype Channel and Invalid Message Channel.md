<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DatatypeChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Datatype Channel is the idea that all data on a channel is the same type so the receiver already knows how to process it. That is why a messaging system needs many channels: if any type could travel on one pipe, two applications would need only one channel in each direction.

Invalid Message Channel is what the receiver does when that contract is broken after delivery. The broker may still transmit a byte message on a text channel, or XML that is not well formed or not valid for the agreed schema. The receiver cannot process it, so it moves the improper message to a special channel for messages that could not be processed. The working Datatype Channel stays a typed pipe; the invalid channel is the quarantine, not a second datatype.
> [!warning] Unverified traps from the dump
> - Putting mixed types on one channel and sorting them in the consumer is not Datatype Channel; the Invalid Message Channel then becomes a dumping ground.
> - The invalid channel is not itself a Datatype Channel for bad data in the happy-path sense; dumps say it is not used for successful communication.
