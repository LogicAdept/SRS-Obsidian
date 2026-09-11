<!--
reps: 0
priority: 0
-->
#API/REST #API/Contracts #API/Idempotency #SystemDesign/Architecture #SRS

# How would you design a delete operation or endpoint

> [!abstract] Short answer
> A production-grade delete is rarely a physical DELETE: it is an idempotent operation with authorization, soft-delete semantics (a status flag or deleted_at timestamp, so recovery and audit survive), consistency handling of what the deletion references (children, counters, caches, search indexes), and an explicit story for permanent removal (retention windows, GDPR erasure jobs). The endpoint contract states the semantics: what 200/204/404 mean, that repeated calls stay idempotent, and how async deletions report progress.

## The contract: idempotent, authorized, explicit

DELETE as an HTTP method is idempotent by definition — the effect of N calls equals one ([[What is idempotency in HTTP and in messaging]] grounds the semantics) — and the implementation must honor that: deleting an already-deleted resource returns the same terminal response (204 Gone/204 No Content or 404 per the API's stated contract — pick one and document it as part of the endpoint's contract), never "not found" for the first call and an error for the second. Authorization is resource-level: the caller may delete THIS resource, not just "some resource" — ownership checks belong server-side. Concurrency needs handling: optimistic locking (If-Match/ETag or a version check) prevents deleting a resource another user just modified — the delete rejects with 409/412 when the precondition fails. Long-running deletions (cascades over millions of rows) should not run inside the HTTP request: return 202 Accepted with a status resource, and process asynchronously — the same pattern as any long operation, with progress reporting and an idempotent worker.

```text
DELETE /orders/42   If-Match: "v7"
  401/403  not authorized            (resource-level check)
  412      ETag mismatch             (concurrent modification)
  202      {statusUrl}               (async cascade accepted)
  204      soft-deleted (deleted_at set, row retained)
  204      repeat call -> same 204   (idempotent, no error)
background: cascade children, update counters, evict caches,
            purge search index; retention job purges later
```

**Listing 1.** The delete contract with its terminal states and background work.

## The data story: soft delete, cascades, and real removal

Soft delete (a `deleted_at` column or status) is the default because deletion is almost always recoverable-by-requirement: users undo, auditors investigate, and foreign keys stay resolvable. Its costs are real and must be engineered: every read query gains a filter (deleted_at IS NULL — an index or a view keeps it from rotting; [[What is a database index and why does it speed up queries]] for the filtering cost), uniqueness constraints need compositing with the delete marker (a unique email must allow re-registration after deletion), and storage grows — which is why soft delete pairs with a retention/purge policy (a scheduled hard-delete after the retention window; for regulated data, an erasure pipeline satisfying GDPR while preserving legal holds). Cascades are a contract decision, not a database default: children deleted, orphaned, or archived — decided explicitly, executed transactionally or via the async worker, and mirrored to derived stores: counters decremented, caches evicted ([[How do you invalidate Spring Cache in a cluster]] for the cluster case), search index entries removed. Event-driven designs publish a Deleted event so all projections react ([[How does an aggregate persist and publish events without a distributed transaction]]'s outbox keeps the event atomic with the state change). [[How would you design a delete operation or endpoint]]-adjacent UX thinking ([[What steps would you take to implement a delete report button in a system]]) covers the human side: confirmation, undo window, audit trail.

> [!warning] A hard DELETE is the one operation you cannot unship
> Physically deleting rows destroys the audit trail, breaks foreign-key history and makes recovery a restore-from-backup exercise. If you must hard-delete, the retention job — not the user-facing endpoint — should be the only code path that does it.

```d2
req: DELETE /orders/42 If-Match v7
auth: resource-level authz {
  a1: 401/403 -> deny
}
pre: precondition check {
  p1: 412 ETag mismatch
}
soft: soft delete {
  s1: set deleted_at
  s2: unique keys recomposed
}
resp: 204 (repeat -> same 204,
idempotent terminal)
bg: async worker {
  b1: cascade children
  b2: update counters
  b3: evict caches
  b4: purge search index
}
ret: retention job -> hard purge
(after window, only path)
req -> auth -> pre -> soft -> resp
soft -> bg: Deleted event (outbox)
bg -> ret: retention window
```

**Fig. 1.** The delete flow: authorization and preconditions guard the soft delete; the outbox event drives projections; the retention job is the only hard-delete path.

> [!tip] Interview answer
> I design delete as idempotent and authorized, usually soft (deleted_at), with ETag preconditions for concurrency, 202-plus-status-resource for big cascades, and explicit cascade semantics — children, counters, caches, search index. Real removal lives in a retention job, not the endpoint, and a Deleted event drives all projections atomically via the outbox.
