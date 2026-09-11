<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> **Schema-first** writes the SDL contract first (`type Query { ... }`) and binds resolvers to it afterward; **code-first** writes resolver code/classes and **derives** the schema from them (annotations, decorators, type builders). The schema exists in both worlds — the difference is its role: artifact-of-record that code conforms to, versus generated output that documents what code does. Most Java stacks (graphql-java, Spring for GraphQL) are schema-first; many JS stacks default code-first.

## How each workflow runs

Schema-first: SDL is the source of truth — reviewed in PRs, diffed by registries, consumed by codegen for clients; the server parses it and wires resolvers by field name (`RuntimeWiring`, `@SchemaMapping`). The risk: drift — SDL promises a type the resolver never actually produces, and the mismatch surfaces at runtime as nulls or bubbling errors rather than at compile time ([[How does null bubbling work when a GraphQL field is null]]).

Code-first: types are declared in code (annotations on classes, builder APIs); the framework materializes SDL from them for tooling and registries. The risk inverts: the schema mirrors whatever code compiled, so accidental surface changes slip through unless the generated SDL is snapshotted and diffed — effectively re-introducing schema-first's artifact for CI ([[Which GraphQL schema changes are breaking]]).

```java
// graphql-java 26.1, schema-first: SDL string parsed, resolvers bound by name.
GraphQLSchema schema = new SchemaGenerator().makeExecutableSchema(
        new SchemaParser().parse(SDL),                    // <- contract first
        RuntimeWiring.newRuntimeWiring()
                .type("Query", w -> w.dataFetcher("character", byId))  // <- code conforms
                .build());
// forgetting a resolver for a declared field is a wiring gap -> runtime nulls,
// not a compile error: the contract and the code are checked by different tools.
```

**Listing 1.** The schema-first seam: two artifacts (SDL, wiring) joined by field names; tests must bridge what the compiler cannot ([[What is a GraphQL schema]]).

```d2
direction: down
S1: "schema-first\nSDL -> wiring -> schema" { width: 300; height: 65 }
S2: "code-first\nclasses -> schema (generated)" { width: 310; height: 65 }
A: "artifact of record:\nreviewed, diffed" { width: 260; height: 65 }
B: "risk: code drifts from SDL" { width: 280; height: 60 }
C: "risk: SDL churns with code\n-> snapshot + diff it" { width: 320; height: 65 }
S1 -> A
S1 -> B
S2 -> C
```

**Fig. 1.** Same executable schema either way; the difference is which artifact can lie — the SDL (schema-first drift) or the generated view of it (code-first churn).

> [!warning] Neither style removes the verification duty
> Three interview-grade points. First: the split is about **workflow, not capability** — code-first stacks can enforce schema-as-contract by committing generated SDL and gating diffs; schema-first stacks can generate resolver stubs/types from SDL to get compile-time checks; mature setups converge on "SDL committed, code generated, diffs gated" ([[How would you explain Spring for GraphQL]]). Second: code-first does not mean untyped — annotations carry nullability and argument types; but permissive defaults (everything nullable unless marked) quietly produce the "everything is nullable" schema that clients must defensively handle ([[What is the difference between GraphQL list and non-null modifiers]]). Third: federation complicates both — subgraphs need SDL-with-directives (`@key`), which schema-first expresses naturally and code-first frameworks must emit faithfully ([[What is the difference between GraphQL federation and schema stitching]]).

Decision heuristics: contract shared across many teams/languages → schema-first (the SDL is the negotiation table); rapid iteration with the schema owned by one team → code-first velocity; enterprise Java → schema-first with codegen is the prevailing combination.

> [!tip] Interview answer
> Schema-first authors the SDL as the contract and binds resolvers to it — great for cross-team contracts, with drift risk between SDL and code. Code-first derives the schema from annotated code — fast iteration, but the schema can churn silently, so generated SDL must be snapshotted and diffed. Both produce the same executable schema; mature teams converge: commit SDL, generate types, gate diffs in CI.

