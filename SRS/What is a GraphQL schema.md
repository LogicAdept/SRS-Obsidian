<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> A GraphQL schema is the **typed contract** of a service: it defines every type, every field, each field's argument and result types, and the root operation types the client can enter through. It is the single source of truth for validation — a request is rejected before execution if it names a field or argument the schema does not expose — and for tooling, because the schema is queryable through introspection.

## What the schema actually contains

An executable schema is built from two halves. The **type definitions** describe the shape: object types with their fields, the built-in scalars (`Int`, `Float`, `String`, `Boolean`, `ID`), custom scalars, enums, lists and non-null wrappers, input object types for arguments, interfaces and unions for polymorphism, and directives ([[What is Schema Definition Language in GraphQL]]). The **runtime wiring** attaches a resolver (a `DataFetcher` in graphql-java terms) to every field that needs one; a field without an explicit resolver falls back to property lookup ([[How does a default GraphQL resolver work]]).

Every schema must expose exactly one **query root** (default name `Query`). A **mutation** root and a **subscription** root are optional, and each of the three must be a distinct object type — you cannot reuse one type as two roots. Execution always starts at one of these roots and walks the selection set; object branches recurse, scalars and enums terminate ([[How does the GraphQL execution engine resolve a query]]).

```graphql
schema {
  query: Query
  mutation: Mutation
}

type Query {
  character(id: ID!): Character
}

type Character {
  id: ID!
  name: String!
  friends: [Character!]!
}
```

**Listing 1.** The `schema` block is only needed to rename the roots; with default names `Query`/`Mutation`/`Subscription` it is omitted.

## Why the contract model matters

Validation is a separate phase from execution. Because the schema knows every field signature, the server can reject unknown fields, wrong argument types, and invalid enum values **before any resolver runs** — an invalid request costs the server almost nothing ([[What are the four arguments passed to a GraphQL resolver]]). The same property powers tooling: clients generate typed code from the schema, IDEs autocomplete, and diff tools classify a schema change as safe or breaking ([[Which GraphQL schema changes are breaking]]).

> [!warning] The schema is not your database model
> A common trap is to map tables one-to-one onto schema types. The schema is an **application-facing API**: you may merge two tables into one type, hide internal columns, expose computed fields, or split one aggregate across types. Anything you do not put into the schema simply cannot be fetched — which is why leaking an internal field through the schema is a design failure, not a runtime bug ([[Is GraphQL a database technology]]).

Another practical consequence: circular references like `Character.friends: [Character!]!` are legal and normal in schemas, while recursive value cycles in JSON would break serialization. The engine handles the recursion because it executes only the fields the client selected, one level of resolvers at a time.

```d2
direction: down
Query: "Query root
(mandatory)" { width: 240; height: 70 }
Character: "Character
object type" { width: 240; height: 70 }
Scalars: "Scalar leaves
ID, String" { width: 240; height: 70 }
Query -> Character: "character(id: ID!)"
Character -> Scalars: "id, name"
```

**Fig. 1.** Execution enters through the mandatory query root, walks object fields, and stops at scalar leaves; mutation and subscription roots would sit beside Query.

> [!tip] Interview answer
> A schema is the typed contract: all types and fields with their argument and result types, plus the mandatory query root and optional mutation and subscription roots. It is built from SDL type definitions plus runtime wiring that binds resolvers to fields. Validation runs against it before execution, and introspection makes it self-describing, which is what powers tooling and typed clients.

