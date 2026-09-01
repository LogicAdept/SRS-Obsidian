<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In a stock-trading dump, the executing application treats as invalid a request that is the wrong type (a price quote on the trade channel), a trade that does not specify the security or share count, or a trade that does not say where to send the confirmation. Once it determines the message is invalid, it resends onto the Invalid Message Channel.

The various applications that send trade requests may wish to monitor that channel to determine if their requests are being discarded.
> [!warning] Unverified traps from the dump
> - Sender-side monitoring is not a substitute for an operator alert whenever the channel contains messages.
> - A discarded request on the invalid channel is not a business NAK; dumps still treat domain failures as application errors, not invalid messages.
