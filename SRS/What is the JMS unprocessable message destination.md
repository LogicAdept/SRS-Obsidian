<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump quotes the JMS specification: if a MessageListener gets a message it cannot process, a well-behaved listener should divert the message to some form of application-specific unprocessable message destination. That destination is an Invalid Message Channel.

The dump contrasts this with throwing RuntimeException from onMessage, which JMS treats as a client programming error. The listener should catch the failure and move the payload to the application-defined unprocessable destination instead of failing the callback.
> [!warning] Unverified traps from the dump
> - Unprocessable message destination is an application queue, not the broker's dead-letter sub-queue, unless the product only offers that one parking place.
> - The JMS wording is a suggestion for a well-behaved listener; the broker does not invent the invalid channel for you.
