<!--
reps: 0
priority: 0
-->
#Java/Collections/Unmodifiable #SRS #New

> [!warning] Untrusted draft
> Text copied from an external question dump. Not checked against official documentation. Do not treat as a review answer.

**How do you obtain a read-only / unmodifiable collection?**

- `Collections.unmodifiableList(list)`
- `Collections.unmodifiableSet(set)`
- `Collections.unmodifiableMap(map)`

These wrap the argument and return a read-only view of the same elements.
