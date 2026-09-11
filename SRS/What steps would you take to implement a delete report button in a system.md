<!--
reps: 0
priority: 0
-->
#Career/Interview #SystemDesign #SRS

# What steps would you take to implement a delete report button in a system

> [!abstract] Short answer
> A "delete report" feature is a requirements-first walkthrough: clarify what "delete" means here (hide from the author? purge content? respect retention rules?), define authorization and audit, choose soft delete with an undo window, design the API and its idempotency, handle derived data (caches, search, aggregates), and ship with tests for the edge cases — the question tests whether you turn a one-word feature into an explicit contract before coding.

## Requirements before keyboard

The first steps are questions, not code. What is being deleted: a user's own report (self-service), any report (admin moderation), or anonymization rather than deletion (compliance may forbid true deletion of financial records)? What happens to references: comments on the report, links, aggregate statistics that counted it, an audit trail that must survive ([[Why is a database preferable to plain text files for structured data]]-level: the data model's integrity rules are the frame)? Is deletion reversible (an undo window is standard UX and an engineering safety net) or immediate? Who may do it (authorization matrix: author, moderator, service account) and what must be logged (who deleted what when — the audit requirement usually decides soft versus hard delete before any framework choice). The retention/compliance answer frequently overrules the product's first instinct: for regulated data the button schedules erasure rather than executing it. These clarifications are the actual interview deliverable — the implementation is routine once they are explicit.

```text
1 clarify : whose delete? reversible? retention/GDPR constraints?
2 authorize: owner? moderator? + audit record (who/when/what)
3 model    : soft delete (deleted_at, deleted_by) + undo window
4 api      : idempotent DELETE, 202 for heavy cascade,
             Deleted event for projections
5 execute  : transactional state change; async: search index,
             caches, counters; retention job for real purge
6 test     : auth matrix, double-delete, undo, cascade, audit trail
```

**Listing 1.** The step ladder from requirements to shipped button.

## The implementation steps

With the contract settled, the engineering is layered. Data: a soft-delete marker (deleted_at/deleted_by) rather than row removal — recoverable, auditable, FK-safe ([[How would you design a delete operation or endpoint]] develops the full endpoint contract); unique constraints composite with the marker if the resource name must become reusable. API: an idempotent DELETE with resource-level authorization, ETag precondition against concurrent edits, 202-plus-status for cascades that exceed interactive latency; an undo endpoint is the inverse operation within the undo window. Propagation: the state change emits a Deleted event (outbox for atomicity with the state change — [[How does an aggregate persist and publish events without a distributed transaction]]), consumers update search index, caches and aggregate counters; UI and feeds stop showing the report after the projections catch up ([[What is eventual consistency]] bounds the "still visible" window — worth telling users "removal propagates within N minutes"). The purge path: a retention job hard-deletes after the window, the only code path allowed to. Tests: the auth matrix, double-delete idempotency, undo correctness, cascade completeness (nothing references a deleted report), and the audit record. The interview close names the tradeoffs made: soft delete costs storage and a filter on every query ([[What is database denormalization for]]'s cousin: read-path costs of write-path choices), and eventual propagation costs a visibility window.

> [!warning] The button is the visible 10% — the contract is the feature
> Deleting without an authorization matrix, audit trail and propagation plan leaks (unauthorized deletes), loses history (unauditable), and rots derived data (stale search hits, wrong counters). The clarifying questions are not ceremony — they are where the bugs are prevented.

> [!tip] Interview answer
> I start with requirements: whose delete, reversible or not, retention constraints, and the audit need — those decide soft versus hard delete before any code. Then: authorized idempotent DELETE with ETag and undo window, soft-delete marker plus Deleted event via outbox, async propagation to search/caches/counters, a retention job as the only hard-delete path, and tests for auth, idempotency and cascade completeness.
