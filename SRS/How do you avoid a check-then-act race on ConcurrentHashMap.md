<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: do **not** `containsKey` then `put` / `get`. Use **`computeIfAbsent`** or **`putIfAbsent`**. A cache dump lists the same bug: `containsKey` + `get` → `computeIfAbsent`.

Compilation dumps: `putIfAbsent(k, v)` inserts only if absent; `computeIfAbsent(k, f)` computes once if missing. `HashMap.putIfAbsent` is not thread-safe just because the method exists.

> [!warning] Unverified traps from the dump
> - Thread-safe **per call** is not thread-safe **per sequence**.
> - `putIfAbsent` still stores a pre-built value; dumps prefer `computeIfAbsent` when the value is expensive to create.
