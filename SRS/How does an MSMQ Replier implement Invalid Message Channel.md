<!--
reps: 0
priority: 0
-->
#Patterns/Enterprise/Integration/Channels/InvalidMessageChannel #ProgrammingLanguages/CSharp #SRS

# How does an MSMQ Replier implement Invalid Message Channel

> [!abstract] Short answer
> The book's .NET Request-Reply example wires three queues — `RequestQueue`, `ReplyQueue`, `InvalidQueue`. The Replier receives asynchronously, and on any processing failure it stamps the request's `Id` onto `CorrelationId` and sends the request to `InvalidQueue` — the Invalid Message Channel role in MSMQ terms.

## The failure path in the official example

The Replier is an Event-Driven Consumer: it calls `BeginReceive` and handles `ReceiveCompleted`, reading the body through `XmlMessageFormatter`, taking `ResponseQueue` as the return address, and replying with `CorrelationId` set to the request's `Id`. The whole handler body sits inside a `try`; the `catch (Exception)` branch prints "Invalid message detected", copies `requestMessage.CorrelationId = requestMessage.Id`, and calls `invalidQueue.Send(requestMessage)`. The demonstration partner, an `InvalidMessenger`, sends a message whose body type the Replier cannot recognize (a binary body on a channel formatted for XML), so delivery succeeds but interpretation fails — the same delivered-but-unprocessable trigger as the JMS version in [[How does a Replier decide a request message is invalid]].

The correlation stamp relies on the MSMQ definition of the property: `Message.CorrelationId` is the identifier used by acknowledgment, report, and response messages to reference the original message. Sending to `InvalidQueue` creates a **new** message with a new `Id`, so the copy is what keeps the original identity traceable — the same provider-assigns-id logic as [[How do you preserve the original Message ID when parking an invalid JMS message]].

```text
Replier.OnReceiveCompleted           (Conceptual, book example shape)
  try:    read Body via XmlMessageFormatter
          reply to ResponseQueue with CorrelationId = request.Id
  catch:  print "Invalid message detected"
          request.CorrelationId = request.Id
          invalidQueue.Send(request)      // park, then BeginReceive again
```

**Listing 1.** The try/catch *is* the validity check in this example: any exception the formatter or handler throws diverts the request to the invalid queue.

> [!warning] The catch is broader than "invalid message"
> In the example, every exception — not only a wrong body type — lands on `InvalidQueue`, which folds transport hiccups into payload triage. A stricter receiver distinguishes decode/validation failures from processing failures, the boundary explained in [[Why should you not treat an application error as an invalid message]].

> [!tip] Interview answer
> The MSMQ Replier implements the pattern with three queues and a try/catch: the request is processed under the expected formatter, and any failure — deliberately, in the example, a binary body on an XML channel — sends the request to `InvalidQueue` with `CorrelationId` set to the original `Id`, so the parked copy still references the request that failed. It is the .NET twin of the JMS example.
