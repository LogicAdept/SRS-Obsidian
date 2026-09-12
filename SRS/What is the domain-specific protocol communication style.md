<!--
reps: 0
priority: 0
-->
#Patterns/Architecture/Microservices/CommunicationStyles #SRS

# What is the domain-specific protocol communication style

> [!abstract] Short answer
> Domain-specific protocol: when services need to speak a protocol purpose-built for the domain - email via SMTP/IMAP, media streaming via RTMP, HLS - let them use it directly instead of flattening everything onto generic HTTP RPC or messaging. The third communication-style option, sitting beside RPI and messaging; niche, but the correct answer whenever the domain has a standardized protocol with semantics that generic transports would lose.

## Mechanism: pick the protocol the domain already standardized

Some interactions are not new designs - they are integrations with an ecosystem that standardized long before microservices did. A notification service talking to mail infrastructure speaks SMTP; a client fetching mail speaks IMAP; a media pipeline delivering a stream speaks RTMP or HLS. Forcing those flows through JSON-over-HTTP means re-implementing the protocol's semantics - delivery semantics, session state, encoding - badly, on top of a generic transport. The pattern's contribution is permission and framing: inter-service communication styles are a portfolio, not a monoculture; alongside [[What is the remote procedure invocation pattern between microservices]] for synchronous request/response and [[What is the messaging communication style between microservices]] for asynchronous channel-based exchange, a service may natively speak the protocol its domain requires. The cost is exactly what the other two styles avoid: the protocol's client and server machinery must be built, secured, monitored and versioned by you, and the service boundary now leaks a wire-level contract - other services coupling to it inherit that protocol's complexity.

```d2
direction: right
nsvc: "Notification service" {style.fill: "#e8f5e9"}
smtp: "Mail infrastructure
SMTP" {style.fill: "#eceff1"}
menc: "Media encoding service" {style.fill: "#e8f5e9"}
rtmp: "Streaming edge
RTMP / HLS" {style.fill: "#eceff1"}
api: "Other services
REST / messaging" {style.fill: "#fff3e0"}
nsvc -> smtp: native protocol
menc -> rtmp: native protocol
api -> nsvc: generic style in
api -> menc: generic style in
```

**Fig. 1.** Generic styles enter the service boundary; the domain-native protocol is used where the domain has standardized one - not imposed on every edge.

## Where it fits and where it does not

Honest framing for an interview: this is the rarest of the three styles, and its value is recognizing when a domain protocol is the right tool rather than dogmatically standardizing on HTTP. Realistic cases: a service that is essentially an SMTP relay with business logic, chat or IoT services speaking MQTT to constrained devices, streaming services speaking HLS to players. What it is not: a license for bespoke one-off binary protocols between two internal services - that is accidental reinvention of transport concerns (framing, retries, versioning) that RPI and messaging already solved, with no ecosystem to inherit. The decision heuristic: does the protocol standardize semantics beyond transport that your flow genuinely needs (mail delivery semantics, streaming session semantics, pub/sub for constrained devices)? If yes, adopt it at the edge that needs it; if no, stay with the generic styles and their tooling.

> [!warning] A protocol boundary is a hard dependency
> Exposing a domain protocol inside the estate couples consumers to its wire format and failure modes: no HTTP status conventions, no JSON tooling, monitoring stacks that need custom probes, and a harder time when the protocol version must move. Contain it: prefer the pattern at the edge - where your service meets the outside ecosystem - and keep internal service-to-service traffic on generic styles unless the domain demand is real. Second trap: assuming the protocol's security story - SMTP or RTMP do not bring OAuth-style authorization; identity decisions still belong in your gateway and services.

> [!tip] Interview answer
> There are three communication styles: RPI, messaging, and domain-specific protocol - using the protocol the domain standardized, like SMTP for mail or HLS/RTMP for streaming, instead of flattening everything onto HTTP or a broker. I reach for it at the edge where those semantics genuinely matter, because it costs custom infrastructure, monitoring and security work. Internal service-to-service traffic usually stays on generic styles - this is the special case, not the default.
