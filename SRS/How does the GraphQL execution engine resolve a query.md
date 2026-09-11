<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> The engine executes a validated operation top-down by levels: it resolves the root field(s), then for each returned object resolves the fields selected under it, recursing until scalars and enums terminate the branch. Every field goes through its own resolver; sibling fields at the same level may run in parallel, parent fields complete before their children start. The result is assembled as a map whose shape mirrors the selection set.

## Phases: parse, validate, execute

Before anything executes, the document is parsed into an AST and validated against the schema (field existence, argument types, fragment spreads, variable usage). Execution then walks the selection set: for each field the engine invokes the field's resolver, coerces the result to the declared type, and — if the result is an object — repeats for the nested selection. A field's resolver sees the parent value via its source argument ([[What are the four arguments passed to a GraphQL resolver]]). Fields without explicit resolvers use default property lookup ([[How does a default GraphQL resolver work]]).

```java
// graphql-java 26.1: SDL -> schema, then execute { hero { id name } }
GraphQLSchema schema = new SchemaGenerator().makeExecutableSchema(
        new SchemaParser().parse(SDL),
        RuntimeWiring.newRuntimeWiring()
                .type("Query", w -> w.dataFetcher("hero", heroFetcher))
                .build());
GraphQL graphql = GraphQL.newGraphQL(schema).build();
// {"data":{"hero":{"id":"1000","name":"Luke Skywalker"}}}
// unselected sibling (homePlanet) never appears: execution follows the selection set only
```

**Listing 1.** Verified on graphql-java 26.1. The engine ran only the selected fields; `homePlanet` existed on the record but was never resolved.

```d2
direction: down
V: "Validate against schema" { width: 270; height: 60 }
Q: "Query.hero (root resolver)" { width: 270; height: 60 }
C: "Character.id, .name (leaf resolvers)" { width: 320; height: 60 }
D: "data map assembled" { width: 240; height: 55 }
V -> Q: "ok"
Q -> C: "children of returned object"
C -> D
```

**Fig. 1.** Execution is a tree walk: root fields first, then children per returned object, stopping at scalar leaves.

> [!warning] "Parallel" has a precise meaning here
> Spec text says root query fields "are expected to be resolved in parallel" and mutation root fields serially — but field-level parallelism is a server implementation choice, not a guarantee. Nested object fields also fan out independently: two `friends` entries each run their own `name` resolver, which is exactly how N+1 happens — one fetch per parent per nested field, unless you batch ([[What is the N plus 1 problem in GraphQL]]). Another classic misread: GraphQL does **not** start all root fields and pick winners — resolvers run to completion (or completion of their returned future) per field, and an engine may limit true concurrency arbitrarily ([[What is GraphQL execution context]]).

Resolvers may return plain values or futures/promises; async resolvers are awaited before their children start, so partial trees do not race ahead of their parents. Errors are per-field: a failing field produces an error entry and — if its type is non-null — triggers null bubbling instead of aborting siblings ([[How does null bubbling work when a GraphQL field is null]]). The engine also enforces the response shape contract: the `data` map contains exactly the selected fields with their aliases, nothing for skipped or unknown fields ([[When do you use aliases in a GraphQL query]]).

> [!tip] Interview answer
> Execution is per-field: validate first, then walk the selection set level by level, calling each field's resolver with the parent value, recursing into objects and stopping at scalars. Sibling root query fields may run in parallel; mutations run serially. Errors are scoped to the failing field and surface in the errors array with data preserved where possible. The response map mirrors the selection set — nothing extra, nothing skipped.

