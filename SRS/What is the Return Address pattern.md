<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration #SRS

# What is the Return Address pattern?

> [!abstract] Short answer
> A **Return Address** is a header field on the request message that says **where the reply should be sent**. The replier reads it and publishes the reply there — it never hardcodes a reply destination and never guesses.

## The reply address travels with the request

Without a return address, a replier must be configured with reply channels — one fixed destination, or worse, per-caller knowledge baked into the replier. Putting the address in the request header encapsulates the request/reply channel decisions inside the requestor: different messages to the same replier can demand replies in different places, and the replier stays generic. Because the return address is infrastructure control data, it belongs in the **header**, not in the body — the replier's business code should not see it. JMS expresses it as `JMSReplyTo`; AMQP 0-9-1 as the `reply_to` property. A hidden bonus: a middleware component can rewrite the field to intercept replies, which is exactly how the [[What is the Smart Proxy pattern]] taps a service; combined with [[What is the Correlation Identifier pattern]] it completes [[What is the Request-Reply pattern]].

```d2
direction: right
req: "Requestor\nsets ReplyTo" {
  width: 190
  height: 65
  style.fill: "#e3f2fd"
}
rq: "Request channel\nheader: ReplyTo=reply.q" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
rep: "Replier\ngeneric, reads header" {
  width: 200
  height: 65
  style.fill: "#e8f5e9"
}
rpl: "Reply channel\nreply.q" {
  width: 190
  height: 60
  style.fill: "#fff3e0"
}
req -> rq -> rep -> rpl```

**Fig. 1.** The replier learns the destination from the message, not from configuration.

## The replier stays generic

```java
// No configuration: wherever the request says, the reply goes
Destination replyTo = request.getJMSReplyTo();
if (replyTo == null) { /* decide: drop, log, or default */ }
reply.setJMSCorrelationID(request.getJMSMessageID());
producer.send(replyTo, reply);
```

**Listing 1.** The replier reads `JMSReplyTo` per request; missing addresses are an explicit branch, not an exception at send time.

> [!warning] Missing and rewritten return addresses are normal failure modes
> A request without a return address will "succeed" at the replier and the reply silently vanishes — validate the field up front. And because any middleware hop can rewrite the address, debugging "where did my reply go" starts by diffing the header end to end; assume nothing about who rewrote it.

> [!tip] Interview answer
> Return Address puts the reply destination in a request header field — JMSReplyTo in JMS, reply_to in AMQP — so the replier answers wherever the requestor asked, without knowing or caring who it is. It keeps reply topology in the requestor's hands, lets different requests target different reply channels, and it is the hook that proxies use to intercept replies.
