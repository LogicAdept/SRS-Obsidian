<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Global Object Identification is the Relay-originated convention for addressing objects **uniquely across the whole API**: every identified type implements the `Node` interface (`id: ID!`), ids are globally unique — typically an opaque Base64 of `TypeName:rawId` — and the schema exposes one root field `node(id: ID!): Node` plus a `nodes(ids: [ID!]!)` variant. Clients refetch or cache any object by its id alone, without knowing which field originally produced it.

## The contract and why clients want it

Two rules make it work. First, the `id` is an **opaque global key**: clients must not parse it (the Base64-of-type-and-id encoding is a common implementation, not a client contract); the server maps a global id back to type and row. Second, `node(id)` is a **universal entry point**: given any node id, the server resolves the type — via the same type-resolver machinery interfaces use — and returns it typed, so the client selects fields with typed fragments ([[What is the difference between a GraphQL interface and a union]]).

```graphql
interface Node {
  id: ID!
}

type Character implements Node {
  id: ID!
  name: String!
}

type Query {
  node(id: ID!): Node
  nodes(ids: [ID!]!): [Node]!
}
```

**Listing 1.** The whole convention in SDL: one interface, one root refetch field. Combined with connections this is the backbone Relay expects ([[How do you paginate a GraphQL list]]).

```d2
direction: down
Id: "id = Base64(\"Character:1000\")" { width: 300; height: 60 }
N: "Query.node(id)" { width: 190; height: 55 }
T: "type resolver -> Character" { width: 280; height: 60 }
F: "client selects ... on Character" { width: 300; height: 60 }
Id -> N
N -> T
T -> F
```

**Fig. 1.** A global id enters through `node`, the type resolver names the concrete type, and the client's typed fragments shape the result — one refetch path for every object kind.

> [!warning] The id is opaque — on both sides
> Three practical rules. First: clients must treat `ID` as a **black box** — encoding `Character:1000` client-side or assuming a format couples them to internals; the spec's `ID` type exists precisely to make ids opaque strings ([[What are GraphQL scalar types]]). Second: ids must be **globally unique**, which is why the type name goes *inside* the encoding — two tables with colliding numeric ids would otherwise alias each other through `node` ([[What is the difference between PRIMARY KEY and UNIQUE]]). Third: security follows the id: `node(id)` is a **direct object reference**, so the resolver must authorize against the caller — leaking internal numeric ids in the clear also aids enumeration ([[How do you authenticate and authorize a GraphQL request]]).

What it buys: normalized client caches key objects by `Type:id` and can dedupe, update, and refetch any entity from anywhere — the cache contract of Relay and most Apollo setups; single-item refetch after a mutation without re-running the original query; and a uniform place to hang per-object permissions ([[What is the typename meta field in GraphQL]]). The cost is real but bounded: implementers wire a type resolver and an id codec, and add the `node` root — engineering-wise the cheapest convention in the GraphQL ecosystem relative to its payoff ([[What is GraphQL introspection]]).

> [!tip] Interview answer
> Global Object Identification standardizes object identity: `Node { id: ID! }`, globally unique opaque ids (commonly Base64 of Type:id), and a `node(id)` root field that returns any object by id, resolved to its concrete type. Clients get one refetch path and stable cache keys; the server must authorize direct references and keep the encoding internal. Connections plus Node is the full Relay contract.

