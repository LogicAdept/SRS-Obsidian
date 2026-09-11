<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS

> [!abstract] Short answer
> A change is breaking when any **valid previous request would fail or change meaning** afterward: removing or renaming a field/type/argument, changing a field's return type to a narrower one, adding a required argument, adding non-null where clients saw null, changing enum value sets, or adding union members and interface implementations that client `... on` branches didn't handle. Additive changes — new optional fields, new types, deprecation markers — are safe. The test is mechanical, which is why registries diff schemas automatically.

## The breaking-change taxonomy, precisely

On the **output** side: removing a field; renaming; narrowing a return type (`String` to `String!`, `[Char]!` to `[Char!]!` — any position where clients tolerated null now fails harder); changing a scalar to another type; removing enum values; adding members to a **union** (exhaustive client selections break even though the change looks additive) ([[What is the difference between a GraphQL interface and a union]]). On the **input** side: adding a **required** argument (existing calls lack it); removing an argument clients pass; making an input field required; removing enum values used as inputs; changing argument defaults in meaning-changing ways ([[How do you pass arguments to a GraphQL field]]).

The subtle class: **behavioral** breaking under a stable schema — a nullable leaf becoming effectively non-null at runtime, cursor format changes, filter semantics — passes schema diff but changes responses; registries flag the syntactic class, humans review semantics ([[How do you version a GraphQL schema]]).

```graphql
# BEFORE                          # AFTER (classified)
type Query {                      type Query {
  users(first: Int): [User]         users(first: Int!): [User!]!   # BREAKING: type narrowed,
}                                                                    argument required
type User {                       type User {
  name: String                      name: String!                 # BREAKING: null seen -> now fails
  email: String                     email: String @deprecated     # SAFE: marker only
  phone: String                     phone: String                 # then removal = BREAKING
}                                 }
enum Role {                       enum Role {
  ADMIN                             ADMIN
  USER                              USER
                                    GUEST                          # SAFE on output-side fields;
}                                                                  # BREAKING if used as input value
```

**Listing 1.** The diff-driven view: same schema before and after, each line classified by what previously-valid requests would do ([[What is the difference between GraphQL list and non-null modifiers]]).

```d2
direction: down
C: "schema change" { width: 200; height: 55 }
Safe: "additive:\nnew optional field, new type,\ndeprecation marker" { width: 330; height: 70 }
Brk: "contract-affecting:\nremove/rename/narrow/\nrequire/enum & union members" { width: 340; height: 75 }
D: "diff gates CI" { width: 190; height: 55 }
M: "migrate + retire" { width: 220; height: 55 }
C -> Safe
C -> Brk
Brk -> D: "registry classifies"
Safe -> M
D -> M
```

**Fig. 1.** Every change is either additive or contract-affecting; registries mechanize the classification so reviews argue about semantics, not syntax.

> [!warning] "We only added a field" is not a safety proof
> The traps that pass naive review. First: adding a union member or an interface implementation **looks** additive but breaks clients whose selections were exhaustive — their typed fragments miss the new member ([[What is the difference between a GraphQL interface and a union]]). Second: adding a required argument breaks every existing call site the moment the schema deploys — "required with default" is the additive variant ([[How do you pass arguments to a GraphQL field]]). Third: nullability tightening (`String` to `String!`) turns previously-successful responses into null-bubbling failures — the schema promised nothing before and promises everything now ([[How does null bubbling work when a GraphQL field is null]]). Fourth: input-side enum additions break clients that *send* unknown values? No — they break clients that *validate locally* against the old set; server-side, new input values are safe for readers but not for stored-enum round-trips.

> [!tip] Interview answer
> Anything that fails a previously-valid request is breaking: removals, renames, return-type narrowing, newly required arguments, output non-null tightening, enum value removals, and union/interface member additions. Additive means new optional surface plus deprecation markers. Registries diff old versus new schemas and classify mechanically; humans then own behavioral changes the diff cannot see — cursor semantics, filter meanings.

