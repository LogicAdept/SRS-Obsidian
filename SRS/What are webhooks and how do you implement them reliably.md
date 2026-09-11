<!--
reps: 0
priority: 0
-->
#API/Webhooks #SRS

# What are webhooks and how do you implement them reliably

> [!abstract] Short answer
> A webhook is reverse API traffic: the provider POSTs an event to a consumer-registered HTTPS URL when something happens. Reliable implementation is consumer work mostly — verify an HMAC signature, deduplicate by event id because delivery is at-least-once, acknowledge with 2xx fast and process asynchronously — and provider work — retries with backoff, signed payloads, replay tooling.

## The delivery contract

Registration binds one URL to one event set; the payload is a self-describing event (id, type, timestamp, data). Delivery is at-least-once by design: networks and consumer outages guarantee retries (with backoff, over hours in serious providers), so the consumer MUST deduplicate — persist the event id and treat a redelivery as a no-op success — the Idempotent Receiver pattern wearing HTTP clothes ([[What is the Idempotent Receiver pattern]], [[What is idempotency in HTTP and in messaging]]). Acknowledge fast: validate and enqueue within seconds, then return 200/202; long processing inside the handler trips provider timeouts and turns success into retry storms. Security is non-negotiable: the URL is a bearer credential (unguessable, often with a secret), and every delivery must be authenticated by an HMAC signature over the raw body — verify with a constant-time comparison — ideally with a timestamp inside the signed material so replays die ([[What is the difference between authentication and authorization]]-adjacent machinery lives in Security cards; the demo shows the mechanics). Expect signature rotation (providers publish old and new secrets during rotation) and payload-version headers.

```text
== valid delivery ==
receiver: sig ok, event evt_1 processed -> 200
== tampered payload (sig does not match) ==
receiver: BAD signature -> 400
== redelivery of the same event after network timeout ==
receiver: duplicate event -> 200 (idempotent no-op)
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver + javax.crypto.Mac): HMAC-SHA256 over the raw body with a constant-time compare, rejection of tampering, and event-id dedupe making redelivery harmless (out/A13_WebhookHmac.txt).

```d2
p: provider
q: event queue
c: consumer endpoint
reg: registration (URL + secret)
p -> q: event occurs
q -> c: POST + X-Signature (HMAC)
+ X-Event-Id
c -> c: verify sig (constant-time)
dedupe event id
c -> q: 202 fast, process async
q -> c: retry with backoff
(until 2xx or policy)
```

**Fig. 1.** The loop: signed POST, fast 2xx, async processing; failures on the provider side become retries the consumer must absorb idempotently.

## The operational checklist

Consumer side: TLS-only endpoint, signature verification before parsing, event-id dedupe store with retention, async processing with its own retries and a dead-letter path for poison events ([[What is the difference between a BACKOUT queue and a Dead Letter Queue for unprocessable messages]] for that discipline), monitoring delivery lag (the provider dashboard or a replay API). Provider side: retries with exponential backoff and a give-up policy, signed payloads with timestamps, idempotency of the events themselves, a replay mechanism, and honest docs of the delivery guarantees. Polling is the alternative: webhooks trade consumer-side polling infrastructure for provider-side delivery infrastructure, and win when events are sparse; SSE or WebSocket streams solve the same push problem for interactive clients ([[How do GraphQL subscriptions work over WebSockets]] for the in-band cousin; [[What are the four kinds of gRPC RPCs]] for the streaming option).

> [!warning] Responding 200 before processing is the contract — not before verifying
> Fast-ack means enqueue-then-200; it never means skip signature verification to save latency. An unverified webhook is a command injection endpoint into your business logic with extra steps.

> [!tip] Interview answer
> Webhooks reverse the call direction: the provider POSTs signed events to my registered endpoint. Reliability is a checklist — verify the HMAC signature with a constant-time compare before parsing, dedupe by event id because delivery is at-least-once, return 2xx within seconds and process asynchronously with retries and a dead-letter path. On the provider side: exponential backoff, signed timestamps against replay, and a replay API for lost deliveries.
