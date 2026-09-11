<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# What is the JMS unprocessable message destination

> [!abstract] Short answer
> It is the Jakarta Messaging specification's name for the application-specific destination where a listener sends a message it received but cannot process — the spec's advice for what the Invalid Message Channel looks like in JMS terms. It is **application-defined**: the spec recommends diverting to it, it does not create it for you.

## What the specification actually says

The asynchronous-delivery section of the Jakarta Messaging specification states: it is possible for a listener to throw a `RuntimeException`, but that is considered a **client programming error**; well-behaved listeners should catch such exceptions and attempt to divert messages causing them to "some form of application-specific 'unprocessable message' destination". Two properties of that wording matter for interviews. It is a recommendation about listener behavior, not broker machinery — no provider creates the destination, and nothing routes to it automatically; and it is application-specific, meaning each system decides whether it is a dedicated queue (the book's example uses `jms/InvalidMessages`), a topic, or a topic-per-contract-family. The full pattern behind it is [[How does the Invalid Message Channel pattern work]].

The destination is the parking place, while the decision procedure that precedes it — type check, required headers such as a reply-to, format validation — is the receiver's contract logic, described in [[How does a Replier decide a request message is invalid]].

> [!warning] It is not the provider's dead-letter queue
> A product's dead-letter sub-queue exists for delivery-side failures the broker detects (expiry, delivery-count exhaustion). The spec's unprocessable destination is for messages the broker delivered successfully. Some products only expose a dead-letter sub-queue as a parking place, and an application can use it as a last resort — the mechanics and the mixing risks are in [[How do you implement Invalid Message Channel when the broker only has a dead-letter sub-queue]] — but the two roles must still be told apart, as in [[What is the difference between Invalid Message Channel and Dead Letter Channel]].

What actually happens when a listener ignores the advice and throws is session-mode-dependent and spelled out in [[What happens if a JMS MessageListener throws a RuntimeException instead of diverting an invalid message]].

> [!tip] Interview answer
> The JMS spec tells listeners that cannot process a message to catch the failure and divert it to an application-specific "unprocessable message" destination — that is the spec-level name of the Invalid Message Channel idea. The destination is defined and wired by the application, not by the provider, and it is distinct from the broker's own dead-letter queue.
