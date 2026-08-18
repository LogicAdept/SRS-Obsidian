<!--
reps: 0
priority: 0
-->
#Java/Collections/Map/TreeMap #Java/Collections/Sorting #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: keys must be **orderable**. Built-ins that dumps name: `Integer`, `String`, `Double`, `Character`. Custom keys must **`implement Comparable`** or you pass a **`Comparator`** to the constructor.

Example: `Person` with `compareTo` by `id`, then `TreeMap<Person, String>`.

Harp-style: TreeMap wants **homogeneous** keys because it sorts; HashMap can mix types because it does not sort.

> [!warning] Unverified traps from the dump
> - Mixing incomparable types at `put` is the ClassCast / “homogeneous keys” story.
> - Enums work because `Enum` implements `Comparable` (separate enum card already exists).
