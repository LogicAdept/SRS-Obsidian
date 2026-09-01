<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump: it is the sender's responsibility to make sure that a message it sends on a channel will be considered valid by that channel's receivers. If it does not, the receivers ignore the sender by rerouting those messages to the Invalid Message Channel.

A message that is valid for one receiver on a channel should be valid for every other receiver on that channel. If one receiver treats it as invalid, the others should as well. Two receivers with different contracts should not share the channel.
> [!warning] Unverified traps from the dump
> - Being ignored this way is not a business NAK; it is the receivers refusing to process traffic that breaks the channel contract.
> - The happy path stays clear only if invalid traffic is moved off the working channel, not left there to be reconsumed.
