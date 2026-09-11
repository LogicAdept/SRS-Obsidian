<!--
reps: 0
priority: 0
-->
#Messaging #Patterns/Enterprise/Integration/SmartProxy #SRS

# What is the Smart Proxy pattern?

> [!abstract] Short answer
> A **Smart Proxy** tracks messages on a service whose replies go to the caller's **Return Address**: it intercepts requests, **stores the original reply address, replaces it with its own**, and when the service replies, forwards the reply — unmodified — back to the original address. The service never learns it is being watched.

## Owning the reply address is owning the conversation

Wire taps observe channels; they cannot observe a service whose replies are addressed per-request to whatever channel the caller wrote into the return address header. The smart proxy solves exactly that: it sits on the request channel, and for each incoming request it (1) stores the original return address keyed to this request, (2) rewrites the return address header to a channel the proxy listens on, and (3) passes the request on. The service replies "normally" — to the proxy. The proxy retrieves the stored original address and uses routing to forward the untouched reply there. To caller and service, nothing changed; in the middle, every request-reply pair is now observable — and interceptable. This is the request-reply-aware evolution of the [[What is the Wire Tap pattern]], built entirely from the mechanics of [[What is the Return Address pattern]] and [[What is the Correlation Identifier pattern]].

```d2
direction: down
c: "Caller\nreplyTo: caller.ch" {
  width: 190
  height: 60
  style.fill: "#e3f2fd"
}
px: "Smart Proxy\nstore caller.ch\nrewrite to proxy.ch" {
  width: 240
  height: 75
  style.fill: "#fff3e0"
}
s: "Service\nreplies to replyTo" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
pr: "proxy.ch\nreply arrives" {
  width: 170
  height: 55
  style.fill: "#fff3e0"
}
c -> px -> s -> pr -> c: "forward reply,\nunmodified"```

**Fig. 1.** The rewrite is invisible at both ends; the proxy sees every pair and forwards faithfully.

## The proxy's ledger

```text
Step    Header state                  Proxy action
------  ----------------------------  -------------------------------
1       replyTo = caller.ch           store (corrId -> caller.ch)
2       replyTo = proxy.ch            forward request to service
3       reply arrives on proxy.ch     look up stored address
4       replyTo = caller.ch           forward unmodified reply
```

**Listing 1.** The whole pattern is a small key-value ledger plus one header rewrite — and a TTL on the ledger for requests that never get replies.

> [!warning] The proxy holds per-request state in a distributed system
> If the proxy restarts, stored return addresses vanish — replies from the service become orphans with nowhere to go, so the ledger needs durable storage or an explicit "drop and alert" policy. And because it terminates replies, the proxy adds a hop of latency and a failure domain exactly in the middle of every conversation it observes.

> [!tip] Interview answer
> A Smart Proxy makes request-reply traffic observable when replies are addressed per request: it intercepts requests, stores the original return address, rewrites the header to itself, and forwards replies back to the original address unmodified. Both sides are unaware. The cost is per-request state that must survive restarts, plus an extra hop in every proxied conversation.
