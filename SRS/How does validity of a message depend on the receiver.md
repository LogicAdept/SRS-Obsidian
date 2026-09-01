<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A message is neither inherently valid nor invalid. The receiver's context and expectations decide. A payload that is valid for one receiver may be invalid for another; those two receivers should not share a channel. If a message is valid for one receiver on a channel, it should be valid for every other receiver on that channel. If one receiver treats it as invalid, the others should as well.

It is the sender's job to publish something every receiver on that channel will accept. Otherwise receivers will ignore the sender by rerouting those messages to the Invalid Message Channel.
> [!warning] Unverified traps from the dump
> - Sharing one channel across receivers with different contracts turns the Invalid Message Channel into a dumping ground for messages that are valid for someone else.
