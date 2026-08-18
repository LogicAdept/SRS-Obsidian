<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps split this.

Insertion-order dump: **no.** Adding an element whose key is **already present** does **not** change iteration order.

Access-order dump: on `put`, if the key **already exists**, the value is replaced and `recordAccess` runs: keep the list position **or** move the node to the **tail**, depending on `accessOrder`. If the key is **new**, the new entry is linked at the **end** of the doubly-linked list (insertion-order). Default `accessOrder` is **false**.

> [!warning] Unverified traps from the dump
> - “Re-`put` never moves the key” is the insertion-order claim; access-order dumps say `put` / `get` *do* move the node.
> - LRU dumps that say “`LinkedHashMap` cannot fully implement LRU because re-`put` does not change order” are using the insertion-order rule on an access-order question.
