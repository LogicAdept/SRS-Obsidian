<!--
reps: 0
priority: 0
-->
#Java/Collections/List/Vector #Java/Collections/Queues/ArrayDeque #SRS

> [!abstract] Short answer
> **Because `Stack` is a `Vector` with five LIFO methods, not a stack type.** It is a synchronized `List`: you can index, insert in the middle, and pay a lock on ordinary single-threaded use. Use a `Deque` instead — almost always `ArrayDeque`: `Deque<E> stack = new ArrayDeque<>()`. The class is **not** `@Deprecated`; the API still says prefer `Deque`.

## Why `Stack` is the wrong type

`Stack` extends `Vector` and tacks on `push`, `pop`, `peek`, `empty`, and `search` at the **last** index ([[How would you explain Stack how why]]). Every `List` / `RandomAccess` operation remains. LIFO is convention, not the type. That is neither a complete nor a consistent stack: `get(i)` and `add(index, e)` compile.

`Vector` is synchronized, unlike the later collections. A local stack does not need that. `Stack.push` is not even a `synchronized` method; it still mutates through synchronized `addElement`. You pay the lock tax and still inherit the leaky `List` surface. Keep `Stack` for “it is thread-safe” is the wrong fix ([[Is the Java Stack class meant for long-term storage]]).

`Deque` is documented as the **more complete and consistent** LIFO set and **should be used in preference** to this **legacy** class. Completeness here is the two-family end API (`addFirst` / `offerFirst`, `removeFirst` / `pollFirst`, `getFirst` / `peekFirst`) plus explicit stack names `push` / `pop`. Consistency is that stack operations are head operations on a type that is **not** a `List` ([[How do you use a Deque as a stack]], [[Which Java collection implements FILO ordering]]).

```d2
direction: right
st: "Stack extends Vector\nList + locks + five LIFO methods" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
dq: "Deque + ArrayDeque\nLIFO at the head, no List" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
st -> dq: "prefer"
```

**Fig. 1.** Replacement is a different type, not a subclass of `Stack`. `ArrayDeque` does not extend `Vector`.

## What to write instead

The example on `Stack`’s own page is `Deque<Integer> stack = new ArrayDeque<>()`. `ArrayDeque` is a circular array `Deque`: no nulls, not thread-safe, amortized O(1) at both ends, and **likely** faster than `Stack` as a stack. `LinkedList` is also a `Deque`; use it when you need `List` and `Deque` together, not as the default stack ([[What is the difference between ArrayDeque and LinkedList as a Deque]]).

If you actually needed concurrent LIFO, `ArrayDeque` is the wrong swap (it documents no concurrent access). `Deque` implementors include concurrent deques; that is a different choice than keeping `Stack` for `Vector`’s locks.

Empty `Stack.peek` / `pop` throw `EmptyStackException`. `Deque.pop` throws `NoSuchElementException`; `Deque.peek` returns `null`. Migrating call sites is not a rename of the class.

```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Stack;

class PreferDeque {
    static void demo() {
        Stack<Integer> legacy = new Stack<>();
        legacy.push(1);
        legacy.get(0);                 // List — why Stack is discouraged

        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(1);
        stack.push(2);
        Integer top = stack.peek();    // 2
        Integer popped = stack.pop();  // 2
        // stack.get(0);               // does not compile — not a List
    }
}
```

**Listing 1.** Declare `Deque`, construct `ArrayDeque`. Indexed `get` on `Stack` is the design leak the replacement removes.

> [!warning] Not `@Deprecated`
> Interview “discouraged” means the preference sentence on `Stack` / `Deque`, not an annotation. The class still compiles in Java 21.

> [!warning] Do not keep `Stack` for synchronization
> `Vector` locks are the old collection model. They do not make a good concurrent stack, and they make a worse single-threaded one. Need threads: pick a concurrent `Deque`. Need a stack: `ArrayDeque`.

> [!tip] Interview answer
> **`Stack` is discouraged because it is a synchronized `Vector`/`List` with LIFO helpers, so it is not a real stack type.** Use `Deque`, usually `ArrayDeque` — the documented replacement, likely faster as a stack, no leftover `get(i)`. It is legacy-preferred, not `@Deprecated`.
