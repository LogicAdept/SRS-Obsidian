<!--
reps: 0
priority: 0
-->
#Java/Collections/Unmodifiable #SRS

# How do you obtain a read-only or unmodifiable collection in Java?

> [!abstract] Short answer
> Two honest routes. **A view:** `Collections.unmodifiableList(list)` (also `unmodifiableSet`, `unmodifiableMap`) wraps the original — reads go **through** to the backing collection, every mutator throws `UnsupportedOperationException`. **A snapshot:** `List.of(...)`, `Set.of(...)`, `Map.of(...)` (since 9) or `List.copyOf(coll)` (since 10) build an independent unmodifiable collection. A view is not a copy — pick a view to delegate, a snapshot to freeze.

## View: read-through, write-rejected

`Collections.unmodifiableList` returns an **unmodifiable view**: query operations "read through" to the specified list, and attempts to modify the returned list — directly or via its iterator — throw `UnsupportedOperationException`. The view is **live**: after the backing list changes, the view's `size`, iteration and `get` reflect it, so a caller that holds only the view still observes every later edit of the backing list. The contract keeps incidental properties aligned with the argument: the view is serializable if the backing list is, and implements `RandomAccess` if the backing list does. The family covers the other collections symmetrically (`unmodifiableSet`, `unmodifiableMap`, `unmodifiableCollection`, …).

## Snapshot: factory-made unmodifiable collections

`List.of`, `Set.of`, `Map.of` and `List.copyOf` create collections that are unmodifiable **by construction**: any mutator always throws `UnsupportedOperationException`, and their `subList` views inherit that. Documented characteristics worth naming in an interview: **null elements are rejected** with `NullPointerException` at creation; iteration order follows the argument order; they are serializable if all elements are; and they are **value-based** — callers should treat equal instances as interchangeable and not synchronize on their identity, because factories are free to reuse instances. `List.copyOf(coll)` copies the elements as of the call, so later edits of the argument never leak in; its implementation note adds that copying an already-unmodifiable list generally returns it without re-copying ([[How are immutable objects used in Java APIs]]).

> [!warning] A view is not a snapshot
> `Collections.unmodifiableList(backing)` does **not** detach you from `backing`: anyone who kept the original reference can add elements, and every holder of the "read-only" list sees them appear. If the intent is independence — a frozen return value or a defensive copy — use `List.copyOf(backing)`; if the intent is delegation, the view is correct and the leak is the caller's design ([[How would you explain immutable classes in Java]]).

The second mix-up is mutability vocabulary: **unmodifiable** forbids changes *through this reference* while **immutable** means the object cannot change at all. `List.of("a")` is immutable; `Collections.unmodifiableList(mutableList)` is still a mutable list wearing a read-only interface — its elements and structure keep changing behind the view ([[Why are immutable objects valuable in concurrent code]]).

```d2
direction: right
backing: "backing list\n(mutable, shared)" {
  width: 230
  height: 70
  style.fill: "#e3f2fd"
}
view: "Collections.unmodifiableList\nlive view, mutators -> UOE" {
  width: 300
  height: 70
  style.fill: "#fff8e1"
}
snap: "List.copyOf(backing)\nindependent snapshot" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
backing -> view: "reads go through\nsize follows"
backing -> snap: "copied once\nlater edits ignored"
```

**Fig. 1.** The view mirrors the backing list forever; the snapshot severs the connection at copy time.

```java
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;

public class UnmodifiableDemo {
    public static void main(String[] args) {
        List<String> backing = new ArrayList<>(List.of("a", "b"));
        List<String> view = Collections.unmodifiableList(backing);

        backing.set(0, "x");
        System.out.println(view.get(0));       // x    - read-through
        backing.add("c");
        System.out.println(view.size());       // 3    - the view is live
        try {
            view.add("d");
        } catch (UnsupportedOperationException e) {
            System.out.println("UOE");         // UOE
        }

        List<String> snap = List.copyOf(backing); // [x, b, c]
        backing.add("c2");
        System.out.println(snap.size());       // 3    - snapshot unaffected

        try {
            List.of("a", null);                // NPE at creation
        } catch (NullPointerException e) {
            System.out.println("NPE");         // NPE
        }
    }
}
```

**Listing 1.** View versus snapshot on JDK 21: read-through and liveness for the view, independence for `copyOf`, `NPE` for null elements in factories. Complete program, run-verified (output matches the comments).

> [!tip] Interview answer
> **To hand out read-only data I pick between a view and a snapshot.** `Collections.unmodifiableList(list)` is a live view — reads go through, writes throw `UnsupportedOperationException`, and edits of the backing list stay visible. `List.of` or `List.copyOf` build an immutable, independent collection that rejects nulls and never changes. View to delegate, snapshot to freeze — `unmodifiableList` is not a copy.
