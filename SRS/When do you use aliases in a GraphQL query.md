<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Aliases rename a field in the response: `aliasName: field`. Needed when one response would collide on the same field name, most commonly querying the same field twice with different arguments (`user(id: 1)` and `user(id: 2)`).

Other dump uses: reshape keys for the frontend (`name` as `title`); disambiguate the same field fetched with different arguments or fragments.

> [!warning] Unverified traps from the dump
> - Dump claim: response keys default to the field name, not the arguments, which is why collisions happen.
