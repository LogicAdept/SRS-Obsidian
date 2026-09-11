<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> A fragment is a **named, reusable selection set**: declared once (`fragment UserFields on User { id name }`) and spread into operations with `...UserFields`. It removes duplication across operations, enables per-type selections on interfaces and unions via type conditions (`... on Movie`), and is the only way to select type-specific fields on polymorphic results — the server splices the fragment's fields in where the spread appears.

## Definition, spread, type conditions

A fragment declares the type it applies to (an object type, an interface, or a union). When spread, the engine includes the fragment's fields only for values whose runtime type matches the condition — for an object type that is always true, for interfaces and unions it is the type resolver's decision. Inline fragments (`... on Movie { title }`) skip the named declaration and are the standard idiom on unions ([[What is the difference between a GraphQL interface and a union]]). Fragments may reference variables and directives, and spreads may nest, subject to one hard rule: no cycles — a fragment cannot spread into itself, which validation rejects statically.

```java
// graphql-java 26.1:
String fragDoc = """
        query Both($withHome: Boolean!) {
          first: droid(id: "2000") { ...droidFields }
          second: human(id: "1000") { ...humanFields homePlanet @include(if: $withHome) }
        }
        fragment droidFields on Droid { name }
        fragment humanFields on Human { name }
        """;
// with variables {withHome: false}:
// {"data":{"first":{"name":"C-3PO"},"second":{"name":"Luke"}}}
```

**Listing 1.** Verified on graphql-java 26.1: two typed fragments spliced into one operation; the `@include(false)` field is absent from the result entirely ([[What do the include skip and deprecated GraphQL directives do]]).

> [!warning] Fragment type conditions must match, and `@skip` fields still cost validation
> A spread on the wrong type is a validation error — `...droidFields` on a `human` field fails before execution, because Droid and Human share no common shape. Conversely, a fragment on the **interface** applies to every implementer and is the honest way to select shared fields. The performance trap: directives strip fields at *execution*, but the document still carries them, and some client-side caches re-request skipped fields when the condition flips — treat conditionally included fields as part of the payload contract ([[Why prefer GraphQL variables over inlined values]]).

On the client side, fragments are the unit of colocation: a component declares the fields it needs as a fragment, and the view composes fragments into operations — Relay formalizes this entirely. On the server side fragments exist only until validation: the document is flattened against the schema before execution, so resolvers never see fragment structure — execution is a plain selection tree ([[How does the GraphQL execution engine resolve a query]]).

Named fragments also serve as stable contracts between teams: a shared `UserFields` fragment changes with the schema, and adding a field to it silently grows every operation that spreads it — convenient for cohesion, dangerous when the fragment is too broad and operations start fetching data nobody reads ([[What is over-fetching and under-fetching compared with REST]]).

```d2
direction: down
Op: "Operation selection set" { width: 260; height: 60 }
Fr: "fragment UserFields on User
id, name" { width: 300; height: 70 }
TC: "... on Movie { title }
inline typed fragment" { width: 280; height: 70 }
Flat: "Flattened selection tree
at validation" { width: 280; height: 65 }
Op -> Fr: "spread"
Op -> TC: "type condition"
Fr -> Flat
TC -> Flat
``
```

**Fig. 1.** Fragments are spliced at validation: the server executes a plain selection tree, while clients keep them as per-type reusable contracts.

> [!tip] Interview answer
> A fragment is a named selection set spliced wherever it is spread, with a type condition that gates it by runtime type. It kills duplication across operations and is the required tool on interfaces and unions through inline or named typed spreads. Validation flattens fragments before execution — resolvers see a plain selection tree — and client architectures use fragments as per-component field contracts. Cycles are rejected; conditions must type-match.

