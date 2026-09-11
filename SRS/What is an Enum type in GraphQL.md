<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> An Enum type is a **closed set of named values** declared in the schema: `enum Episode { NEWHOPE EMPIRE JEDI }`. A field or argument of that type accepts only one of those names — nothing else passes validation. Enums are leaves like scalars, but opposite in spirit: a scalar allows any value its coercion accepts, an enum allows exactly the declared names, serialized bare (no quotes) in documents and as their name strings in JSON responses.

## Mechanics that interviews probe

Enum values are written as unquoted names in request documents and as unquoted names in SDL — `hero(episode: EMPIRE)`, never `hero(episode: "EMPIRE")` for a real enum argument. In the JSON response the enum serializes as a string ("EMPIRE"), because JSON has no enum literal; the name is the contract. An enum can also declare a **default value** for an argument (`episode: Episode = NEWHOPE`), applied when the client omits it.

Enums are also valid **input** values for input objects and directive arguments, and they can carry `@deprecated` per value — the schema-level way to retire one member without breaking the whole type ([[Which GraphQL schema changes are breaking]]).

```java
// SDL: enum Episode { NEWHOPE EMPIRE JEDI }
// and type Query { hero(episode: Episode = NEWHOPE): String }
String ep = env.getArgument("episode"); // default coercion: enum name as String
// hero(episode: EMPIRE)   -> "Han Solo"
// hero                    -> "Luke Skywalker"  (SDL default applied)
// hero(episode: PREQUEL)  -> validation error before execution:
// {"errors":[{"message":"Validation error (WrongType@[hero]) : argument 'episode' with value 'EnumValue{name='PREQUEL'}' is not a valid 'Episode' - Literal value not in allowable values for enum 'Episode' - 'EnumValue{name='PREQUEL'}'","locations":[{"line":1,"column":8}],"extensions":{"classification":"ValidationError"}}]}
```

**Listing 1.** Verified on graphql-java 26.1. An SDL-generated enum arrives in a resolver as its name string unless the wiring explicitly maps it to a Java enum; an unknown value is a `ValidationError`, not a resolver error.

> [!warning] Enum names are identifiers, not strings
> Enum members must be GraphQL names — no spaces, no leading digits — and they cannot collide with the reserved names `true`, `false`, and `null`. The classic design smell is treating enums as lookup tables with dozens of members or internal numeric codes: the wire contract is the *name*, so adding a member is safe, renaming one is breaking, and mapping numeric codes onto enum names belongs in the runtime layer, not in the schema ([[What are GraphQL scalar types]]).

The Java mapping is a detail worth stating precisely. Generated from SDL, a `GraphQLEnumType` coerces input literals to the enum's name string; to get real Java enum constants you either define the enum type in code with `GraphQLEnumType.newEnum().value("EMPIRE", Episode.EMPIRE)` or convert in the resolver. Spring for GraphQL does not change this: annotations receive whatever coercion produced ([[How would you explain Spring for GraphQL]]).

Use an enum when the set is small, stable, and semantic (order state, episode list). Use a scalar or a reference by `ID` when the set is large or grows with data — enums are schema text, so "one enum member per row in the database" would make every data change a schema deployment ([[Is GraphQL a database technology]]).

```d2
direction: down
Doc: "hero(episode: EMPIRE)" { width: 260; height: 60 }
V: "Validation against enum" { width: 260; height: 60 }
R: "Resolver receives value
(name string by default)" { width: 280; height: 70 }
Err: "ValidationError,
no execution" { width: 260; height: 60 }
Doc -> V: "EMPIRE in set?"
V -> R: "yes"
V -> Err: "no"
```

**Fig. 1.** An enum argument outside the declared set fails validation before any resolver runs; a valid name is passed to the resolver.

> [!tip] Interview answer
> An enum is a finite, named value set: validated before execution, serialized by name, written bare in documents, and deprecatable per value. It differs from scalars (free values under a coercion) and from ID strings (no closed set). In resolvers expect the name string unless wiring maps it to a Java enum. Choose enums for small stable taxonomies, never for database-row-sized sets.

