<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #Java/Language/Optional #Java/Collections #SRS

# What is `NoSuchElementException`?

> [!abstract] Short answer
> **An unchecked `RuntimeException` from accessors when the requested element is not there.** Classic cases: `Iterator.next()` with no remaining element, `Queue.remove()` / `element()` on an empty queue, and `Optional.get()` (or no-arg `orElseThrow()`) on an empty `Optional`.

## Missing element, not a `null` dereference

`NoSuchElementException` is in `java.util` and extends `RuntimeException`. You do not declare it in `throws` ([[Is RuntimeException a subclass of Exception]], [[Must you declare RuntimeException in a throws clause]], [[What are common kinds of unchecked exceptions in Java]]).

`Iterator.next()` throws it when `hasNext()` would be false. `Queue.remove()` and `element()` throw it when the queue is empty. `poll()` and `peek()` return `null` instead of throwing.

`Optional.get()` on empty is this type, **not** `NullPointerException`. Prefer `orElseThrow()` or an explicit empty check ([[What does orElseThrow do on Optional]], [[How do you prevent a NullPointerException]]).

```d2
direction: down
it: "Iterator.next()  (exhausted)" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
opt: "Optional.empty().get()" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
nsee: "NoSuchElementException" {
  width: 280
  height: 50
  style.fill: "#ffebee"
}
rm: "Queue.remove() / element()  (empty)" {
  width: 320
  height: 50
  style.fill: "#ffebee"
}
poll: "Queue.poll() / peek()  (empty)" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
nil: "null (no throw)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
it -> nsee
opt -> nsee
rm -> nsee
poll -> nil
```

**Fig. 1.** Missing-element throw versus empty-queue `null`.

```java
import java.util.ArrayDeque;
import java.util.Collections;
import java.util.Iterator;
import java.util.Optional;
import java.util.Queue;

class Demo {
    static String nextEmpty() {
        Iterator<String> it = Collections.emptyIterator();
        return it.next();
    }

    static String getEmpty() {
        return Optional.<String>empty().get();
    }

    static String removeEmpty() {
        Queue<String> q = new ArrayDeque<>();
        return q.remove();
    }

    static String pollEmpty() {
        Queue<String> q = new ArrayDeque<>();
        return q.poll();
    }
}
```

**Listing 1.** `nextEmpty`, `getEmpty`, and `removeEmpty` throw `NoSuchElementException` at run time. `pollEmpty` returns `null`. You may catch it like any unchecked exception ([[Can you catch an unchecked exception in Java]]). None of these methods needs `throws`.

> [!warning] Empty `Optional.get()` is not `NullPointerException`
> `Optional` is a present/absent box. Empty means “no value,” so `get()` throws `NoSuchElementException`. `null` inside `Optional` is a different bug (`Optional.of(null)`).

> [!warning] `poll` / `peek` return `null`; `remove` / `element` throw
> Empty-queue pairs are the usual collections quiz. Mixing them with `Iterator.next()` is fine; calling `next()` without `hasNext()` is the iterator form of the same idea.

> [!tip] Interview answer
> **`NoSuchElementException` is an unchecked `RuntimeException` when an accessor has nothing to return.** `Iterator.next()` with no more elements, empty-queue `remove()`/`element()`, and empty `Optional.get()` all throw it. Empty `Optional.get()` is not an NPE, and `poll()`/`peek()` return `null` instead of throwing.
