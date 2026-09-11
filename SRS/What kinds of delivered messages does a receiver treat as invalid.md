<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #Messaging #SRS

# What kinds of delivered messages does a receiver treat as invalid

> [!abstract] Short answer
> Anything the messaging system delivered but the receiver's contract rejects: a body that fails to parse or validate, content that is lexically fine but wrong for the receiver, missing or unexpected header fields the receiver requires, and a well-formed message that simply arrived on the wrong channel.

## The catalog of failure points

The Invalid Message Channel exists precisely because delivery success says nothing about processability. The book's channel chapter walks through the failure points in order: the **body** may raise parsing or lexical errors (broken XML, truncated bytes); the body may be lexically valid but **semantically wrong** for this receiver (it fails the agreed schema or DTD, or uses fields this endpoint never expects); the **headers** may be missing properties the receiver needs — a correlation identifier, a return address, message-sequence metadata — or carry values that make no sense; and the message may be a perfectly good message on the **wrong channel**, which the receiver cannot interpret even though the intended audience could have. Each of these is covered from a different angle in [[What happens when a message of the wrong type arrives on a Datatype Channel]] and [[How does validity of a message depend on the receiver]].

Header-contract failures deserve emphasis because the body looks fine: a request without its `JMSReplyTo` return address cannot be answered even though the payload parsed, so the receiver parks it as invalid — the reasoning is worked out in [[How does a Replier decide a request message is invalid]].

```text
Failure point        Example                         Broker's view
-------------------- ------------------------------- --------------
Body parsing         malformed JSON, broken XML      delivered OK
Body schema          XML valid-looking, fails DTD    delivered OK
Required header      no correlation id / reply-to    delivered OK
Wrong channel/type   byte payload on a text channel  delivered OK
```

**Listing 1.** Every row was already "delivered"; the receiver's contract is the thing that failed, which is why the rows belong on an invalid channel rather than in broker machinery.

> [!warning] Business-rule failure is a different bucket
> A message that parses, validates, and carries all required headers but then fails in the domain — the requested record does not exist, the account is overdrawn — is an **application error**, not an invalid message. Parking it would send triage looking for format problems that are not there; the boundary is drawn in [[Why should you not treat an application error as an invalid message]].

> [!tip] Interview answer
> Invalid means delivered-but-unprocessable: unparsable or schema-invalid bodies, missing required header fields such as correlation or reply-to, wrong payload type for the channel, and well-formed messages sent to the wrong channel. The broker did its job in all of these — the receiver's expectations are what failed, so the receiver, not the broker, parks the message.
