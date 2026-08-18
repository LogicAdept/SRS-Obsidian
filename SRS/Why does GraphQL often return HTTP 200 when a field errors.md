<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

GraphQL puts field failures in a top-level `errors` array next to whatever `data` still resolved. Partial success is normal. Dumps say HTTP 200 is common because the transport request was processed; GraphQL errors are application-level. One HTTP status cannot describe mixed field success/failure.

Each error may include `message`, `path`, `locations`, and `extensions` codes. A failed field becomes null; if non-null, it bubbles.

Exceptions listed: malformed JSON, parse/validation at the edge, auth middleware — those may be 400/401. Newer GraphQL-over-HTTP mapping allows non-200; tooling has long assumed 200.

> [!warning] Unverified traps from the dump
> - Dump claim: do not treat HTTP 200 as 'no GraphQL errors'; read `errors`.
> - GraphQL-over-HTTP status rules are a separate mapping from the result map.
