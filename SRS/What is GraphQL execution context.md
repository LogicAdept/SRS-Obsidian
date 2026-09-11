<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> The execution context is the **per-request state bag** every resolver can reach: who the caller is, which data loaders and caches are request-scoped, tracing spans, locale — whatever the transport layer built before execution started. It is created once per operation, threaded through the whole tree (each resolver's `context` argument is the same object), and discarded with the request. GraphQL defines the *slot*; servers define what goes in it.

## Lifecycle and what belongs inside

Creation happens at the boundary: the transport (HTTP handler, WebSocket message loop) authenticates the caller, builds the context — user, permissions, loaders, a correlation id — and passes it into execution together with the document and variables. From then on the context is read-mostly: every resolver in the tree shares the same instance, including resolvers running in parallel, so anything mutable in it needs synchronization or should be replaced with request-scoped services ([[What are the four arguments passed to a GraphQL resolver]]).

Typical contents, by contract: authenticated principal and roles for field-level authorization ([[How do you authenticate and authorize a GraphQL request]]); per-request `DataLoader` instances so batch caches cannot leak between users or requests ([[How does DataLoader batch GraphQL resolver calls]]); deadline/cancellation and tracing data for observability; and feature flags if resolvers branch on them.

```java
// graphql-java 26.1: context built per request, read in resolvers.
ExecutionInput anon = ExecutionInput.newExecutionInput()
        .query("{ publicInfo salary }")
        .context(Map.of("role", "anonymous"))       // <- the context
        .build();
// salary resolver: if (!"hr".equals(ctx.get("role"))) throw forbidden;
// anon -> {"errors":[{"message":"Exception while fetching data (/salary) : salary requires role=hr",
//   "path":["salary"],"extensions":{"code":"FORBIDDEN","classification":"DataFetchingException"}}],"data":null}
// hr   -> {"data":{"publicInfo":"public","salary":"120000 USD"}}
```

**Listing 1.** Verified on graphql-java 26.1. The same document with different contexts produced different outcomes: the context carried authorization state, not the document.

```d2
direction: down
T: "Transport layer\nHTTP / WebSocket" { width: 260; height: 65 }
X: "ExecutionContext\nuser, loaders, tracing" { width: 280; height: 70 }
R1: "root resolver" { width: 200; height: 55 }
R2: "nested resolvers" { width: 220; height: 55 }
T -> X: "build once"
X -> R1
X -> R2: "same instance"
```

**Fig. 1.** One context per request: built at the transport, shared read-only by every resolver in the tree.

> [!warning] Context is not a global and not a data store
> Three recurring mistakes. First: a singleton or shared context across requests leaks authentication between users — the classic DataLoader-in-singleton bug is a context bug ([[Why is rate limiting harder in GraphQL than REST]]). Second: hiding heavy data loads inside the context (pre-fetching "everything" up front) defeats lazy execution and reintroduces over-fetching at the server boundary; loaders exist precisely to defer and batch ([[What is the N plus 1 problem in GraphQL]]). Third: conflating context with `info` — context is *who asks*, info is *what the schema looks like here*; authorization belongs to the first, projections to the second ([[What is GraphQL introspection]]).

In Spring for GraphQL the context maps naturally to thread-local-free design: `GraphQLContext` plus `BatchLoaderRegistry`-wired loaders are handed to annotated controllers via parameters, and WebSocket reconnects build a fresh context per subscription session ([[How do GraphQL subscriptions work over WebSockets]]).

> [!tip] Interview answer
> The execution context is per-request shared state: created once at the transport (auth, loaders, tracing), passed to every resolver, gone with the request. It carries who the caller is and request-scoped resources — never global or cross-request data, since parallel resolvers share it read-mostly. Per-request DataLoader caches live here, which is what makes batching safe under multi-tenancy.

