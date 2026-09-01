<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Message Expiration dumps split two handlers. If the messaging system sees that a message is already expired, it may drop it or move it to a Dead Letter Channel. Time-zone skew is called out: the messaging system is supposed to normalize time for that comparison.

If a receiver actually receives a message it then treats as expired, those notes send it to the Invalid Message Channel instead. On a Publish-Subscribe Channel each subscriber has its own copy, so one subscriber deciding the copy is expired does not force that decision on the others.
> [!warning] Unverified traps from the dump
> - Broker-side expiry is Dead Letter Channel behavior; receiver-side expiry after delivery is Invalid Message Channel behavior in those notes.
> - The same notes say setting expiration on a reply in Request-Reply is usually pointless because the sender wants to know the request arrived promptly.
