<!--
reps: 0
priority: 0
-->
#Java/OOP/Constructors #Java/Immutability #SRS

# How would you explain copy constructors or defensive copying in Java?

> [!abstract] Short answer
> A **copy constructor** is an ordinary constructor `Box(Box other)` that you **write**; Java does **not** synthesize one. **Defensive copying** means you **do not store or return** a caller’s mutable object: copy **in** (constructor/setter) and copy **out** (getter) so later `array[0] = …` cannot change your instance. `Object.clone` is a **shallow** field-for-field assignment; `int[].clone()` / `Arrays.copyOf` copy the **array**, not nested objects. `List.copyOf` snapshots structure; **`unmodifiableList` is a view**, not a copy. Copy vs default/parameterized: [[How do default copy and parameterized constructors differ]]. `clone`: [[How would you explain the Object clone method and its issues]]. Immutable APIs: [[How are immutable objects used in Java APIs]].

## Write a copy; break aliases

Constructors initialize a **new** instance ([[What is constructor]]). `Box(Box other) { this.data = other.data; }` shares the array. Independence needs a **new** array (and copies of **mutable** elements if you need a deep freeze). `Object.clone` states that explicitly: after `super.clone()`, replace references to mutable internals with copies; primitives and immutable refs (`String`) usually need nothing more. Cloneable: [[Why is clone declared on Object rather than on Cloneable]]. Why immutability: [[How would you explain immutability and its benefits in Java]]. `String`: [[Why is java.lang.String immutable and final]].

**Inbound.** Constructor or setter takes `int[]` / `List` / `Date`-like mutables → store `data.clone()`, `Arrays.copyOf(data, data.length)`, `new ArrayList<>(c)`, or `List.copyOf(c)` (unmodifiable copy; no nulls).

**Outbound.** Getter must not return the private array/list. Return `data.clone()` or `List.copyOf(names)`. Returning the field lets the caller mutate your representation.

**Copy constructor vs `clone`.** `new Box(other)` is a normal `new` plus your copy logic; it can copy a **supertype** view (`Box(Box)` applied to a subclass **drops** subclass fields). `clone()` is conventional for same-class copies (`x.clone().getClass() == x.getClass()` when everyone calls `super.clone()`), still shallow unless you deepen it. Arrays are `Cloneable`; `T[] clone()` returns `T[]`.

```d2
direction: down
in: "caller passes mutable data" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
store: "store a copy\nclone / copyOf / List.copyOf" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
alias: "store the reference\ncaller still mutates you" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
in -> store
in -> alias
```

**Fig. 1.** Defensive copying breaks the alias. Assigning the parameter keeps it.

```java
import java.util.List;

class Box {
    private final int[] data;

    Box(int[] data) {
        this.data = data.clone();
    }

    Box(Box other) {
        this.data = other.data.clone();
    }

    int[] snapshot() {
        return data.clone();
    }
}

class Names {
    private final List<String> names;

    Names(List<String> names) {
        this.names = List.copyOf(names);
    }

    List<String> names() {
        return names;
    }
}
```

**Listing 1.** `Box` copies the array in, across a copy constructor, and out. `Names` snapshots a list of immutable `String`s; returning the unmodifiable list is then safe.

> [!warning] `this.data = data` is not a copy
> After `new Box(a)`, `a[0] = 9` changes `Box` if you stored `a`. The same hole exists on a getter that returns `data`. `clone()` / `copyOf` on an `Object[]` still **shares the elements**.

> [!warning] `Collections.unmodifiableList(live)` is not a defensive copy
> It is a **view**. Mutating `live` is visible. `List.copyOf(live)` / `new ArrayList<>(live)` take a snapshot of **slots**, not of mutable element objects.

> [!warning] `Box(Box other)` does not copy a subclass
> `new Box(special)` where `special` is `SpecialBox extends Box` builds a plain `Box`. `clone()` is the usual same-class copy; a copy constructor on the parent type is a **widening** copy.

> [!tip] Interview answer
> Java has no built-in copy constructor; you write Box(Box other) and copy each field, cloning mutable parts. Defensive copying is the same idea at API boundaries: copy mutable arguments before storing them and copy mutable internals before returning them. Object.clone and array clone are shallow; List.copyOf snapshots a list, unlike an unmodifiable view. Prefer immutable components so many copies become unnecessary.
