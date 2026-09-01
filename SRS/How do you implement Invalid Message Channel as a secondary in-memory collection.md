<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Patterns/Enterprise/Integration/Channels/DeadLetterChannel #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The same Advent dump's build-it-yourself TypeScript sketch uses two arrays: mainQueue for Event values and deadLetterQueue for DeadLetter records that keep the event, an error string, and an attempt count. enqueue pushes onto the main collection. process shifts each event, runs a handler, and on throw pushes {event, error, attempts: 1} onto the dead-letter array instead of dropping it.

The handler throws on empty data, so a mix of valid and empty payloads leaves the empty one on the secondary collection for later inspect or replay. The dump's claim is that the semantics are the same whether the second channel is an in-memory array, a database table, or a broker dead-letter exchange: try to process, catch failures, route to a separate channel.
> [!warning] Unverified traps from the dump
> - An in-memory second array has no broker delivery semantics; it is a teaching stand-in for the quarantine role.
> - Catching every throw and parking it collapses application errors into the same collection as structurally invalid payloads.
