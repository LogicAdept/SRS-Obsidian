<!--
reps: 0
priority: 0
-->
#Java/Collections/List #SRS

# How do you get all List elements except the first and last three with one call?

> [!abstract] Short answer
> **`list.subList(3, list.size() - 3)`.** `subList(from, to)` returns a **view** of the range `from` **inclusive** to `to` **exclusive**, backed by the original list, so the call itself copies nothing and costs O(1). For a 10-element list that is exactly `[3, 4, 5, 6]`. If the edges may be shorter than three, clamp the indices — `Math.max(3, 0)` and `Math.min(list.size() - 3, list.size())` — because an out-of-range endpoint throws.

## A view, not a copy

`List.subList(int fromIndex, int toIndex)` is specified as a **view of the portion** between `fromIndex` inclusive and `toIndex` exclusive. If the endpoints are equal the view is empty; nothing is copied, and the result supports every optional operation the backing list supports. Non-structural changes — `set` on an existing slot — flow **both ways**: writing through the view updates the backing list, and a `set` on the backing list is visible through the view. Structural writes through the view also land in the backing list: `view.add(x)` inserts into the backing list at the view's offset, and the documented idiom `list.subList(from, to).clear()` removes the whole range in one statement ([[What is an efficient way to remove a contiguous block from the middle of an ArrayList]]). A `subList` of a `subList` works too — the inner view routes back to the same root list.

Endpoint rules: `fromIndex == toIndex` is an empty view; `fromIndex < 0`, `toIndex > size` are illegal endpoint values for which the contract declares `IndexOutOfBoundsException`. Note the exclusive upper bound — `subList(3, 7)` never contains index `7`, which is why `list.size() - 3` (not `size() - 4`) is the correct second argument ([[What is the List interface in Java]]). On the stock JDK, `fromIndex > toIndex` surfaces as `IllegalArgumentException` from the internal range check, while still being an illegal-endpoint case.

> [!warning] A kept view dies when the backing list is structurally modified elsewhere
> The contract says the view's semantics become **undefined** if the backing list is structurally modified "in any way other than via the returned list". In practice with `ArrayList`, holding a `subList` across an `add` or `remove` done through another reference makes the next view access throw `ConcurrentModificationException` ([[How would you explain write collection throw ConcurrentModificationException]]). Extract data first — `List.copyOf(list.subList(3, list.size() - 3))` — or re-derive the view after the mutation.

A second trap follows from the same view idea: the returned object is **not** an instance of the original class. An `ArrayList` view's class is `java.util.ArrayList$SubList`, so casting the result back to `ArrayList` or serializing it as one fails; treat it as a plain `List` ([[How do you search and remove elements in a List]]).

```d2
direction: right
backing: "backing list [0..9]" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
view: "subList(3, 7) = [3, 4, 5, 6]" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
mirror: "set flows both ways" {
  width: 240
  height: 50
}
dead: "backing add/remove via another path" {
  width: 300
  height: 60
  style.fill: "#ffebee"
}
backing -> view: "backed by"
view -> mirror: "add, set, clear write through"
dead -> view: "view invalidated\n(CME on ArrayList)"
```

**Fig. 1.** The view is a window over the same storage: writes flow through, and a structural change made behind the window's back kills it.

```java
import java.util.List;
import java.util.ArrayList;

public class SubListDemo {
    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(List.of(0, 1, 2, 3, 4, 5, 6, 7, 8, 9));

        List<Integer> middle = list.subList(3, list.size() - 3);
        System.out.println(middle);            // [3, 4, 5, 6]
        middle.set(0, 99);
        System.out.println(list.get(3));       // 99
        middle.clear();
        System.out.println(list.size());       // 6

        List<Integer> stale = list.subList(1, 4);
        list.add(42);
        try {
            stale.get(0);
        } catch (java.util.ConcurrentModificationException e) {
            System.out.println("stale view");  // stale view
        }
    }
}
```

**Listing 1.** One call takes the middle, writes flow both directions, `clear()` trims the range, and a stale view throws on first use. Complete program, run-verified on JDK 21 (output matches the comments).

> [!tip] Interview answer
> **`list.subList(3, list.size() - 3)`** — `subList` is a live view, `from` inclusive, `to` exclusive, so those two indices cut off the first and last three elements without copying anything. `subList(from, to).clear()` is the documented way to drop a range. Keep the view only while the backing list is not structurally modified elsewhere — otherwise it throws `ConcurrentModificationException` on `ArrayList`.
