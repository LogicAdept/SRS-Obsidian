<!--
reps: 0
priority: 0
-->
#API/Idempotency #SRS

# What is the Idempotency-Key header used for in HTTP APIs

> [!abstract] Short answer
> The Idempotency-Key header makes unsafe POST retries safe: the client generates a unique key per logical operation and resends the same key on every retry; the server stores key -> outcome (or key -> effect) and replays the stored response instead of re-executing. Payment APIs (Stripe standardized the practice) use it because a retried charge must never double-charge.

## The protocol mechanics

Flow: client picks a key (UUID) scoped to one logical operation; sends POST with the key; the server, keyed on (key, endpoint scope), does an atomic put-if-absent of the outcome. First call executes and stores; a retry with the same key finds the stored outcome and replays it — same status, same body — so the client cannot even tell it retried. The edge cases define the design: a retry arriving while the first execution is still in flight (server must track in-flight keys and either wait, reject with 409 and Retry-After, or serialize — returning "not found yet" would break the contract); a key reused with a different payload (client bug — reject 409/422, do not silently re-execute); key retention (Stripe keeps keys 24 hours; the window is part of the documented contract); and scoping — keys are per endpoint or per operation type, not global. On the client: one key per logical attempt group, regenerated only for a genuinely new operation; on a new key after error, the old operation must be provably dead ([[What is idempotency in HTTP and in messaging]] for the semantic ground; [[How do you design idempotent REST API operations]] for the design discipline; [[What is the Idempotent Receiver pattern]] for the messaging twin).

```text
== first POST, key=k1 ==
server: key=k1 -> PROCESS (charge #1)
client: 201 {"charge":"c1","amount":1000}
== network timeout, client retries POST with SAME key=k1 ==
server: key=k1 -> REPLAY (no second charge)
client: 201 {"charge":"c1","amount":1000}
== new operation, new key=k2 ==
server: key=k2 -> PROCESS (charge #2)
client: 201 {"charge":"c2","amount":1000}
== POST without key ==
client: 400 {"error":"Idempotency-Key header required"}
```

**Listing 1.** Verified on JDK 21 (com.sun.net.httpserver): the store maps key -> stored response; same-key retries replay charge c1 twice without a second charge, a new key processes normally, and a missing key is rejected up front (out/A02_IdempotencyKey.txt).

```d2
c: client
s: server
st: key store {
  k1: k1 -> 201 charge c1
  k2: k2 -> 201 charge c2
}
c -> s: POST + Idempotency-Key: k1
s -> st: put-if-absent k1
s -> c: 201 (executed)
c -> s: timeout -> retry k1
s -> st: get k1 -> replay
s -> c: 201 same body (no re-exec)
```

**Fig. 1.** The server replays the stored outcome for a repeated key; execution happens exactly once per key.

## Implementation decisions that matter

Storage: the store must be shared across server instances (the honest options are a DB unique constraint or a Redis-style TTL store with a synchronous write path) and written atomically with the effect when correctness demands it (transactional outbox makes key and effect one transaction — [[How does an aggregate persist and publish events without a distributed transaction]] for the pattern). TTL equals the documented retention; expired keys re-executing is a documented risk window, not a bug to discover. Headers extend the pattern: request-id echo for tracing, replay indicators for debugging. The pattern generalizes beyond REST — queue consumers, job submissions, and payment processors all implement it; the header is just its standardized HTTP dress ([[How do you handle long-running operations in a REST API]] — async endpoints need the same discipline at job creation).

> [!warning] The key is a promise about payload identity
> Same key with a different body must be an error, never a re-execution — otherwise the key is decoration and double-execution returns through the "new key per retry" bug. Validate the payload hash against the stored one; Stripe rejects the mismatch.

> [!tip] Interview answer
> Idempotency-Key turns unsafe POSTs into safely retryable operations: the client generates one key per logical operation and reuses it on retries; the server atomically stores key to first outcome and replays that outcome for duplicates — same status, same body, no second charge. Hard edges are the in-flight retry (must serialize or 409, never re-run), key reuse with a different payload (reject), and retention (a documented TTL). The store is shared, transactional with the effect when needed, and scoped per operation.
