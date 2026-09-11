<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Messaging Gateway pattern?

> [!abstract] Short answer
> A **Messaging Gateway** is a class that **wraps messaging-specific calls** behind **domain-specific methods**: application code calls `getCreditScore(customer)` instead of building messages, setting properties, and sending to channels — only the gateway knows messaging is involved.

## A facade between domain code and middleware

The gateway encapsulates the messaging code — constructing messages, setting headers, choosing channels, correlating replies — and exposes business functions with strongly typed parameters, exactly like any other method. The application reads `getCreditScore`, not `Message.MessageReadPropertyFilter.AppSpecific`. It is the messaging-specific version of the general Gateway pattern from Fowler's EAA: an interface that hides a technology boundary. In Spring Integration this is an interface with a `@MessagingGateway` annotation and proxy implementation; the gateway can hide synchronous-looking calls that are actually async request-reply, which makes it the natural home for [[What is the Request-Reply pattern]] plumbing alongside [[What is the Correlation Identifier pattern]] bookkeeping. Compared with the [[What is the Message Endpoint pattern]], a gateway is the application-facing refinement; compared with the [[What is the Channel Adapter pattern]], it serves apps that already live in the same codebase rather than foreign systems.

```d2
direction: right
app: "Application\ncreditService.getScore(c)" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
gw: "Messaging Gateway\nmethod -> message -> channel" {
  width: 240
  height: 75
  style.fill: "#fff3e0"
}
ms: "Messaging system" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
app -> gw -> ms```

**Fig. 1.** Domain code calls a method; only the gateway knows a message was sent.

## Facade in code

```java
@MessagingGateway(defaultRequestChannel = "credit.requests")
public interface CreditGateway {
    @Gateway(replyTimeout = 2000)
    int getCreditScore(String customerId);
}
// application: gateway.getCreditScore("C-77")  -- messaging invisible
```

**Listing 1.** The interface declares the domain operation; the generated implementation does the message building, sending, and reply correlation.

> [!warning] Gateways hide asynchrony, and hidden asynchrony surprises
> A synchronous-looking gateway method that times out throws where the caller cannot distinguish "slow" from "broken" from "never will answer". Make timeouts, error channels, and async variants explicit configuration, not defaults nobody reviews — otherwise the first broker hiccup surfaces as mysterious latency inside ordinary business code.

> [!tip] Interview answer
> A Messaging Gateway wraps all messaging-specific code behind a domain-facing interface: application methods like getCreditScore, internally message construction, channel selection, and reply correlation. It is the messaging flavor of the Gateway facade pattern; Spring Integration's annotated gateway interfaces are the standard example. The design duty is managing hidden asynchrony — timeouts and error paths must be explicit.
