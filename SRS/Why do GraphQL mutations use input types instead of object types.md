<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Mutation arguments are **input values** — data the client *sends* — and the type system enforces that split: only scalars, enums, and other input objects (`input PostInput { ... }`) are legal argument types. Output object types are the other kind: their fields are backed by resolvers and may include lists, interfaces, unions, and computed relations that no client could ever serialize *into* an argument. Separate `input` types make the write contract explicit, evolvable, and statically validated.

## Two kinds of types, one grammar

GraphQL types divide into **input types** (appear where values flow client-to-server: arguments, input-object fields, variable declarations) and **output types** (appear where values flow server-to-client: field results). Object types are output-only; input objects are input-only; scalars and enums serve both. An input object cannot contain: fields with arguments, non-scalar relations, interfaces or unions — none of that can arrive as client data. Conversely an output type cannot be an argument even if every field "looks serializable", because output fields are *resolver-backed behavior*, not data ([[What is Schema Definition Language in GraphQL]]).

```graphql
type Mutation {
  createPost(input: PostInput!): CreatePostPayload!
}

input PostInput {
  title: String!
  tags: [String!]
}

type CreatePostPayload {
  id: ID!
  title: String!
}
```

**Listing 1.** The idiomatic mutation shape: one input object bundles all writable fields; the payload type returns the created entity's identity and fields.

At runtime the input object arrives as a coerced map. Verified on graphql-java 26.1 with `mutation M($in: PostInput!) { c: createPost(input: $in) { id title } }` and variables `{in: {title: "Hello", tags: ["api"]}}`: the resolver read `env.getArgument("input")` as `Map` — `RUN createPost title=Hello tags=[api]` — and returned the payload; the result was `{"data":{"c":{"id":"p42","title":"Hello"}}}` ([[What are the four arguments passed to a GraphQL resolver]]). Validation covers the whole input tree before execution: unknown input fields, wrong types, and missing required input fields are `ValidationError`s — mutations cannot receive malformed payloads ([[How do you pass arguments to a GraphQL field]]).

```d2
direction: down
C: "client sends\nvariables: PostInput" { width: 260; height: 65 }
In: "input PostInput\nscalars, enums, nested inputs" { width: 310; height: 65 }
V: "statically validated\nunknown field -> error" { width: 290; height: 60 }
R: "resolver: Map -> store" { width: 230; height: 55 }
P: "CreatePostPayload\noutput type back" { width: 260; height: 60 }
C -> In -> V -> R -> P
```

**Fig. 1.** The write path: input types in one direction, validation at the boundary, a payload type back — never the same type serving both directions.

> [!warning] Input types are a contract device, not just syntax policing
> Three design points. First: **evolution** — bundling arguments into one `input` object lets you add optional fields without touching the mutation's signature; adding a second positional argument to an existing mutation is a breaking change, adding a field to its input object is not ([[Which GraphQL schema changes are breaking]]). Second: **do not mirror the entity** — a `User` output type with 40 fields does not imply `UserInput` with the same 40; inputs should expose exactly what is writable, with server-controlled fields (ids, audit stamps, computed values) absent — that is the point of the boundary ([[Is GraphQL a database technology]]). Third: the **payload pattern** — returning a wrapper type with the entity plus `userErrors` treats expected business failures (duplicate email) as data instead of exceptions; reserve the `errors` array for genuine failures, and keep that convention consistent across mutations ([[What does the GraphQL errors array contain]]).

A related trap: input objects are **structurally validated but semantically opaque** — the type system cannot express "endDate after startDate"; cross-field rules belong in the resolver or a custom scalar/domain layer, and the payload-vs-error convention decides how violations surface ([[How does null bubbling work when a GraphQL field is null]]).

> [!tip] Interview answer
> Mutations take input types because GraphQL splits types by flow direction: input objects (scalars, enums, nested inputs only) travel client-to-server and are fully validated before execution; object types are resolver-backed output and cannot be sent. One input object per mutation keeps the signature additive and evolvable, inputs should expose writable fields only, and business failures are best returned as payload `userErrors` rather than exceptions.

