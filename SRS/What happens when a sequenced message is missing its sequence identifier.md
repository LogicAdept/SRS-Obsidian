<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Messaging #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Message Sequence dumps split a large payload into ordered parts. Each part needs a sequence identifier (which sequence it belongs to), a position identifier, and a size or end indicator.

If a message that is supposed to be part of such a group arrives without the sequence id or another required sequence field, the receiver treats it as illegal and moves it to the Invalid Message Channel. The messaging system may have delivered it; the receiver still cannot reassemble the group.
> [!warning] Unverified traps from the dump
> - Missing sequence metadata is an invalid-message case, not automatically a Dead Letter Channel case.
> - Those notes also say Message Sequence on one channel does not mix well with Competing Consumers or a Message Dispatcher.
