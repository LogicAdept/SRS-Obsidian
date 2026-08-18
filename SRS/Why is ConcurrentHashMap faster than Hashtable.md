<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/Hashtable #Java/Collections/Map/ConcurrentHashMap #Java/Versions/5 #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `ConcurrentHashMap` uses **multiple buckets** to store data. That **avoids read locks** and improves performance versus `Hashtable`. Both are thread-safe.

`get()` on `ConcurrentHashMap` has **no locks**, while **all `Hashtable` operations are simply synchronized**. `Hashtable` is from old Java; `ConcurrentHashMap` was added in **Java 1.5**.

Another dump: `Hashtable` is a thread-safe hash map, but unlike `ConcurrentHashMap` **all its methods are simply synchronized**, so **every operation blocks**, even retrieval of independent values.

> [!warning] Unverified traps from the dump
> - “Multiple buckets” here is dump shorthand for concurrent access, not “Hashtable has only one bucket.”
> - HashMap-vs-Hashtable tables still call `Hashtable` thread-safe; that is not the same as “use it instead of `ConcurrentHashMap`.”
