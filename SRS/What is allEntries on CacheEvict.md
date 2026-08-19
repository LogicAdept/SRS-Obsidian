<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`allEntries = true` clears every entry in the named cache, not one key. Example: empty `clearBooksCache()` used only to wipe `books`.

> [!warning] Unverified traps from the dump
> - Expensive on a large Redis region; dumps still show it as the “clear the cache” interview knob.

