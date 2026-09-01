<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A poison message is a delivery whose content always fails (bad payload, divide-by-zero data, unknown region). If the receiver catches the error and Abandons or lets the lock expire, the same message is received again forever unless a cap exists.

On AppFabric / Service Bus the receiver implements Invalid Message Channel by calling Deadletter after a validation check (for example unknown region) instead of waiting for MaxDeliveryCount. Optionally it retries a few times on DeliveryCount for transient faults, then dead-letters. Broker-side MaxDeliveryCount (default 10) is the safety net when the app keeps abandoning: the messaging system then uses Dead Letter Channel behavior.

A separate consumer on the dead-letter sub-queue inspects DeadLetterReason and completes the message so the entity does not fill up.
> [!warning] Unverified traps from the dump
> - Catch-and-abandon without a delivery cap is the poison loop; setting MaxDeliveryCount to int.MaxValue effectively disables that safety net.
> - Calling Abandon immediately retries; taking no action waits LockDuration, which can reorder processing.
