<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Authentication (who you are): dumps put it at the HTTP/middleware layer (JWT or cookie), then stash the user on GraphQL `context`. GraphQL itself has no login step.

Authorization (what you may do): per field or per object in resolvers or a shared service/directive (`@auth`). One URL does not equal one ACL the way a REST route might. A single query can touch many types.

Throw (for example Forbidden); other fields can still resolve. Data-layer RLS is listed as defense in depth but lacks query-shape context.

> [!warning] Unverified traps from the dump
> - Dump claim: endpoint-level auth is not enough; check per field.
