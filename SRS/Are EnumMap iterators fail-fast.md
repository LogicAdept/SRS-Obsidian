<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/EnumMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

One dump’s “important points” list: `EnumMap` iterators are **fail-fast**, “much like `ConcurrentHashMap`”, **do not throw** `ConcurrentModificationException`, and **may not show** modifications that happen during iteration.

> [!warning] Unverified traps from the dump
> - That wording mixes the usual fail-fast (`CME`) story with the weakly-consistent / no-`CME` story. Treat it as an unverified dump, not a review answer.
> - Other collection dumps call `HashMap` iterators fail-fast *because* they throw `CME`.
