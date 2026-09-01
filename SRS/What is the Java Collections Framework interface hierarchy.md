<!--
reps: 0
priority: 0
-->
#Java/Collections #SRS #New

> [!warning] Untrusted draft
> Text copied from an external question dump. Not checked against official documentation. Do not treat as a review answer.

**Place these types in a hierarchy:** `List`, `Set`, `Map`, `SortedSet`, `SortedMap`, `Collection`, `Iterable`, `Iterator`, `NavigableSet`, `NavigableMap`.

- `Iterable`
  - `Collection`
    - `List`
    - `Set`
      - `SortedSet`
        - `NavigableSet`
- `Map`
  - `SortedMap`
    - `NavigableMap`
- `Iterator` is a separate type (not a subtype of `Iterable`).
