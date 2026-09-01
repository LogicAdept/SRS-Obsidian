<!--
reps: 0
priority: 0
-->
#Java/Collections/List/LinkedList #Java/Collections/Queues/ArrayDeque #SRS

> [!abstract] Short answer
> **Both implement `Deque`; the split is the backing store and extra contracts.** `ArrayDeque` is a circular `Object[]`: no nulls, not a `List`, amortized O(1) at both ends, and **likely faster as a queue**. `LinkedList` is a doubly-linked `List` **and** `Deque`: nulls allowed, indexed access by walking, content `equals`, and a `ListIterator` can unlink the current node without shifting an array. For a plain queue or stack, take `ArrayDeque`.

## Same `Deque` methods, different machines

End insert/remove/examine are cheap on both. `ArrayDeque` keeps elements in a resizable circular array (`elements`, `head`, `tail`). `LinkedList` allocates a `Node` per element (`item`, `next`, `prev`) and holds `first` / `last`. That is the “node overhead”: three references plus a header per element, against packed array slots (with spare null cells, including the reserved tail slot).

The array layout is why the API calls `ArrayDeque` **likely** faster than `LinkedList` as a queue (and likely faster than `Stack` as a stack). Traversal is index walks over contiguous slices, which VMs optimize as simple array loops. `LinkedList` walks `next` / `prev` pointers. “Always faster” is not a guarantee; the documented default for queue/stack work is still `ArrayDeque` ([[How do you use a Deque as a stack]]).

```d2
direction: right
ad: "ArrayDeque\ncircular Object[]\nDeque only, no null" {
  width: 260
  height: 90
  style.fill: "#e8f5e9"
}
ll: "LinkedList\nNode item / next / prev\nList + Deque, nulls allowed" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Same `addFirst` / `addLast` surface. Pick the array unless you need the `List` half of `LinkedList` ([[Why does LinkedList implement both List and Deque]]).

`ArrayDeque` does **not** implement `List`: no `get(int)`, no `listIterator`, no indexed `add`. Interior `remove(Object)`, `removeFirstOccurrence`, `contains`, and `iterator.remove()` copy a slice of the ring — **linear** time. `LinkedList` index operations “perform as could be expected for a doubly-linked list”: they **traverse** from the nearer end, then pointer-swing. There is no public `Node` type. The O(1) unlink is `unlink` on a node the `ListIterator` already holds (`iterator.remove()` / `ListIterator.remove()`). You do not pass a node reference in from client code.

`LinkedList` permits `null`. `ArrayDeque` rejects it (`NullPointerException`). `Deque` already uses `null` from `poll` / `peek` to mean empty, so a stored null on `LinkedList` makes those returns ambiguous ([[Why do most Queue implementations forbid null]]).

`equals` / `hashCode` follow the type, not the `Deque` variable: `ArrayDeque` keeps identity equality; `LinkedList` is a `List`, so two lists with the same sequence compare equal ([[Do Queue and Deque implementations override equals]]). Neither class is synchronized.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.LinkedList;
import java.util.List;

class ArrayDequeVsLinkedList {
    static void contrast() {
        Deque<String> ring = new ArrayDeque<>();
        Deque<String> nodes = new LinkedList<>();
        ring.addLast("x");
        nodes.addLast("x");
        nodes.addLast(null);          // LinkedList allows it
        // ring.addLast(null);        // NullPointerException

        String first = ((LinkedList<String>) nodes).get(0); // "x" — walk from an end
        // no get(int) on ArrayDeque

        boolean ringsEqual = ring.equals(new ArrayDeque<>(List.of("x")));
        // false — identity equals

        LinkedList<String> copy = new LinkedList<>();
        copy.addLast("x");
        copy.addLast(null);
        boolean listsEqual = nodes.equals(copy); // true — List equals
    }
}
```

**Listing 1.** Both variables are `Deque`. Null, indexed `get`, and `equals` still follow the concrete class.

Grow on `ArrayDeque` copies the array (double when small, else about +50%), so end inserts are **amortized** constant, not a hard bound on every call. `LinkedList` `addFirst` / `addLast` allocate one node and retarget `first` / `last` — true pointer O(1), with the extra object.

> [!warning] You never hold a `LinkedList.Node`
> “Constant-time remove given a node” is an internal `unlink`. The public hook is a `ListIterator` already sitting on that element. `remove(Object)` and `remove(index)` still search or walk. `ArrayDeque.iterator().remove()` is linear. Do not choose `LinkedList` as a deque for a node handle you cannot obtain.

> [!warning] A `Deque` reference does not hide `List` equals or nulls
> `Deque<String> d = new LinkedList<>()` still allows `null` and still uses content `equals`. Code that assumes every `Deque` is an `ArrayDeque` (no nulls, identity `equals`, no `get(int)`) breaks on `LinkedList`.

> [!tip] Interview answer
> **`ArrayDeque` is a circular array `Deque`; `LinkedList` is a doubly-linked `List` that also implements `Deque`.** Use `ArrayDeque` for a queue or stack: no nulls, amortized O(1) at both ends, likely faster. Reach for `LinkedList` when you also need `List` — indexed access, `ListIterator` unlink, or content `equals` — not because you have a node pointer.
