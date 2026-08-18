<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/HashMap #Java/Collections/Map/LinkedHashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **`HashMap` does not guarantee iteration order.** `LinkedHashMap` is “just like `HashMap`” plus a **predictable iteration order**. It is a hash table **and** a linked list: it **inherits `HashMap`**, keeps insertion-order by default, and can switch to **access-order** (`true` as the third constructor argument) so recently accessed entries move to the end — the usual LRU-cache story.

Another dump: `LinkedHashMap` is **slightly slower and more memory-intensive** than `HashMap` because of that list; the predictable order is the trade-off. The extra structure is a **doubly linked list**. Default is insertion-order. `accessOrder == true` means last-access order: `get()` / `put()` move the entry to the **end** of the list.

> [!warning] Unverified traps from the dump
> - One dump calls it a “Hashtable and Linked list” implementation — that is wording for *hash table*, not `java.util.Hashtable`.
> - Another dump says use `LinkedHashMap` when pairs are “sorted by insertion order.” Insertion-order is not key sort order (`TreeMap`).
