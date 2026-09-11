<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> graphql-java is the **canonical GraphQL engine for the JVM**: a MIT-licensed library (not a framework) that parses SDL, builds executable schemas, validates documents, and executes operations — with resolvers expressed as `DataFetcher`s bundled per field. It implements the spec (including subscriptions via reactive-streams), ships analysis tooling (`MaxQueryDepthInstrumentation`, `MaxQueryComplexityInstrumentation`), and is the foundation under Spring for GraphQL. Version 26.x is the current line; it targets modern JDKs and needs Java 8+ historically, newer lines require Java 11+.

## The core API surface

Four steps cover the whole engine. **Parse SDL**: `SchemaParser` turns SDL text into a `TypeDefinitionRegistry`. **Wire and build**: `RuntimeWiring` binds `DataFetcher`s to type/field pairs, and `SchemaGenerator.makeExecutableSchema` merges both into a `GraphQLSchema`. **Wrap**: `GraphQL.newGraphQL(schema).build()` creates the execution facade. **Execute**: `graphql.execute(ExecutionInput)` runs parse/validate/execute and returns a spec-shaped result — `data`, `errors`, optionally extensions. Async variants return `CompletableFuture`; a subscription operation returns a result whose `data` is a `Publisher` of per-event results ([[How do GraphQL subscriptions work over WebSockets]]).

```java
// graphql-java 26.1 — the minimal full cycle:
GraphQLSchema schema = new SchemaGenerator().makeExecutableSchema(
        new SchemaParser().parse(SDL),
        RuntimeWiring.newRuntimeWiring()
                .type("Query", w -> w.dataFetcher("character", byId))
                .build());
GraphQL graphql = GraphQL.newGraphQL(schema).build();
ExecutionInput in = ExecutionInput.newExecutionInput()
        .query("{ character(id: "1000") { name } }")
        .dataLoaderRegistry(registry)          // batching hooks in here
        .build();
// {"data":{"character":{"name":"Luke Skywalker"}}}
```

**Listing 1.** Verified on graphql-java 26.1 (JDK 21): SDL in, wiring merged, execution out — the four-step shape every framework on top of it reuses ([[How does the GraphQL execution engine resolve a query]]).

```d2
direction: down
Sdl: "SDL text" { width: 150; height: 50 }
Reg: "TypeDefinitionRegistry" { width: 260; height: 55 }
W: "RuntimeWiring\nDataFetchers, TypeResolvers" { width: 300; height: 65 }
Sch: "GraphQLSchema" { width: 190; height: 55 }
G: "GraphQL facade" { width: 190; height: 55 }
R: "ExecutionInput ->\ndata + errors" { width: 240; height: 65 }
Sdl -> Reg
Reg -> Sch
W -> Sch
Sch -> G
G -> R
```

**Fig. 1.** The engine's pipeline: SDL parsed, wiring merged into a schema, wrapped in the facade, executed per request.

> [!warning] It is an engine, not a web framework
> Three boundaries worth stating precisely. First: no transport — graphql-java knows nothing about HTTP or WebSocket; servers embed it behind a handler, or adopt Spring for GraphQL which owns that layer ([[How would you explain Spring for GraphQL]]). Second: no DI, no annotations — wiring is explicit code; forgetting a fetcher fails at wiring time for missing types or manifests as runtime nulls for fields, so tests against real schemas are mandatory ([[How does a default GraphQL resolver work]]). Third: **enum and scalar coercion details are engine-specific**: SDL enums arrive as name strings unless mapped to Java enums, `Int` is 32-bit, and custom scalars implement serialize/parseValue/parseLiteral — knowing these beats knowing the API ([[What are GraphQL scalar types]]).

What it ships that interviews touch: instrumentation hooks (tracing, depth/complexity limits) applied at `newGraphQL(...).instrumentation(...)`; first-class DataLoader integration via `DataLoaderRegistry` on the execution input; and `DataFetchingEnvironment` bundling parent/args/context/info per resolver ([[What are the four arguments passed to a GraphQL resolver]]). For federation, graphql-java provides subgraph support (`@key`/entity fetchers); the router role typically uses Apollo Router or a Java gateway.

> [!tip] Interview answer
> graphql-java is the JVM's reference-quality GraphQL engine: SchemaParser plus RuntimeWiring produce an executable schema; GraphQL.newGraphQL wraps it; execute runs validation and per-field DataFetchers. It ships subscriptions over reactive-streams, DataLoader batching, and depth/complexity instrumentation — but no HTTP layer and no DI, which is exactly the gap Spring for GraphQL fills.

