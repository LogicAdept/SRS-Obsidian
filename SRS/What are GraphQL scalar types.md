<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> Scalar types are the **leaves** of a schema: fields whose results have no sub-selection. GraphQL defines five built-in scalars — `Int`, `Float`, `String`, `Boolean`, and `ID` — and lets a service define custom scalars with its own serialization rules. Every query execution bottoms out at scalars: object fields recurse, scalar fields resolve to values.

## The five built-ins and what they guarantee

`Int` is a signed 32-bit integer, `Float` a double-precision value, `String` UTF-8 text, `Boolean` true/false. `ID` looks like `String` or `Int` on the wire but semantically means "a unique identifier that must not be treated as human-readable text" — it exists so clients serialize and cache it as an opaque key ([[What is global object identification in GraphQL]]). The spec requires these five to be present in every schema; anything else is a custom addition ([[What is a GraphQL schema]]).

```graphql
type Character {
  id: ID!
  name: String!
  height: Float
  mass: Int
  human: Boolean
}
```

**Listing 1.** Nullable scalars (`Float`, `Int`) may be absent; the non-null wrappers (`ID!`, `String!`) must always produce a value.

Each scalar is defined by three runtime operations: **serialize** (internal value to response), **parseValue** (a JSON variable into an internal value), and **parseLiteral** (an inline literal in the query text). That triple is exactly what a custom scalar implements — for example a `DateTime` that serializes an `Instant` to an ISO string, parses a JSON string variable into `Instant`, and parses the same literal inside a request document ([[What are the four arguments passed to a GraphQL resolver]]).

> [!warning] Custom scalars have no schema-level validation
> A custom scalar is only as strict as its parse functions. Nothing in SDL can say "this String is really an email" — if `parseValue` accepts any string, invalid data flows into resolvers. The standard countermeasures are strict parse implementations (reject at the boundary) or making the field an object type with validated fields. And beware the arithmetic trap: `Int` is 32-bit, so large counts (files over ~2 GB, nanosecond timestamps) silently need `Float`, `String`, or a custom scalar ([[What are the two fundamental relational data integrity types]]).

Enums are the other leaf kind and are **not** scalars: an enum is a finite set of named values, serialized by name, while a scalar accepts any value its coercion allows ([[What is an Enum type in GraphQL]]). In graphql-java an SDL-defined enum arrives in a resolver as its name string by default, and a value outside the set fails validation before execution.

Where do resolvers see scalars? As argument values (`env.getArgument("minId")` returns `Integer`) and as field results. In graphql-java 26.1, executing `{ character(id: "1000") { name } }` against a `Character` record produces `{"data":{"character":{"name":"Luke Skywalker"}}}` — execution stopped at the scalar leaf and serialized the record component ([[How does the GraphQL execution engine resolve a query]]).

```d2
direction: down
Field: "Object field" { width: 230; height: 60 }
Leaf: "Scalar leaf
Int, Float, String, Boolean, ID" { width: 300; height: 70 }
Val: "serialize / parseValue / parseLiteral" { width: 330; height: 70 }
Field -> Leaf: "selection ends"
Leaf -> Val: "coercion contract"
```

**Fig. 1.** Every branch bottoms out at a scalar; the coercion triple defines how values cross the JSON boundary in both directions.

> [!tip] Interview answer
> Scalars are leaf types — `Int`, `Float`, `String`, `Boolean`, `ID` are required, custom ones (DateTime, Long, Email) are defined by serialize/parseValue/parseLiteral. `ID` is intentionally opaque: same wire format as String, but clients must treat it as an opaque key. Enums look similar but are a closed set of names, not free values, and `Int` is 32-bit — a classic pitfall for big numbers.

