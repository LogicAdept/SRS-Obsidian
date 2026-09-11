<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Meta fields are fields the schema never declares but every request may select: `__typename` on **any** object, and `__schema` and `__type` on the **query root only**. `__typename` returns the runtime object type — the discriminator clients use on interfaces and unions; `__schema` and `__type` are the entry points of introspection. They cannot appear with arguments, cannot be aliased into existence elsewhere, and require no wiring.

## `__typename` everywhere, introspection at the root

Selecting `__typename` on a field returning an interface or union asks the server's type resolver which concrete type this value is; the response carries it as an ordinary key. On plain object types it names that type. On the root it names the operation type. Clients lean on it for cache normalization: without `__typename` a normalized store cannot key a polymorphic object ([[What is the difference between a GraphQL interface and a union]]).

```java
// graphql-java 26.1, union SearchResult = Movie | Person:
// { search(text:"a") { __typename ... on Movie { title } ... on Person { name } } }
// {"data":{"search":[{"__typename":"Movie","title":"A New Hope"},{"__typename":"Person","name":"Luke"}]}}
// { __typename }  ->  {"data":{"__typename":"Query"}}
```

**Listing 1.** Verified on graphql-java 26.1: the runtime type resolver decided each member; `__typename` on the root names the query type itself ([[What is GraphQL introspection]]).

`__schema` exposes the whole type system (`{ __schema { queryType { name } } }` returns the root's name); `__type(name: "Movie")` looks up one type and its fields. These two exist **only** on the query root operation type — selecting them on a nested object is a validation error. Because they are real fields, they cost execution time and response size like any other field, which is why production gateways may restrict them ([[Why disable GraphQL introspection in production]]).

> [!warning] `__typename` is type identity, not type safety
> Two traps. First: `__typename` reflects what the server's type resolver returned — a wrong or missing resolver produces a wrong member name or a runtime error, and the client's fragments simply select nothing ([[How does the GraphQL execution engine resolve a query]]). Second: do not build branching *server* logic on `__typename` or treat it as an access token; it is a serialization convenience. Also note the double-underscore namespace is reserved: user-defined type or field names starting with `__` are illegal by the spec precisely to keep meta fields collision-free ([[What is Schema Definition Language in GraphQL]]).

A subtle execution detail: `__typename` is resolved without invoking field resolvers for the object's other fields, and it is available even where the value itself would be filtered by directives — the meta field is about identity, not payload ([[What do the include skip and deprecated GraphQL directives do]]). In persisted-query setups it is a common implicit dependency: clients include `__typename` in most operations, so a persisted-query migration must preserve it in registered documents ([[What are persisted queries in GraphQL]]).

```d2
direction: down
Any: "any object field" { width: 230; height: 55 }
TN: "__typename
runtime member type" { width: 240; height: 60 }
Root: "query root only" { width: 220; height: 55 }
Sch: "__schema / __type
full introspection" { width: 260; height: 60 }
Any -> TN
Root -> Sch
``
```

**Fig. 1.** One meta field exists everywhere (__typename), the introspection pair exists only on the query root; all three are never declared in SDL.

> [!tip] Interview answer
> GraphQL has three implicit meta fields: `__typename` selectable on every object returns the runtime type — essential to discriminate interface and union members and for client cache normalization; `__schema` and `__type` live only on the query root and power introspection. The `__` prefix is reserved, meta fields take no arguments, and `__typename` is decided by the server's type resolver, so it is as correct as that resolver.

