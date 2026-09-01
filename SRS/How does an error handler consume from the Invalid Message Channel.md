<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump: the administrator defines one or more Invalid Message Channels. They are not used for successful communication, so they can hold improper messages without hurting the happy path. An error handler that wants to diagnose those messages uses a receiver on the invalid channel and detects them as they become available.

The same dump compares that consumer to a utility monitoring an error log: pick up the strange message and figure out what to do with it. Ideally the process would consume invalid messages, determine the cause, and fix the underlying problem. Often the cause is a coding or configuration error that needs a developer or analyst. At minimum, watch the channel and alert when it contains messages.
> [!warning] Unverified traps from the dump
> - A channel nobody consumes is as useful as an error log nobody reads.
> - The error handler on the invalid channel is not the working-path receiver; it is a separate subscriber for triage.
