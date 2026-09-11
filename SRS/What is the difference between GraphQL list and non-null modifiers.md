<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> `[T]` is the **list** wrapper; `T!` is the **non-null** wrapper; they compose to build four distinct types: `[T]`, `[T]!`, `[T!]`, `[T!]!`. The exclamation mark changes where null may appear: `T!` forbids a null *element result*, `[T]!` forbids a null *list result*, and `[T!]` forbids null *inside* the list while the list itself may be null. Reading the type from the inside out gives the exact nullability contract.

## The four combinations

For an element type `T`:

- `[T]` — the list itself may be null, and any element may be null: `null` or `[null, T]` are valid.
- `[T]!` — the list must be present (never null), but it may contain nulls: `[null]` is valid.
- `[T!]` — the list may be null, but if present, no element may be null: `[T]` only.
- `[T!]!` — the list must be present and every element must be present. This is the idiomatic "always answer with a list, possibly empty" type.

The empty list is a *value*, not a null: `[T!]!` fields return `[]` when nothing matched, which is why that combination dominates real schemas — clients can iterate without null checks ([[What is a GraphQL schema]]).

```graphql
type Query {
  a: [Int]      # null or [1, null]
  b: [Int]!     # [1, null] — list always, elements optional
  c: [Int!]     # null or [1, 2] — elements always
  d: [Int!]!    # [1, 2] or [] — always a list, never a null element
}
```

**Listing 1.** The four wrappings of the same element type; only `d` guarantees iteration safety.

## The execution twist: non-null propagates failures

The sharp interview point is what happens at runtime when a resolver *fails* or returns null. A null reaching a non-null position is not silently passed through: the field gets an error entry and null **bubbles** to the nearest nullable ancestor, which may discard a whole object or the entire data section ([[How does null bubbling work when a GraphQL field is null]]). So `[Int]!` means a failed element becomes `null` *inside* the list — the list survives. `[Int!]!` means one failed element nulls its **parent object**, potentially collapsing the whole list. Declaring `[T!]!` is therefore also a reliability decision: it says "one bad row aborts the response", which for large lists is usually not what you want ([[Why does GraphQL often return HTTP 200 when a field errors]]).

> [!warning] Input positions mean the opposite direction
> The same wrapper in an argument or input-object field describes what the *client* must send: `first: Int` may be omitted; `first: Int!` is required. The asymmetry trap: on output, `!` is a promise the server makes; on input, it is a demand on the caller. And `[T]!` on an argument still allows the client to send `[null]` — only `[T!]` forbids null elements ([[How do you pass arguments to a GraphQL field]]).

```java
// graphql-java 26.1, schema field "friends: [User!]!" where one friend's name fetch throws:
// {"errors":[{"message":"Exception while fetching data (/user/friends/1/name) : db down",
//   "path":["user","friends",1,"name"],"extensions":{"classification":"DataFetchingException"}}],
//  "data":{"user":null}}
// the element failure nulled the parent object, and [User!]! bubbled that null to "user".
```

**Listing 2.** One non-null element failing removed the entire list's parent — the price of `[T!]!`.

```d2
direction: down
L: "[T]! list required" { width: 250; height: 60 }
E: "[T!] elements required" { width: 250; height: 60 }
Both: "[T!]! both promises" { width: 250; height: 60 }
Fail: "one element fails" { shape: oval; width: 230; height: 55 }
Bubble: "null bubbles to nearest
nullable ancestor" { width: 300; height: 70 }
E -> Both: "compose"
L -> Both: "compose"
Both -> Fail: "runtime"
Fail -> Bubble
```

**Fig. 1.** Wrappers compose, but at runtime a failure under a non-null wrapper bubbles past it — the promise is enforced by propagation, not by masking.

> [!tip] Interview answer
> Read wrappings inside out: `!` forbids null at its position. `[T]` allows nulls anywhere, `[T]!` promises the list, `[T!]` promises the elements, `[T!]!` promises both. On output the promise is enforced by null bubbling — one failing element under `[T!]` can kill the parent object — so `[T!]!` trades resilience for iteration safety. On input the same `!` becomes a requirement on the client.

