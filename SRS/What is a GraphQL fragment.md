<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A fragment is a named, reusable set of fields on a given type: `fragment Name on Type { ... }` spread with `...Name`. Dumps use them when several queries or UI components need the same selection, so you change fields once.

Named fragments: reuse and colocation (Relay/Apollo: a component owns the fragment for the data it renders). Inline fragments (`... on Type`) select fields on interfaces and unions for the concrete type.

Some lists also claim fragments help normalized caches because repeating `id` lets the client match objects.

> [!warning] Unverified traps from the dump
> - Dump claim: inline fragments are for polymorphic types; named fragments are for reuse — related, not the same tool.
