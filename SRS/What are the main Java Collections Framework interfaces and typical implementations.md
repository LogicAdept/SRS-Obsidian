<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS #New

> [!warning] Untrusted draft
> Text copied from an external question dump. Not checked against official documentation. Do not treat as a review answer.

**What are the main Java Collections Framework interfaces and typical implementations?**

- Top of the framework: `Collection` and `Map` (`Map` does not extend `Collection`).
- `Collection`: `List` (ordered, duplicates), `Set` (no duplicates), `Queue` (FIFO insert/remove).
- Typical `List`: `ArrayList`, `LinkedList`, `Vector` (synchronized), `Stack` (LIFO on `Vector`).
- Typical `Set`: `HashSet` (hash table / `HashMap` keys), `LinkedHashSet` (insertion order), `TreeSet` (natural order or `Comparator`).
- Typical `Queue`: `PriorityQueue`, `ArrayDeque` (`Deque`, also usable as LIFO).
- Typical `Map`: `HashMap`, `LinkedHashMap`, `TreeMap`, `Hashtable` (synchronized, no nulls), `WeakHashMap`, `ConcurrentHashMap`.
