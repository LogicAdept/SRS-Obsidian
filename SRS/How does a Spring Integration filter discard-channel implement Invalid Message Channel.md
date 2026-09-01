<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Java/Spring/Integration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A Spring Integration dump implements the quarantine with a filter. IntegrationFlow.from("orders.raw") filters OrderCommand so amount().signum() > 0, with discardChannel("orders.rejected"), then sends survivors to orders.validated.

It says decide explicitly whether rejected messages are discarded, routed, or treated as errors, and that a discard channel is safer than silent dropping when rejected messages matter operationally. An exercise on that page asserts rejected orders appear on the rejection channel.
> [!warning] Unverified traps from the dump
> - Filter discard-channel parks the original Message, not a MessagingException wrapped as ErrorMessage on errorChannel.
> - Some dumps still throw after the discard send when throwExceptionOnRejection is true, which is not a quiet invalid-message move.
