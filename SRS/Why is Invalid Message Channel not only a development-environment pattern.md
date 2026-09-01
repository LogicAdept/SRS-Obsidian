<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A CPI dump's worked example parks a missing outbound Authorization on a JMS queue named InvalidMessages, which can look like a development-only trick in a tiered environment. The same dump says the ideal would be to use the pattern only in development, then immediately contradicts that: the pattern is more useful where multiple senders share one channel. When a new sender is added, developers monitor the invalid channel to catch common issues such as missing authorizations.

It also says more helpful error identifiers can be coded with XML Validator, EDI Validator, or custom checks such as body length or required headers. Messages on that channel are described as delivered successfully but unprocessable because of contents, usually a coding or configuration issue that cannot be retried until it is fixed.
> [!warning] Unverified traps from the dump
> - The same dump parks missing adapter Authorization as InvalidMessages, which other notes would call an application or adapter-config error.
> - That dump also says an invalid field value should not go to the Invalid Message Channel, which conflicts with lists that park schema and value failures there.
