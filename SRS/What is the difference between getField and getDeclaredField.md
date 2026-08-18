<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps:

- `getField` / `getFields` — **public** members, including inherited.
- `getDeclaredField` / `getDeclaredFields` — members **declared on this class**, all visibilities, **not** inherited.

Private access: `getDeclaredField("name")`, then `setAccessible(true)`, then `get` / `set`.

The vault already has a Language-tagged dump of the private-field recipe: Can object get access to member class declared how private if yes what way.

> [!warning] Unverified traps from the dump
> - `getField` will not see a private field; that is a common interview miss.
