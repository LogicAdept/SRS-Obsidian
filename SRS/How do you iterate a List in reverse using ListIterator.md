<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #Java/Collections/List #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `ListIterator` is for **Lists**, **bidirectional**, with **index** operations. Start at the **end** and walk with `previous`:

```java
List<String> l = new ArrayList<>(List.of("a", "b", "c"));
ListIterator<String> it = l.listIterator(l.size());
while (it.hasPrevious()) {
    System.out.print(it.previous()); // "cba"
}
```
