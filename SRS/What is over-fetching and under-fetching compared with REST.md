<!--
reps: 0
priority: 0
-->
#API/GraphQL #API/REST #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Over-fetching is getting more data than the UI needs (a REST `/users/1` returning address and bio when only name is shown). Under-fetching is getting too little, forcing extra requests (`/users/1` then `/users/1/posts`).

Dumps say GraphQL addresses both by letting the client select fields and nest related selections in one query. Caveat in the same lists: unused JSON keys can shrink while the server still over-fetches in resolvers unless you batch (DataLoader) and select columns carefully.

> [!warning] Unverified traps from the dump
> - Dump claim: nested GraphQL is not free; N+1 database hits are a separate problem from HTTP under-fetching.
