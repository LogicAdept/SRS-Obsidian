<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #SRS

# Why should you not treat an application error as an invalid message

> [!abstract] Short answer
> Because the message is fine. A well-formed command that fails in the domain — delete a record that does not exist, debit an overdrawn account — is an application error: nothing about the payload violates the receiver's contract, so parking it on the Invalid Message Channel misleads everyone who later triages it.

## Drawing the seam inside the receiver

The distinction tracks the processing pipeline. While the receiver is **decoding and validating** — checking the datatype, parsing the body, validating against the schema, verifying required headers — a failure means the message itself is unusable, and the Invalid Message Channel is exactly the right destination; that catalog is [[What kinds of delivered messages does a receiver treat as invalid]]. Once decoding succeeded and the application is **operating on the extracted data**, failures belong to the business logic: the Command Message that says "delete record 42" is perfectly valid even when record 42 is gone, and it should be handled the way failed requests are normally handled — a reply carrying the error, a log, possibly a retry under business rules — not parked where triage looks for format problems. The Service Activator and the Messaging Gateway are the natural seam: what happens before the invocation they perform is messaging; what happens inside it is application. The endpoint patterns themselves are in [[What is the Service Activator pattern]] and [[What is the Messaging Gateway pattern]], and the command side of the example in [[What is the Command Message pattern]].

> [!warning] Configuration errors are not payload errors either
> Flows that park "missing outbound Authorization" on an InvalidMessages queue are folding an adapter or environment configuration failure into payload triage — the parked message will parse perfectly, sending investigators in the wrong direction. Invalid-message traffic reflects a problem **with the delivered message**; everything else needs its own channel (or at least its own reason codes).

The practical test: if replaying the identical message after fixing the *application or configuration* would succeed, the message was never invalid — validity being receiver-relative means the receiver's contract failed, not the business, as set out in [[How does validity of a message depend on the receiver]]. Messages that *are* structurally fine but get retried pointlessly belong to the opposite mistake described in [[What is the difference between the Retry Pattern and Invalid Message Channel]].

> [!tip] Interview answer
> An application error happens while processing an already-decoded, already-valid message — a command referencing a record that does not exist is the classic case. Parking it as an invalid message hides the real cause, because the quarantine is read as "something wrong with this payload". Validation and decode failures go to the invalid channel; business failures go through error replies, logging, and business-level retry.
