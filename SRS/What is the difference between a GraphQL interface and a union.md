<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Both are abstract types. An interface lists fields every implementer must include (an `is-a` with shared fields, for example `Node { id }`). Clients can query those shared fields without inline fragments.

A union is a set of object types with no required common fields (`SearchResult = User | Post`). Clients must use inline fragments (`... on Type`) per branch.

Choose interface when types share structure you query in common; union when they do not. Both need a runtime concrete type (`__resolveType` / `__typename`).

> [!warning] Unverified traps from the dump
> - Dump claim: `__typename` is how clients tell union members apart.
