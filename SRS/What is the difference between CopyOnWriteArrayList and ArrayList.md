<!--
reps: 0
priority: 0
-->
#Java/Collections/List/ArrayList #Java/Collections/Concurrency #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: `CopyOnWriteArrayList` arrived in **JDK 1.5**, implements `List`, and is an “enhanced `ArrayList`” where **add / set / remove** are done by making a **fresh copy** of the backing array.

Another dump: it implements `List` and `RandomAccess`, so it offers the `ArrayList` surface. It is a **thread-safe** `ArrayList`. Each iterating thread sees a **snapshot** of the backing array taken when the iterator is created, so it does **not** throw `ConcurrentModificationException`. **Iterator** `remove` / `set` / `add` throw `UnsupportedOperationException`. It is a concurrent **replacement for a synchronized List** when **iterations outnumber mutations**. Allows **duplicates**. **Slower than `ArrayList`** because of copying.

Prefer `CopyOnWriteArrayList` over `ArrayList` (dump) when: concurrent use; iterations ≫ writes; iterators must see the snapshot from creation time; you do not want to synchronize access yourself.

Same dump’s `ArrayList` contrast: after `iterator()`, a structural `add` **immediately** throws `ConcurrentModificationException`; `Iterator.remove` on `ArrayList` is allowed.

> [!warning] Unverified traps from the dump
> - One dump says a **new array copy is created every time an iterator is created**. Other dumps say the copy happens on **write**.
> - A sample in one dump starts the mutator with `t.run()` rather than `t.start()`.
> - Iterator mutation (`remove`/`set`/`add`) is **unsupported** on `CopyOnWriteArrayList`, unlike `ArrayList`.
