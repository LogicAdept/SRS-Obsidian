<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The Schema Definition Language (SDL) is GraphQL's human-readable, language-agnostic syntax for describing the schema: types, fields, and operations that form the client/server contract.

It drives introspection, validation, autocomplete, docs, and codegen. The same SDL can back a server written in any language; resolvers supply behavior. In code-first setups the SDL is generated rather than handwritten, but dumps still treat it as the published contract.

Example shape from dumps:

```
type Query { user(id: ID!): User }
type User { id: ID! name: String! email: String }
```

> [!warning] Unverified traps from the dump
> - Dump claim: schema-first writes SDL by hand; code-first generates it. Either way SDL is the published contract.
