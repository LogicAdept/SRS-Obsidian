<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Scalars are the leaf types: a query path ends there and you cannot sub-select fields on them. Built-ins named in dumps: Int, Float, String, Boolean, and ID (serialized as a string unique identifier).

Object types have named fields you must select. Custom scalars (DateTime, Email, URL, JSON) are used when built-ins lack validation or serialization. Dumps say you implement serialize (output), parseValue (variables), and parseLiteral (inline literals).

Clients do not learn a custom scalar's wire format from introspection alone, so dumps tell you to document the format.

> [!warning] Unverified traps from the dump
> - Dump claim: ID is a scalar, not an object; Int is described as a signed 32-bit integer in some lists.
