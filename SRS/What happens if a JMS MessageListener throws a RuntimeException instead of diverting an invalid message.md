<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

JMS dumps quote the spec: throwing RuntimeException from onMessage is a client programming error. A well-behaved listener should catch it and divert the message to an application-specific unprocessable-message destination (the Invalid Message Channel idea).

If the exception still escapes, behavior depends on acknowledgment mode. AUTO_ACKNOWLEDGE or DUPS_OK_ACKNOWLEDGE: the provider redelivers immediately; how many times before it gives up is provider-dependent; JMSRedelivered is set and JMSXDeliveryCount is incremented on redelivery. CLIENT_ACKNOWLEDGE: the next message is delivered; redelivery of the previous one needs a manual session recover. Transacted session: the next message is delivered; RuntimeException does not roll the session back by itself. Providers should flag listeners that throw as possibly malfunctioning.
> [!warning] Unverified traps from the dump
> - Throwing to force redelivery of a permanently bad payload is the poison loop; the spec path is catch-and-divert, not throw.
> - On a transacted session, dumps say you must roll back yourself if you want redelivery; an uncaught RuntimeException will not do it.
