<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/Messages #SRS

# What is the Command Message pattern?

> [!abstract] Short answer
> A **Command Message** is a regular message whose body **tells the receiver to invoke a specific operation** — messaging's replacement for RPC. The receiver parses the command and executes it; the sender cares that it happens, not where.

## A regular message carrying an imperative

There is no dedicated infrastructure type for commands: any message can be a command — a JMS `ObjectMessage` holding a `Serializable` command object, a `TextMessage` holding the command in XML or JSON, a .NET message with a command stored in it; a SOAP request is a command message in this sense. What makes it a command is semantics: the body names an operation and its parameters, and the receiving endpoint knows how to dispatch it. This gives you reliable, buffered invocation — the request survives a receiver outage — at the price of hand-rolling dispatch and reply handling, which is where [[What is the Request-Reply pattern]], [[What is the Return Address pattern]], and [[What is the Correlation Identifier pattern]] come in. Commands differ from documents and events in timing and intent; the contrast is spelled out in [[What is the difference between a command and an event]].

```d2
direction: right
req: "Requestor" {
  width: 160
  height: 55
  style.fill: "#e3f2fd"
}
ch: "Command channel\n(commands only)" {
  width: 210
  height: 65
  style.fill: "#fff3e0"
}
rec: "Receiver\ndispatch: cmd.name" {
  width: 200
  height: 65
  style.fill: "#e8f5e9"
}
op: "ShipOrder(orderId)" {
  width: 200
  height: 55
  style.fill: "#e8f5e9"
}
req -> ch -> rec -> op```

**Fig. 1.** The command channel carries imperatives; the receiver dispatches by the command name in the body.

## Dispatch shape

```java
public void onMessage(Message m) throws Exception {
    Command cmd = mapper.readValue(((TextMessage) m).getText(), Command.class);
    switch (cmd.name()) {
        case "ShipOrder"  -> shipping.ship(cmd.orderId());
        case "CancelOrder" -> shipping.cancel(cmd.orderId());
        default -> { /* unknown command: quarantine, do not crash */ }
    }
}
```

**Listing 1.** The receiver owns command dispatch; unknown commands should be parked for humans rather than rejected into a redelivery storm.

> [!warning] A command is not an event with a verb in its name
> `OrderShippedCommand` published on a broadcast channel means every subscriber now "owes" an execution — command semantics on pub/sub produce duplicate or meaningless executions. Commands go to the endpoint that owns the operation (point-to-point); if you find yourself broadcasting them, you actually wanted an [[What is the Event Message pattern]] or a [[What is the Publish-Subscribe Channel pattern]] redesign.

> [!tip] Interview answer
> A Command Message wraps an invocation request in a normal message: the body names the operation and its parameters, and the receiver dispatches it — messaging instead of synchronous RPC. There is no special broker type; it is semantics, not plumbing. Commands belong on point-to-point channels to exactly the service that owns the operation, and they pair with Return Address and Correlation Identifier when a reply is needed.
