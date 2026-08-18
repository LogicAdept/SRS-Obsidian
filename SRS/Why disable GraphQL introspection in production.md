<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: introspection hands a full map of types and fields to anyone who can query `__schema`. That eases discovery of undocumented, experimental, or sensitive fields.

It is not a substitute for authorization. Typical dump advice: disable or gate introspection in production; still check permissions on every field; optionally keep it in staging or behind auth.

> [!warning] Unverified traps from the dump
> - Dump claim: disabling introspection is security-through-reduced-exposure, not real access control.
