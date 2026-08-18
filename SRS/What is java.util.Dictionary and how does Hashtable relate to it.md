<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `java.util.Dictionary` is an **abstract** class for a key–value relation, similar to a map. Keys and values are objects and **must not be null**; inserting a null key or value causes `NullPointerException`.

The dump’s example constructs `Dictionary dictionary = new Hashtable();` and walks `dictionary.elements()` / `dictionary.keys()` with `Enumeration`.

HashMap-vs-Hashtable tables: **`Hashtable` inherits `Dictionary`**; **`HashMap` inherits `AbstractMap`**.

> [!warning] Unverified traps from the dump
> - `Dictionary` is not the `Map` interface.
> - The same dumps still show `Hashtable` as the concrete `Dictionary` while calling `Hashtable` legacy.
