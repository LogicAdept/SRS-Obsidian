<!--
reps: 0
priority: 0
-->
#Java/Collections/Queues/PriorityQueue #SRS

# What does `PriorityQueue` require of its elements?

> [!abstract] Short answer
> **Not `null`, and mutually comparable under the queue’s ordering.** Default ordering is **natural order** (`Comparable`). A `Comparator` at construction replaces that; then elements need not implement `Comparable`, but they must be comparable **to one another by that comparator**. Insert of a bad element throws `ClassCastException` or `NullPointerException` on `offer`/`add` (an empty queue constructs fine). **Duplicates are allowed.** The head is the **least** element; ties at the head are broken arbitrarily.

## Comparable *or* a constructor `Comparator` — never `null`

`PriorityQueue` is an unbounded priority heap. Elements are ordered by natural ordering **or** by a `Comparator` supplied at construction. It does **not** permit `null`. Natural ordering also does not permit non-comparable objects (`ClassCastException`) [[What is java.util.PriorityQueue]] [[Does PriorityQueue allow null]].

`offer` / `add` document both failures: `NullPointerException` if the element is `null`; `ClassCastException` if it cannot be compared with elements already in the queue **according to the queue’s ordering**. Collection constructors throw the same if the source, or any element, is `null`, or if the source’s elements cannot be compared to one another.

“Comparable” in interview speak means **the ordering is total for the occupants**: `Comparable.compareTo` when `comparator()` is `null`, otherwise `Comparator.compare`. A `null` comparator argument still means natural order (`PriorityQueue(Comparator)` since Java 8) [[What is the difference between java.lang.Comparable and java.util.Comparator]] [[How do you build a max-heap with PriorityQueue]].

```d2
direction: down
insert: "offer / add / collection ctor" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
npe: "null element\nNullPointerException" {
  width: 240
  height: 65
  style.fill: "#fff3e0"
}
cce: "not comparable under this ordering\nClassCastException" {
  width: 320
  height: 65
  style.fill: "#fff3e0"
}
ok: "non-null, mutually comparable\nheap insert; duplicates kept" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}

insert -> npe
insert -> cce
insert -> ok
```

**Fig. 1.** The empty constructor does not type-check occupants. The first (and later) inserts do.

The type is a `Queue`, not a `Set`: equal-priority values can sit together. If several are tied for least, the head is **one** of them — unspecified which. `contains` / `remove(Object)` still use `equals`, not the comparator [[What happens when two PriorityQueue elements have equal priority]].

The queue is unbounded; internal array capacity grows as elements are added (growth policy unspecified). `peek` / `element` / `size` stay cheap; `contains` is a linear `equals` scan [[What are the time complexities of PriorityQueue operations]].

```java
import java.util.Comparator;
import java.util.PriorityQueue;

class PriorityQueueElementRules {
    static void demo() {
        new PriorityQueue<Object>(); // ok — empty, nothing compared yet
        PriorityQueue<String> natural = new PriorityQueue<>();
        natural.offer("b");
        natural.offer("a");          // String is Comparable; head is "a"
        natural.offer("a");          // duplicate kept
        // natural.offer(null);      // NullPointerException

        PriorityQueue<Object> notComparable = new PriorityQueue<>();
        // notComparable.offer(new Object()); // ClassCastException on insert

        PriorityQueue<int[]> byLength =
            new PriorityQueue<>(Comparator.comparingInt(a -> a.length));
        byLength.offer(new int[] {1, 2}); // no Comparable on int[]
    }
}
```

**Listing 1.** Natural-order queues need `Comparable` elements (here `String`). A constructor comparator is enough for types that are not `Comparable`. `null` is never an element, including with a comparator. Failure is on `offer`/`add`, not on `new PriorityQueue<>()`.

> [!warning] “Must be `Comparable`” is incomplete
> Only **natural order** requires `Comparable`. With `Comparator.reverseOrder()` or `comparingInt(...)`, the comparator is the ordering. Mixing two unrelated types in one natural-order queue still throws `ClassCastException`.

> [!warning] The empty queue does not validate elements
> `new PriorityQueue<Widget>()` succeeds even if `Widget` is not `Comparable`. The first `offer` is where `ClassCastException` shows up. Collection constructors fail earlier, while copying the source.

> [!tip] Interview answer
> **No `null`s. Elements must be mutually comparable: natural `Comparable` order, or a `Comparator` given at construction.** Otherwise `offer`/`add` throw `ClassCastException`. **Duplicates are allowed; the head is the least element.** The empty constructor does not check this.
