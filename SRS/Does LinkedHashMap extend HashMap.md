<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/LinkedHashMap #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **yes.** `LinkedHashMap` **inherits `HashMap`** and implements `Map`. A compilation page: it **extends `HashMap`** and adds a doubly-linked list through the entries.

> [!warning] Unverified traps from the dump
> - Extending `HashMap` is not “it *is* a `LinkedList`.” The list is extra links on the entries.
> - One dump still says “Hashtable and linked list implementation of Map” in the same breath as “inherits HashMap.”
