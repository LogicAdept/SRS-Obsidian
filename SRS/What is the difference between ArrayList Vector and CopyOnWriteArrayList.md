<!--
reps: 0
priority: 0
-->
#Java/Collections/Concurrency #Java/Collections/List/ArrayList #Java/Collections/List/Vector #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **`ArrayList` is fast and unsynchronized; `Vector` is synchronized; `CopyOnWriteArrayList` is thread-safe and great for read-heavy workloads.**

```java
CopyOnWriteArrayList<String> safeList = new CopyOnWriteArrayList<>();
safeList.add("a");
safeList.addIfAbsent("a"); // de-dup helper
```

Related dump: choose `ArrayList` for random access / append-heavy, `LinkedList` for frequent middle insert/remove, `CopyOnWriteArrayList` for **many readers, few writers**.

> [!warning] Unverified traps from the dump
> - `Vector` is the whole-list lock story; dumps still tell you not to pick it for new code.
> - `addIfAbsent` is a `CopyOnWriteArrayList` extra, not an `ArrayList` method.
