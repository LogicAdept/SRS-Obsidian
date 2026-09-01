<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A message can be invalid because required values are missing, values are the wrong type, the structure is not the agreed schema, or the type does not belong on that channel. Retrying processing will keep failing the same validations. There is no point in redelivery; the receiver should move the message to an Invalid Message Channel so it is not lost and the main flow is not blocked.

Transient failures (downstream timeout, connection blip) are the opposite case: those can succeed on a later attempt and should not be classified as invalid messages.
> [!warning] Unverified traps from the dump
> - Dumps that equate Invalid Message Channel with a Dead Letter Queue often still recommend retries before parking, which is DLC/poison-handling, not format validation.
