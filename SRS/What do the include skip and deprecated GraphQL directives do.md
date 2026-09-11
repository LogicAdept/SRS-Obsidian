<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> `@skip(if: ...)` removes a field from the result when the condition is true; `@include(if: ...)` keeps it only when true; `@deprecated(reason: ...)` marks a schema field, argument, input field, or enum value as legacy so it shows up in tooling and can be removed later. The first two are client-side runtime directives defined by the spec; the third is a schema-authoring annotation. All three are regular directives — the spec simply defines them for every schema.

## Runtime directives: conditional selection

`@skip` and `@include` take one boolean `if` argument, typically a variable: `homePlanet @include(if: $withHome)`. They are mutually exclusive in meaning — `@skip(if: $x)` equals `@include(if: !$x)` — and they act at execution: the field is not resolved, not executed, and absent from the response, but it is still part of the document and still validated ([[What is a GraphQL fragment]]).

```java
// graphql-java 26.1, variables {withHome: false}:
// query Both($withHome: Boolean!) {
//   second: human(id: "1000") { ...humanFields homePlanet @include(if: $withHome) }
// }
// {"data":{"second":{"name":"Luke"}}}   // homePlanet not resolved, not present
```

**Listing 1.** Verified on graphql-java 26.1: the conditionally included field is missing from the response, not null — no resolver ran for it.

`@deprecated` lives in SDL: `homePlanet: String @deprecated(reason: "Use origin instead")`. It changes nothing at runtime — the field still resolves — but introspection exposes `isDeprecated` and the reason, so clients, IDEs, and schema-diff tools flag usage long before removal ([[What is GraphQL introspection]]). Deprecation is the core of additive schema evolution: add the replacement, deprecate the old, migrate callers, remove later ([[How do you version a GraphQL schema]]).

> [!warning] Directives are not feature flags for server logic
> Three traps. First, `@skip`/`@include` only select fields — they cannot change resolver behavior, skip authorization, or hide data: an unauthorized caller can `@include` whatever the schema already exposes ([[How do you authenticate and authorize a GraphQL request]]). Second, custom directives must be *declared* in SDL with their locations and, on most servers, implemented by the framework — SDL alone defines validation placement, not behavior ([[What is the difference between schema-first and code-first GraphQL]]). Third, do not build boolean explosion into queries (`@include(if: $modeIsX)` on dozens of fields): that is a sign the API needs separate operations or fields, not conditional mega-queries.

Beyond the built-ins, custom directives are the extension point of choice for cross-cutting schema behavior — `@auth`, `@upper`, `@cacheControl` — applied as annotations on schema elements and implemented via directive wiring in graphql-java or transform hooks in federated composition. The spec reserves no names for them and requires every directive to declare where it may appear (locations) and its argument types ([[What is Schema Definition Language in GraphQL]]).

```d2
direction: down
F: "field @include(if: $c)" { width: 270; height: 55 }
C: "$c == true" { width: 160; height: 50 }
C2: "$c == false" { width: 170; height: 50 }
Exec: "resolver runs,
key in response" { width: 260; height: 60 }
Skip: "no execution,
key absent" { width: 230; height: 60 }
F -> C: "if"
F -> C2: "if"
C -> Exec
C2 -> Skip
``
```

**Fig. 1.** Runtime directives gate execution and response presence per field; the document itself still validates as if the field were unconditional.

> [!tip] Interview answer
> `@skip`/`@include` are spec-defined runtime directives controlling whether a selected field executes and appears in the response — driven by variables, validated but conditionally absent. `@deprecated` is the schema-side marker: no runtime effect, but introspection surfaces it so tooling and diffing flag legacy fields during additive evolution. Custom directives extend the same mechanism with declared locations and server-side wiring.

