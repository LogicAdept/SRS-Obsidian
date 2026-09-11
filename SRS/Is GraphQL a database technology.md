<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> No. GraphQL is a **query language for APIs** plus a runtime for executing those queries against your existing code and data. It has no storage engine, no indexing, no query planner over tables, no persistence — a GraphQL service is a thin, strongly typed layer that maps incoming selections onto whatever backends you already have: SQL databases, caches, other HTTP services, in-memory objects.

## Why the confusion is persistent

The schema *looks* like a database description: types, fields, relations, even "queries". But three properties separate them decisively. First, a schema describes an **application surface**, not storage: fields may be computed, aggregated across services, or renamed for clients — nothing in GraphQL stores anything ([[What is a GraphQL schema]]). Second, execution is **resolver-driven**: each field calls ordinary application code; the language has no notion of tables, joins, or indexes — cross-entity "joins" happen because a resolver calls a store, not because the engine plans an access path ([[How does the GraphQL execution engine resolve a query]]). Third, the runtime is agnostic to transport and serialization — properties no database owns ([[What is Schema Definition Language in GraphQL]]).

```graphql
type Character {
  id: ID!
  name: String!
  friends: [Character!]!
}
```

**Listing 1.** `friends` looks like a self-referential relation — but its resolver may call a graph store, a SQL join, or another microservice. The schema cannot tell you, and does not care.

```d2
direction: down
C: "Client document" { width: 200; height: 55 }
G: "GraphQL layer\nschema + resolvers" { width: 240; height: 65 }
S1: "SQL database" { width: 190; height: 55 }
S2: "cache" { width: 150; height: 50 }
S3: "HTTP services" { width: 190; height: 55 }
C -> G
G -> S1
G -> S2
G -> S3
```

**Fig. 1.** The GraphQL layer sits above arbitrary backends; it composes and shapes data, it never owns it.

> [!warning] The API layer cannot replace what databases guarantee
> Interviews surface this as follow-ups. Without a query planner there are no access paths: a "join" through resolvers is N+1 unless you batch explicitly — the database's job you now do in application code ([[What is the N plus 1 problem in GraphQL]]). There is no transactional scope across resolvers: a mutation touching two stores has no atomicity from GraphQL itself ([[What is the difference between a GraphQL query a mutation and a subscription]]). And filtering, sorting, and pagination are **not built in**: the schema decides what arguments like `filter` or `first` mean per field; the language provides no WHERE/ORDER BY — you design it ([[How do you paginate a GraphQL list]]).

The flip side of "not a database" is the honest boundary of the claim: GraphQL *servers* may sit directly on a database, and some products (Hasura, PostGraphile) auto-generate resolvers from tables — but that is an integration choice; the language itself stays storage-agnostic ([[Is GraphQL a database technology]]). When a candidate answers "it's a database for your frontend", the precise correction is: it is a typed contract plus a resolver runtime that moves the last-mile data shaping from the backend into the API layer — with all the engineering obligations that move entails ([[What is over-fetching and under-fetching compared with REST]]).

> [!tip] Interview answer
> GraphQL is a query language for APIs plus a runtime: schemas describe what clients may ask, resolvers map fields onto existing code and stores — SQL, caches, services. It stores nothing, plans nothing, and guarantees no transactions or indexes; filtering, sorting, and joins are application code. Databases expose storage; GraphQL exposes an application-shaped view above it.

