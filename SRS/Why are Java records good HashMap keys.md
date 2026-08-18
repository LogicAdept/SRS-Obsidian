<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Collections/Map/HashMap #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: generated `equals()` and `hashCode()` use all components, so two `new Point(0, 0)` instances look up the same map entry without a hand-written pair.

```java
record Point(int x, int y) {}
Map<Point, String> labels = new HashMap<>();
labels.put(new Point(0, 0), "origin");
labels.get(new Point(0, 0));  // "origin"
```

Caveats from the same dumps:

- A mutable component (`List`, array) that you mutate after `put` breaks the key contract.
- Array components: generated `equals` is said to compare arrays by reference, so two `int[]{1,2,3}` headers do not match; dumps say override with `Arrays.equals` / `Arrays.hashCode`.
- `hashCode` is computed on each call (no instance-field cache).

Null components are claimed to be handled via `Objects.equals`.

> [!warning] Unverified traps from the dump
> - This does not contradict losing HashMap entries when a mutable key changes after `put`.
> - One dump says generated hashCode is a 31-multiply chain, not `Objects.hash` (which allocates an array).
