<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/IdentityHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump body: default **IdentityHashMap expected maximum size is 21**; default **HashMap initial capacity is 16**.

The same page’s recap table **swaps** those numbers (IdentityHashMap 16, HashMap 21).

> [!warning] Unverified traps from the dump
> - 21 is **expected maximum size**, not HashMap’s capacity/load-factor pair.
> - The dump’s own table contradicts its prose.
