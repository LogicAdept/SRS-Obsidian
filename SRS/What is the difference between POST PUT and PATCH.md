<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #SRS
# What is the difference between POST PUT and PATCH

> [!abstract] Short answer
> POST means "process this" — the server decides what happens and where the resulting resource lives; repeats cause repeats. PUT means "make the resource at this URI exactly this" — a full replacement the client can safely repeat (idempotent). PATCH means "apply this partial modification" — the payload is a change document, and idempotency depends on that document's semantics (RFC 5789).

## The three contracts

| | POST | PUT | PATCH |
|---|---|---|---|
| Who names the resource | server (Location header) | client (URI in the request) | existing resource |
| Payload meaning | processing instructions / full new entity | complete new representation | partial change document |
| Idempotent | no | yes | not guaranteed |
| Typical use | create in collection, actions, search endpoints | create-or-replace at known id | field updates, deltas |

```json
// POST /orders      -> 201, Location: /orders/8412
{ "sku": "A-1", "qty": 2 }

// PUT /orders/8412  -> full replace
{ "sku": "A-1", "qty": 2, "note": "gift" }

// PATCH /orders/8412 -> partial
{ "qty": 3 }
```

**Listing 1.** The same intent expressed three ways: the body shape and the response contract differ, not just the verb.

## The idempotency math (why this trio is drilled)

- **POST × N** → N resources: retries after a network timeout are dangerous, hence Idempotency-Key headers in payment APIs ([[What is idempotency in HTTP and in messaging]]).
- **PUT × N** → the same end state: the last complete write wins. The price: the client must know the full representation — a PUT missing a field *removes* it (or the server rejects; the contract is "replace").
- **PATCH × N:** a `{ "qty": 3 }` JSON-patch-style document is idempotent (same result each time); an `INC qty` delta-style patch is not (each repeat adds). RFC 5789 explicitly leaves this to the patch document format — JSON Merge Patch is idempotent by construction.

```d2
direction: down
p: "POST /orders\nserver: create + Location" { width: 280; height: 80; style.fill: "#e3f2fd" }
u: "PUT /orders/8412\nclient: full replace, idempotent" { width: 300; height: 80; style.fill: "#fff3e0" }
pa: "PATCH /orders/8412\ndelta, idempotency = payload's" { width: 300; height: 80; style.fill: "#ffebee" }
```

**Fig. 1.** Three cards of the same deck: ownership of the URI and the body's completeness define the contract.

> [!warning] "PUT = update" is the popular lie
> PUT is *replace*: partial data sent as PUT either wipes fields or forces the client to GET-then-merge (a race under concurrency). That is the gap PATCH fills. Second trap: "PUT cannot create" — it can (create-or-replace at a client-chosen URI; that is how idempotent upserts work). Third: treating PATCH as automatically retry-safe — retries are safe only if the patch document itself is idempotent ([[Which common HTTP methods are not idempotent]] for the property table).

The method family: [[What are the HTTP request methods]]; the GET/POST contrast: [[What is the difference between GET and POST]]; REST-level consequences: [[Which HTTP status codes matter most in REST API design]] (201+Location vs 200/204).

> [!tip] Interview answer
> POST: server-owned URI, processing semantics, non-idempotent — repeats duplicate. PUT: client-chosen URI, full replacement, idempotent — and it can create (upsert), but partial PUT loses fields. PATCH: partial change document per RFC 5789, idempotent only if the patch format itself is. The production bow: payment APIs add Idempotency-Key to POST because retries are inevitable — that is this trio's semantics turned into infrastructure.
