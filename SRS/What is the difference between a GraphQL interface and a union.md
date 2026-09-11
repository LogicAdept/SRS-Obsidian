<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> An **interface** is a named set of fields that many object types implement; a **union** is an anonymous set of object types with *no* shared fields at all. Both make a field return one of several object types, and both force the client to use fragments with type conditions (`... on X`) to select type-specific fields — but interfaces express "shares a common shape", unions express "one of these alternatives".

## How each is declared and resolved

An interface declares fields that every implementing type must also declare (with compatible types, and implementations may add more). A union simply lists its members: `union SearchResult = Movie | Person`. There is no inheritance between unions and interfaces and no union of unions — members must be object types. On the server, fields returning either kind need a **type resolver**: given the runtime object, it names which object type this value is, so the engine knows which fragment selections apply ([[How does the GraphQL execution engine resolve a query]]). In graphql-java that is a `TypeResolver` wired on the interface or union; forgetting it fails schema construction with "There is no type resolver defined for interface / union" ([[What is the difference between schema-first and code-first GraphQL]]).

```java
// SDL: union SearchResult = Movie | Person; Query.search: [SearchResult!]!
// runtime wiring must register a TypeResolver for SearchResult:
w.type("SearchResult", w2 -> w2.typeResolver(env -> {
    Object o = env.getObject();
    return env.getSchema().getObjectType(o instanceof Movie ? "Movie" : "Person");
}));
// executing { search(text:"a") { __typename ... on Movie { title } ... on Person { name } } }:
// {"data":{"search":[{"__typename":"Movie","title":"A New Hope"},{"__typename":"Person","name":"Luke"}]}}
```

**Listing 1.** Verified on graphql-java 26.1. The type resolver discriminates members at runtime; `__typename` in the response tells the client which member each element is ([[What is the typename meta field in GraphQL]]).

On the client, `... on Movie { title }` applies `title` only to Movie objects, and a fragment spread on the interface applies to every member — for an interface the client can select common fields *without* a type condition, which is impossible for a union.

> [!warning] Unions are not enums and not tables
> Three recurring mixups. First: a union member set is fixed in the schema — a union is not "any type" and cannot span scalars or lists, only named object types. Second: adding a member to a union is a **breaking change** for clients that use exhaustive `... on` selection without a default branch, so member additions deserve the same review as argument changes ([[Which GraphQL schema changes are breaking]]). Third: choosing interface vs union is about *shared fields*, not about closeness of meaning — if two types share even one field a client always needs, an interface removes duplication; if they share nothing, forcing an interface produces a lie in the contract.

Interfaces can also extend other interfaces (spec October 2021 allows `interface X implements Y`), giving layered contracts; unions have no such composition. For federated graphs, the `Node`-style interface pattern (`Node { id: ID! }` plus a `node(id: ID!)` root field) is the standard way to fetch any entity by its global id ([[What is global object identification in GraphQL]]).

```d2
direction: right
I: "interface Node
{ id: ID! }" { width: 240; height: 70 }
A: "Movie implements
id, title" { width: 230; height: 70 }
B: "Person implements
id, name" { width: 230; height: 70 }
U: "union SearchResult
= Movie | Person" { width: 260; height: 70 }
I -> A: "common shape"
I -> B: "common shape"
U -> A: "member"
U -> B: "member"
```

**Fig. 1.** Interface members share declared fields; union members share nothing and are only alternatives resolved by a type resolver.

> [!tip] Interview answer
> Both model "a field may return several object types" and both need a server-side type resolver plus client-side typed fragments. An interface names the shared fields every implementer must provide, so clients can select them unconditionally; a union has no shared fields and is pure "one of these objects". Choose interface for common shape, union for alternatives — and remember adding a union member breaks clients that select exhaustively.

