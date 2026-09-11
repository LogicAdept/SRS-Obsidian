<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> When a field cannot produce a value — the resolver returned null, or it threw — but its declared type is non-null (`String!`, `[Character!]!`), the engine cannot put null there. Instead it records an error for that field, sets the field to null, and the null **bubbles up** to the nearest nullable ancestor, whose value becomes null; if there is no nullable ancestor, `data` itself is null. Siblings of the failed field still resolve.

## The walk to the nearest nullable ancestor

Nullable positions absorb the failure; non-null positions propagate it. Concretely: a null at a nullable field just appears as null in the response. A null at a non-null field is a spec violation, so the engine adds an error entry and moves the null one level up — if the enclosing object is nullable, that whole object becomes null (its siblings and other list elements survive); if that object is also non-null, it keeps bubbling ([[What is the difference between GraphQL list and non-null modifiers]]).

```java
// graphql-java 26.1, schema: hero: Character! (root), fallback: Character (nullable),
// Character.name: String! (non-null), name resolver throws.
// q1 { hero { name } } with hero resolver returning null:
// {"errors":[{"message":"The field at path '/hero' was declared as a non null type, but the code involved in retrieving data has wrongly returned a null value.  The graphql specification requires that the parent field be set to null, or if that is non nullable that it bubble up null to its parent and so on. The non-nullable type is 'Character' within parent type 'Query'","path":["hero"],"extensions":{"classification":"NullValueInNonNullableField"}}],"data":null}
// q2 { fallback { name homePlanet } } with name throwing:
// {"errors":[{"message":"Exception while fetching data (/fallback/name) : db connection lost","locations":[{"line":1,"column":14}],"path":["fallback","name"],"extensions":{"classification":"DataFetchingException"}}],"data":{"fallback":null}}
```

**Listing 1.** Verified on graphql-java 26.1. Case 1: null at a non-null root with no nullable ancestor — `data` is null. Case 2: a non-null leaf failed inside a nullable parent — the **whole object** became null, so even the successfully-resolved `homePlanet` vanished from the response.

```d2
direction: down
F: "field fails / returns null" { width: 260; height: 60 }
N: "declared nullable?" { shape: oval; width: 200; height: 55 }
Y: "field = null,\nsiblings survive" { width: 240; height: 60 }
P: "null bubbles to nearest\nnullable ancestor" { width: 300; height: 65 }
D: "no nullable ancestor ->\ndata: null" { width: 280; height: 60 }
F -> N
N -> Y: "yes"
N -> P: "no"
P -> D: "nothing absorbs it"
```

**Fig. 1.** Nullability declarations decide where failures stop: every `!` pushes the failure one level up until a nullable type absorbs it.

> [!warning] One non-null leaf can erase a whole list's payload
> The design cost of `!` shows under failure: in a list of `[Character!]!`, one element whose name resolver throws nulls that element's **parent object**, and because the element position is non-null too, the null bubbles past the list itself — potentially collapsing the entire `data` for that branch. That is why careful schemas make leaf fields nullable unless non-nullness is provable, and why "[T!]!" trade-offs belong in design review, not habit ([[What is the difference between GraphQL list and non-null modifiers]]). Second trap: an exception thrown from a resolver is *not* "an error instead of a value" that politely replaces the field — it is a failed non-null position whenever the field is declared `!`, so throwing from a `String!` resolver is a schema-wide decision ([[What does the GraphQL errors array contain]]).

Where the rule comes from: the spec's errors section defines non-null propagation exactly this way, and every compliant server behaves alike — which makes nullability a **client contract**: clients generated from a schema know a `String!` can never be null in responses, and libraries skip null checks accordingly ([[What is a GraphQL schema]]).

> [!tip] Interview answer
> Null bubbling is the engine's rule for honoring non-null types: a null or failing field at a non-null position becomes an error entry plus a null that propagates to the nearest nullable ancestor — that ancestor becomes null, siblings survive, and with no nullable ancestor the whole data is null. So one failing non-null leaf can null an entire object or branch; declare `!` only where absence is truly impossible.

