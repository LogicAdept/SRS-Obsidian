<!--
reps: 0
priority: 0
-->
#API/GraphQL #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

If a non-null field (`Type!`) resolves to null or throws, dumps say the error bubbles to the nearest nullable parent: that parent becomes null and the failed field is listed in `errors` with a `path`. A nullable field can be null without wiping the parent.

Over-marking fields `!` means one failed leaf can null a whole object or the entire `data` tree. Guidance in dumps: use `!` only when you can guarantee the value (for example `id`); leave fields nullable when they depend on optional data or other services.

> [!warning] Unverified traps from the dump
> - Dump claim: 'I default to nullable and earn non-null' is the interview phrasing some lists want.
