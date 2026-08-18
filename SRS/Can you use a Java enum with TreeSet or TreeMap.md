<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Collections/Set #Java/Collections/Map/TreeMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. `java.lang.Enum` implements `Comparable`, which sorted collections require. Natural order is declaration order.

```java
enum Priority { LOW, MEDIUM, HIGH }
TreeSet<Priority> prioritySet = new TreeSet<>();
prioritySet.add(Priority.HIGH);
prioritySet.add(Priority.LOW);
// iterates LOW, MEDIUM, HIGH
```

You cannot compare constants of two different enum types.

> [!warning] Unverified traps from the dump
> - This is not the same question as why `EnumSet` exists versus `HashSet`/`TreeSet`.
