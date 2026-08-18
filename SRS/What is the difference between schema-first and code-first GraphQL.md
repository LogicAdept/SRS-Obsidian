<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Schema-first: write `.graphql` SDL by hand, then implement matching resolvers. Pros in dumps: explicit, language-agnostic contract. Cons: SDL and resolvers can drift.

Code-first: define types in the host language (Nexus, TypeGraphQL, Strawberry, Pothos); SDL is generated. Pros: one source of truth, language type-safety, refactors. Cons: schema less obvious, coupled to that stack.

Trade-off dumps name: schema-first optimizes for a shared contract; code-first for type-safety and less drift.

> [!warning] Unverified traps from the dump
> - Dump claim: generated SDL is still the published contract even in code-first.
