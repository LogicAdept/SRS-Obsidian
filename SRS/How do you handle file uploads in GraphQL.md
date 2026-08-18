<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the spec is JSON-like text; there is no native file type.

Multipart GraphQL request: `multipart/form-data` with `operations` JSON, a map from files to variable paths, and binary parts. Servers expose an `Upload` scalar (graphql-upload / Apollo integrations).

Out-of-band (often preferred in the same dumps): mutation returns a signed URL (S3/GCS); client PUTs the file; another mutation stores the key. Keeps binaries off the GraphQL process.

Base64 in a String is listed as OK only for tiny files (~33% bloat). Multipart breaks pure-JSON caching and complicates batching.

> [!warning] Unverified traps from the dump
> - Dump claim: signed-URL upload is often preferred at scale over stuffing files through GraphQL.
