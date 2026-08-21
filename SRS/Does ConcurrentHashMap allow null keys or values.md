<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/ConcurrentHashMap #Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **neither.** No null key or value. `put` of null throws **`NullPointerException`**. `HashMap` allows one null key and null values.

Compilation dumps: in a concurrent map, `get` returning null would be ambiguous (absent vs mapped to null). You cannot disambiguate with `containsKey` then `get`, because another thread can change the mapping between the two calls. Banning nulls makes a null `get` mean **absent**.

> [!warning] Unverified traps from the dump
> - “No nulls” is shared with `Hashtable` in other tables; the ambiguity story is the concurrent-map reason dumps add.
> - `computeIfAbsent` dumps assume “current value is null” means absent.
