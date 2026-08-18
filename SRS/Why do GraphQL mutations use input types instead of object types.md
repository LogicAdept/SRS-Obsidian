<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Input types (`input`, not `type`) are for arguments, especially mutation payloads. GraphQL dumps say you cannot reuse output object types as arguments: output types may have resolved relations, interfaces, unions, or computed fields a client cannot send.

Input fields may only be scalars, enums, or other input types: no resolvers, no interfaces/unions. Bundling args into one `CreateUserInput` keeps the mutation signature evolvable.

Dumps also like returning a payload type (entity plus `userErrors`) rather than a bare entity.

> [!warning] Unverified traps from the dump
> - Dump claim: output `User` and input `UserInput` are different kinds even if fields look similar.
