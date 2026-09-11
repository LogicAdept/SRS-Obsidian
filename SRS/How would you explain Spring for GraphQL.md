<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Spring for GraphQL is the **official Spring stack over the graphql-java engine**: it adds the transport and integration layer graphql-java lacks — HTTP and WebSocket endpoints, annotated controller mappings (`@QueryMapping`, `@SchemaMapping`, `@SubscriptionMapping`), exception translation, security context propagation, first-class DataLoader wiring via `BatchLoaderRegistry`, and Boot auto-configuration with GraphiQL. You write Spring idioms; the engine executes.

## What the annotations map to

A `@Controller` with `@QueryMapping` methods becomes root-field resolvers: the method name (or the annotation's field name) binds to the schema field, parameters are injected (`@Argument`, `@Arguments`, `DataFetchingEnvironment`, `Principal`, `Context`). `@SchemaMapping(typeName = "Character")` binds nested fields; `@BatchMapping` declares a batch loader that Spring registers as a DataLoader — the idiomatic N+1 cure ([[How does DataLoader batch GraphQL resolver calls]]). `@SubscriptionMapping` methods return a reactive `Flux`/`Publisher` that becomes the source event stream over WebSocket ([[How do GraphQL subscriptions work over WebSockets]]).

```java
// Spring for GraphQL shape (Boot starter: spring-boot-starter-graphql):
@Controller
class CharacterController {
    @QueryMapping
    Character characterById(@Argument String id) { ... }        // Query.characterById

    @SchemaMapping(typeName = "Character")
    CompletableFuture<List<Episode>> episodes(Character c) { ... } // nested field

    @BatchMapping(typeName = "Character")
    Mono<Map<Character, List<Episode>>> episodesFor(List<Character> list) { ... } // batched
}
// the endpoint is auto-exposed at POST /graphql; GraphiQL on /graphiql in dev.
```

**Listing 1.** The Spring contract: annotations bind methods to schema fields; the engine under them is graphql-java with Spring's wiring conventions ([[How does the GraphQL execution engine resolve a query]]).

```d2
direction: down
Http: "POST /graphql\nWebSocket /graphql" { width: 220; height: 60 }
Sc: "Spring controllers\n@QueryMapping / @SchemaMapping" { width: 330; height: 65 }
Se: "Security / context propagation" { width: 300; height: 60 }
E: "graphql-java engine" { width: 220; height: 55 }
R: "BatchLoaderRegistry\nDataLoader dispatch" { width: 290; height: 60 }
Http -> Sc
Sc -> Se
Se -> E
R -> E
```

**Fig. 1.** Spring owns transport, security, and wiring ergonomics; graphql-java owns execution; BatchLoaderRegistry bridges both for batching.

> [!warning] Spring sugar does not change engine semantics
> Three corrections for interviews. First: **nullability, coercion, and bubbling are graphql-java's** — a `@SchemaMapping` returning null for a non-null field still triggers null bubbling; Spring adds no nullability magic ([[How does null bubbling work when a GraphQL field is null]]). Second: **exception handling is translation, not swallowing**: `@GraphQlExceptionHandler` methods map exceptions to `GraphQlErrorException`/error entries — unhandled exceptions become generic field errors with class details hidden ([[What does the GraphQL errors array contain]]). Third: **context propagation is explicit** — security principals and `GraphQLContext` flow through reactor contexts; long-lived subscription streams need re-authorization per event since the socket outlives tokens ([[How do you authenticate and authorize a GraphQL request]]).

Boot integration specifics worth naming: the starter auto-configures the `/graphql` endpoint (HTTP + WebSocket), `WebGraphQlInterceptor` for header/context plumbing, `GraphiQL` builder enabled by default in dev profiles, federation subgraph support via `@BatchMapping` entity resolvers, and first-party testing support (`GraphQlTester` against mocks or live transports). Where does Spring stop? At the router: federation gateway duties belong to a dedicated router deployment ([[What is the difference between GraphQL federation and schema stitching]]).

> [!tip] Interview answer
> Spring for GraphQL is the transport and integration layer over graphql-java: Boot auto-configures /graphql and GraphiQL, controllers bind resolvers via @QueryMapping/@SchemaMapping, @BatchMapping registers DataLoaders declaratively, @SubscriptionMapping returns Flux streams over WebSocket. It adds exception translation, security propagation, and GraphQlTester — while execution semantics stay the engine's.

