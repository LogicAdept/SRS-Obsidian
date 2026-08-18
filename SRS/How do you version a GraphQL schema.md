<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps favor versionless evolution, not `/v2` URLs. Add fields and types; mark old fields `@deprecated(reason: "...")` instead of deleting. Clients request only the fields they use, so additive changes do not break existing queries.

REST needs versions more often because endpoints return a fixed payload. Monitor field usage, then remove after clients migrate. Field aliases are sometimes listed for major renames.

> [!warning] Unverified traps from the dump
> - Dump claim: adding fields is non-breaking; removing or renaming is the breaking act.
