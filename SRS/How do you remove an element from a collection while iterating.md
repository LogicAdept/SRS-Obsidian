<!--
reps: 0
priority: 0
-->
#Java/Collections/Iteration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: **yes.** `Iterator.remove()` deletes the **last element returned by `next()`**.

```java
List list = new ArrayList();
list.add("One");
list.add("Two");
list.add("Three");

Iterator iterator = list.iterator();
while (iterator.hasNext()) {
    String str = iterator.next();
    if (str.equals("Two")) {
        iterator.remove();
    }
}
```

Related dump: if `remove()` is called **without** a preceding `next()`, the result is `IllegalStateException`.

> [!warning] Unverified traps from the dump
> - Calling `list.remove(...)` inside the loop is not this API; dumps use that to trigger `ConcurrentModificationException`.
> - `CopyOnWriteArrayList` iterators in other dumps **reject** `Iterator.remove()` with `UnsupportedOperationException`.
