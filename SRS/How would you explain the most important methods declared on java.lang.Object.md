<!--
reps: 0
priority: 0
-->
#Java/Language/Object #SRS

# How would you explain the most important methods declared on `java.lang.Object`?

> [!abstract] Short answer
> The methods that matter in practice are the ones **every object already has** and that you **override or must not call casually**: **`equals` and `hashCode` together**, **`toString`**, **`getClass`**, then **`wait` / `notify` / `notifyAll`**, with **`clone` and `finalize`** as known traps. Defaults are **identity**. A full roster lives on [[How would you explain key methods declared on java.lang.Object]]; this card is the interview ranking — **what you change, and what you must not misuse**.

## What the language puts on every object

`Object` is the root type, so class instances and arrays inherit its methods ([[How would you explain java.lang.Object as the root of the class hierarchy]]). The spec’s own summary is `clone`, `equals`, `finalize`, `getClass`, `hashCode`, `wait` / `notify` / `notifyAll`, and `toString`. “Most important” is not a second API: it is **which of those show up in design and interviews**.

```d2
direction: down
override: "You override\nequals + hashCode\ntoString" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
finals: "You cannot override\ngetClass, wait, notify,\nnotifyAll" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
avoid: "You usually avoid\nclone, finalize" {
  width: 240
  height: 80
  style.fill: "#ffebee"
}
```

**Fig. 1.** Importance here means: value equality, debugging, runtime type, monitors — not “call `finalize`.”

## Override for value, keep identity unless you mean it

**`equals(Object)`** on `Object` is **`this == obj`**. **`hashCode`** must agree: equal objects, equal codes; `Object` picks distinct ints when it reasonably can. If a type is a **map/set key** or a domain value, override **both** in the same class ([[How would you explain default equals and hashCode inherited from Object]], [[Why should equals and hashCode be overridden together]]). If you care only about identity, leave both alone — that is a valid choice, not a missing override.

**`toString`** defaults to `getClass().getName() + '@' + Integer.toHexString(hashCode())`. Override when logs and debugger views should show **state**, not a hex identity tag.

**`getClass`** is **`public final`**. It returns the **runtime** `Class` (the object locked by `static synchronized` methods of that class). You never override it; you use it when you need the exact class, not an `instanceof` lattice.

```java
final class Money {
    final int cents;

    Money(int cents) { this.cents = cents; }

    @Override
    public boolean equals(Object o) {
        if (!(o instanceof Money)) {
            return false;
        }
        Money m = (Money) o;
        return m.cents == cents;
    }

    @Override
    public int hashCode() {
        return Integer.hashCode(cents);
    }

    @Override
    public String toString() {
        return cents + "¢";
    }
}
```

**Listing 1.** Conceptual: the three methods you actually rewrite for a value type. `getClass()` stays the inherited `final` method.

## Important because they are easy to get wrong

**`wait` / `notify` / `notifyAll`** are **`final`**, live on **`Object`** (the monitor), not on `Thread`. The caller must **own that object’s monitor** or the call throws `IllegalMonitorStateException`. `wait` releases **that** lock and parks until notify, interrupt, timeout, or a **spurious wakeup** — loop on the condition ([[How would you explain the Object wait method and waiting on monitors]]).

**`clone`** is **`protected`**, shallow, and `Cloneable`-gated ([[How would you explain the Object clone method and its issues]]). **`finalize`** is **`protected`**, deprecated for removal, and not a destructor ([[How would you explain the finalize method in Java and why it is discouraged]]). Both are “important” as **don’t start there**, not as tools you reach for first.

> [!warning] “Most important” is not `clone` or `finalize`
> Listing every `Object` method is correct; ranking `clone` next to `equals` is how interviews go wrong. The methods you **override for correctness** are `equals` / `hashCode` / `toString`. The methods you **must not call without a monitor** are `wait` / `notify`. `getClass` is `final`. `finalize` is on the way out.

> [!warning] `equals` without `hashCode` breaks maps
> A value-based `equals` and the inherited `hashCode` put equal instances in **different** buckets. The contract is pairwise: override both or override neither.

> [!tip] Interview answer
> **The important `Object` methods are `equals` and `hashCode` (identity by default — override both for value types), `toString`, and `final` `getClass`.** Then name `wait`/`notify` as monitor methods on the object, not on `Thread`. Mention `clone` and `finalize` only as legacy traps you do not use in new code.
