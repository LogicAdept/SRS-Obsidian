<!--
reps: 0
priority: 0
-->
#Java/Collections/Unmodifiable #SRS

# When should you use Collections emptyList versus a new empty list instance?

> [!abstract] Short answer
> **`Collections.emptyList()` (or `List.of()` since 9) when the empty result is data the caller only reads; `new ArrayList<>()` when the receiver will fill the list.** `emptyList()` is an immutable, **shared** singleton — no allocation per call — and it is serializable and type-safe via target typing. A fresh `ArrayList` is a distinct mutable instance with its own backing array, which is exactly what a collecting caller needs.

## One shared immutable instance versus a fresh mutable one

`Collections.emptyList()` returns an empty **immutable** list. The documentation states the practical part explicitly: implementations "need not create a separate List object for each call", so the cost is comparable to a constant field — and on the stock JDK every call returns the **same reference**. Type safety comes from the generic method: `List<String> s = Collections.emptyList();` compiles because the type parameter is inferred from the target, which is the whole reason the method (since 5) supersedes the raw `EMPTY_LIST` field ([[What is wrong with null and how do you avoid it]]). `List.of()` behaves the same way — shared instance, unmodifiable — and the two empty lists are `equals`-equal to each other, because `List` equality is content-based.

`new ArrayList<>()` is the opposite deal: a per-call allocation of a mutable list with its own array and `modCount`. The receiver can `add`, `remove`, and hand it out safely without checking what contract the caller assumed. That is the list you want when building a result incrementally or when the method's contract says "returns a list you may modify" ([[How are immutable objects used in Java APIs]]).

Equality and identity behave differently across the three: the two empty singletons are the same object per call site, a fresh `ArrayList` never is, yet **all** empty lists are equal by content — so code that only compares contents works with any of them. Never rely on identity for the singletons: the value-based factories explicitly tell callers to treat equal instances as interchangeable ([[How do you obtain a read-only or unmodifiable collection in Java]]).

> [!warning] Handing `emptyList()` to a caller that appends throws at runtime
> A method that returns `Collections.emptyList()` for the "no data" case invites callers to do `result.add(...)` — an `UnsupportedOperationException` thrown far from the code that chose the type. This is a contract bug, not a JDK quirk: the same call succeeds when the happy path returns a mutable `ArrayList`, so the failure appears only for the empty branch. Decide by **who mutates**: returning read-only data — `emptyList()`; returning a buffer the caller fills — `new ArrayList<>()`.

```d2
direction: down
q: "who may mutate the returned list?" {
  width: 320
  height: 55
}
mut: "the caller fills it" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
ro: "read-only result" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}
al: "new ArrayList<>()" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
el: "Collections.emptyList() / List.of()" {
  width: 330
  height: 55
  style.fill: "#e8f5e9"
}
uoe: "add later -> UnsupportedOperationException" {
  width: 340
  height: 55
  style.fill: "#ffebee"
}
q -> mut
q -> ro
mut -> al
ro -> el
mut -> uoe: "never return the singleton here"
```

**Fig. 1.** The choice is a mutability contract, not a style preference.

```java
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;

public class EmptyListDemo {
    public static void main(String[] args) {
        List<String> a = Collections.emptyList();
        List<String> b = Collections.emptyList();
        System.out.println(a == b);        // true  - shared immutable instance
        System.out.println(a.equals(b));   // true  - equal to any empty list
        System.out.println(a.equals(new ArrayList<String>())); // true
        try {
            a.add("x");
        } catch (UnsupportedOperationException e) {
            System.out.println("UOE");     // UOE
        }

        List<String> c = new ArrayList<>(); // distinct, mutable, safe to fill
        c.add("x");                        // works
        System.out.println(c);             // [x]

        List<String> typed = Collections.emptyList(); // target typing
        System.out.println(typed.isEmpty()); // true
    }
}
```

**Listing 1.** Identity, content equality, the mutation trap, and inference. Complete program, run-verified on JDK 21 (output matches the comments).

> [!tip] Interview answer
> **`Collections.emptyList()` is a shared immutable singleton — zero allocation, serializable, and type-inferred — so I return it when the empty result is read-only data.** `new ArrayList<>()` allocates a fresh mutable list, and that is what a caller who appends to the result needs. Mixing them up surfaces as `UnsupportedOperationException` on the first `add`, so I pick by who mutates, and `List.of()` since 9 is the same deal as `emptyList()`.
