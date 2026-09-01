<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A pattern glossary lists Retry Pattern as a related design: retry failed messages before they are designated invalid. Camel dumps in the same family install errorHandler(deadLetterChannel(...)) and retry before the payload is named invalid.

Channel-chapter and CPI dumps split the other way. A structurally invalid message (wrong type, missing required headers, schema that will not parse) fails the same check on every redelivery; they say move it to the Invalid Message Channel and do not retry until the sender or contract is fixed. Transient failures (timeout, connection blip) are not invalid messages and can succeed later. CPI adds that messages on the invalid channel usually reflect a coding or configuration issue, so they cannot usefully be retried.
> [!warning] Unverified traps from the dump
> - Retry-before-invalid is Dead Letter / poison-handling advice labeled as Invalid Message Channel.
> - Glossaries that list Dead Letter Queue as an alternative name for Invalid Message Channel import retry policy from the DLQ side.
