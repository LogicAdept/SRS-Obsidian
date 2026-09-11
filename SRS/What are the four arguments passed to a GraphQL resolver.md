<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Every resolver receives four positional arguments: **parent** (the value of the enclosing object, often called `obj` or `source`), **args** (the field's argument values), **context** (per-request shared state: authenticated user, data loaders, tracing spans), and **info** (execution metadata: the field definition, its return type, the selection set, path). In graphql-java they are packed into one `DataFetchingEnvironment` exposing all four.

## What each argument is for

The **parent** is how nested resolvers chain: a root field returns an object; each child field's resolver receives that object as source and reads or computes its part ([[How does a default GraphQL resolver work]]). The **args** map carries the client's argument values, coerced and defaulted ([[How do you pass arguments to a GraphQL field]]). The **context** is created per request before execution and threaded through every resolver — the natural place for auth state and request-scoped caches ([[What is GraphQL execution context]]). The **info** parameter reveals where in the schema this resolver runs: field name, return type, the merged selection set (what the client actually asked for — useful for projections), and the response path for error reporting ([[How does the GraphQL execution engine resolve a query]]).

```java
// graphql-java 26.1: one DataFetcher reading all four concerns through the environment.
DataFetcher<Object> salary = env -> {                       // the whole env = 4 args in one
    Employee e = env.getSource();                           // parent
    String unit = env.getArgumentOrDefault("unit", "USD");  // args
    String role = ((Map<String, Object>) env.getContext()).get("role").toString(); // context
    return env.getFieldDefinition().getName() + ":" + unit + ":" + role;            // info
};
```

**Listing 1.** The environment is the four-argument bundle: source, argument map, context object, and field/selection metadata.

```d2
direction: down
P: "parent / source\nenclosing object value" { width: 280; height: 65 }
A: "args\ncoerced argument values" { width: 240; height: 60 }
C: "context\nrequest-scoped state" { width: 250; height: 60 }
I: "info\nfield definition, selection, path" { width: 300; height: 65 }
R: "Resolver" { shape: oval; width: 160; height: 50 }
P -> R
A -> R
C -> R
I -> R
```

**Fig. 1.** Four inputs, one resolver call — different lifecycles: parent from execution, args from the request document, context from transport setup, info from the schema.

> [!warning] context and info are not interchangeable — and one of them leaks
> Two traps. First: context is created at the transport boundary; putting per-field mutable state into it makes parallel sibling fields race ([[Why do GraphQL mutations run serially while queries can run in parallel]]). Second: `info.getSelectionSet()` is a projection tool, but anything you *skip* fetching based on it changes semantics — clients that add a field to a selection break behavior, not just payloads; treat selection-based optimization as a contract ([[What is over-fetching and under-fetching compared with REST]]). In JS-style signatures the argument order matters (parent, args, context, info); forgetting the order makes `context` receive args — a classic bug in hand-rolled resolvers that graphql-java sidesteps by passing one environment object.

Where do the four map to real code? In graphql-java: `env.getSource()`, `env.getArguments()` / `env.getArgument(name)`, `env.getContext()`, and `env.getFieldDefinition()` / `env.getSelectionSet()` / `env.getExecutionStepInfo()`. In Spring for GraphQL, `@SchemaMapping` methods declare them as Java parameters — the framework injects `DataFetchingEnvironment` or individual pieces ([[How would you explain Spring for GraphQL]]). The four-argument contract is stable across GraphQL servers because the execution model — not the language binding — defines it.

> [!tip] Interview answer
> Resolvers get parent, args, context, info. Parent is the enclosing object value and chains nesting; args are the coerced field arguments; context is per-request shared state like auth and loaders; info is execution metadata — field definition, selection set, response path. Java servers bundle them in a DataFetchingEnvironment instead of four positional parameters, which removes the classic argument-order bug.

