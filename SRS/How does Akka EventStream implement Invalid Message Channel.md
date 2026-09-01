<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A pattern glossary implements Invalid Message Channel with Akka EventStream. ProcessingActor handles Message(body, "Valid") by processing it. Any other messageType is published as InvalidMessage(body) on context.system.eventStream.

InvalidMessageHandlerActor subscribes to InvalidMessage and handles it off the main processing path. The sequence dump shows the processor publishing InvalidMessage and the handler acknowledging, rather than crashing the processor or dropping the payload.
> [!warning] Unverified traps from the dump
> - EventStream is an in-process pub-sub bus labeled as the invalid channel, not a broker destination.
> - The same glossary still lists Dead Letter Channel as Also Known As for Invalid Message Channel.
