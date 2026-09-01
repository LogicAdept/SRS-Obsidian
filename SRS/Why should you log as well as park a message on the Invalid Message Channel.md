<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A channel-chapter dump compares the Invalid Message Channel to an error log for messaging: when processing goes wrong, put the message on the invalid channel. If it will not be obvious to anyone browsing that channel why the message is invalid, the application should also log an error with more details.
> [!warning] Unverified traps from the dump
> - Parking without a reason or log line leaves a payload that cannot be triaged.
> - Treating the invalid channel as the only log and never alerting on it is the ignored-error-log failure the same dump warns about.
