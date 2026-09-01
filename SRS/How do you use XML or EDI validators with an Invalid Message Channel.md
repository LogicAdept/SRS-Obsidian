<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A CPI dump stores invalid messages on a JMS queue named InvalidMessages for developers to inspect. An Exception Subprocess on failure puts the incoming message there with a JMS receiver adapter. The example that fails because Authorization or Cookie headers are missing is the candidate they send to that queue.

The same dump says more useful error identifiers can be coded with an XML Validator, an EDI Validator, or custom checks (body length, required headers). It rates the pattern on being able to create the invalid channel, not on how good the identification is, even while noting that XML and EDI validators are available for validation.
> [!warning] Unverified traps from the dump
> - That dump also says a message with an invalid field value should not go to the Invalid Message Channel, which conflicts with lists that park schema and value failures there.
> - The worked example parks a missing outbound Authorization as InvalidMessages, which other notes would call an application or adapter-config error rather than an invalid message.
