<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`!` marks non-null (returning null is a runtime error for that field). `[]` marks a list. They combine positionally; dumps say read inside-out:

- `[String]`: nullable list of nullable strings
- `[String!]`: list may be null; no element may be null
- `[String]!`: list itself cannot be null; elements may be null (or the list empty)
- `[String!]!`: non-null list of non-null elements

On arguments, `!` means the value is required. A non-null field that resolves to null propagates the error up to the nearest nullable parent, so overusing `!` can blank large response sections.

> [!warning] Unverified traps from the dump
> - Dump claim: adding `!` later on output is often treated as safe; tightening an input/argument to non-null is breaking.
