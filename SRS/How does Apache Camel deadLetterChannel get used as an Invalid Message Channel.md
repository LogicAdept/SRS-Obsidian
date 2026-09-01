<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A Java Camel dump implements Invalid Message Channel by installing errorHandler(deadLetterChannel("jms:queue:invalid-message-queue")) and then throwing IllegalArgumentException from an otherwise clause when the body is null or header MessageType is not Valid. The invalid payload therefore lands on a Camel Dead Letter Channel endpoint whose queue is named like an invalid-message queue.

Related-pattern lists from the same glossary call Dead Letter Queue an alternative name for Invalid Message Channel and mention a Retry Pattern that retries failed messages before they are designated invalid.
> [!warning] Unverified traps from the dump
> - errorHandler(deadLetterChannel("jms:queue:invalid-message-queue")) is DLC machinery labeled as Invalid Message Channel.
> - Retry-before-invalid contradicts dumps that say a structurally invalid message should not be retried at all.
