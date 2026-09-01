<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Pattern glossaries and some interview lists treat Invalid Message Channel, Dead Letter Channel, Error Channel, and Dead Letter Queue as aliases. They are not. Invalid Message Channel is the receiver parking a delivered message it cannot understand. Dead Letter Queue / Dead Letter Channel is the messaging system's place for messages it cannot deliver (expiry, max delivery count, unroutable).

A CLIMB-style EIP interview answer that says Dead Letter Queues store malformed messages or misconfigured consumers is describing both problems with one name. Camel's errorHandler(deadLetterChannel(...)) is an error handler after failed processing, which is closer to DLC than to the receiver's invalid-message move.
> [!warning] Unverified traps from the dump
> - Software pattern lexicons list Dead Letter Channel and Dead Letter Queue under Also Known As for Invalid Message Channel.
> - Advent-of-EIP style posts dump malformed JSON, poison messages, TTL expiry, and unroutable traffic into one DLQ labeled Invalid Message Channel.
