<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When designing a messaging system for applications to use, a channel-chapter dump says the administrator must define one or more Invalid Message Channels for the applications to use. Receivers then have a known destination to move improper messages to, instead of each endpoint inventing a private junk pile or dropping traffic.

The Invalid Message Channel is not used for normal, successful communication, so clutter there does not block the happy path. Applications still have to agree which invalid channel to use, the same way they agree on the working Datatype Channels at design or deployment time.
> [!warning] Unverified traps from the dump
> - Defining the queue is not the pattern; the receiver still has to move delivered-but-unprocessable messages there.
> - One shared invalid channel across unrelated contracts mixes triage; dumps allow more than one channel.
