<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

# What is GraphQL

> [!abstract] Short answer
> A **query language for APIs** plus a **runtime** that executes an operation against a **schema** you define. It is not a database, not a storage engine, and not a general-purpose programming language. A service maps existing code and data onto types and fields; the client names the fields it wants; the result’s `data` map follows that selection.

## Language plus runtime, not a store

A GraphQL service publishes an application-specific **type system**. A client sends a **document**: operations (`query`, `mutation`, `subscription`) and optional fragments. The service **parses**, **validates** against the schema, then **executes** field resolvers. Tools can reject an invalid operation before any resolver runs.

GraphQL does not pick a programming language or a storage system. Resolvers may load a row, call another HTTP API, or return an in-memory object. [[Is GraphQL a database technology]] is the usual confusion.

```d2
direction: down
doc: "Document\nquery / mutation / subscription" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
schema: "Schema\ntypes, fields, root operations" {
  width: 280
  height: 80
  style.fill: "#fff3e0"
}
exec: "Execute field resolvers\nleaves are Scalar or Enum" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
resp: "Result map\ndata, maybe errors" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

doc -> schema: validate
schema -> exec
exec -> resp
```

**Fig. 1.** A request is a document checked against a schema, then executed field by field. Transport (often HTTP) is outside this picture.

```graphql
type Query {
  me: User
}

type User {
  name: String
}
```

**Listing 1.** A minimal schema: the `query` root must exist; `mutation` and `subscription` roots are optional.

```graphql
{
  me {
    name
  }
}
```

**Listing 2.** Shorthand query: omit the `query` keyword only for this operation kind. Mutations and subscriptions must name their operation type.

```json
{
  "data": {
    "me": {
      "name": "Luke Skywalker"
    }
  }
}
```

**Listing 3.** Typical JSON encoding of an execution result. The `data` tree matches the selection; this encoding is common, not required by the language.

## Schema, fields, resolvers

Every GraphQL schema must expose a **query** root object type (default name `Query`). Mutation and subscription roots are optional and, if present, must be **different** object types from each other and from query. Default names are `Query`, `Mutation`, and `Subscription`. [[What is a GraphQL schema]] and [[What is the difference between a GraphQL query a mutation and a subscription]] unpack those roots.

Each field is backed by a **resolver**. Execution starts at the chosen root, walks the selection set, and stops at Scalar or Enum leaves. Nested object fields run another selection. See [[How does the GraphQL execution engine resolve a query]] and [[What are the four arguments passed to a GraphQL resolver]].

```js
function resolveQueryMe(_parent, _args, context, _info) {
  return context.request.auth.user;
}

function resolveUserName(user, _args, context, _info) {
  return context.db.getUserFullName(user.id);
}
```

**Listing 4.** Conceptual resolvers: `me` reads the authenticated user from request context; `name` loads a string from whatever store you wired in.

Query root fields may run in parallel. Mutation root fields are expected to run **serially** because they typically have side effects. A query **may** still write data; that is a convention and a server choice, not a language ban.

Design principles that show up in interviews:

- **Hierarchical** — the request is shaped like the response.
- **Strongly typed** — validation happens against the schema.
- **Client-specified fields** — the client picks fields the schema already publishes; the service does not invent extra `data` keys for unrequested fields.
- **Self-describing** — the type system is itself queryable ([[What is GraphQL introspection]]).

[[What is the difference between GraphQL and REST]] is the comparison card; GraphQL is types and fields, not a catalog of resource URLs.

## Transport is not the language

The execution spec does **not** require a serialization format or a transport. HTTP POST to a URL that often ends in `/graphql`, with JSON `query` / `variables` / `operationName`, is the usual hosting choice ([[How do GraphQL subscriptions work over WebSockets]] for the long-lived case). GET may be offered for queries; mutations must not be executed via GET under the GraphQL-over-HTTP rules.

> [!warning] GraphQL is not “always HTTP 200 JSON from `/graphql`”
> Field failures belong in the GraphQL result (`data` plus `errors`, or a request-error result with `errors` and no `data`). HTTP status is a **separate** mapping. Partial execution can still produce `data`. Do not treat “200 forever” or “one URL is in the spec” as part of GraphQL itself. [[Why does GraphQL often return HTTP 200 when a field errors]] is that mapping.

> [!warning] Selecting fewer fields does not make resolvers cheap
> The client can avoid **over-fetching** unused JSON keys. Each selected field still runs a resolver. A list of `User` with nested `friends` can still hit the store once per parent unless you batch ([[What is the N plus 1 problem in GraphQL]]). GraphQL does not replace indexing, authorization, or query cost limits.

Schema evolution is usually additive: add fields, deprecate old ones, remove later. That is a product practice, not a guarantee that you will never break clients.

> [!tip] Interview answer
> GraphQL is a typed query language and a runtime: you publish a schema, clients send a document naming fields, the server validates then resolves those fields against your existing data. It is not a database and it is not HTTP. Query is required; mutation and subscription are optional. The JSON you see in demos is a common encoding of a result map that follows the selection set.
