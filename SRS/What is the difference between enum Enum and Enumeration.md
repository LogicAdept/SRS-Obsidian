<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Collections/Iteration #SRS

> [!abstract] Short answer
> **Three different names.** `enum` is the keyword that declares an enum class. `Enum` is `java.lang.Enum`, the implicit superclass of every such class. `Enumeration` is `java.util.Enumeration`, a Java 1.0 cursor (`hasMoreElements` / `nextElement`) used by `Vector` and `Hashtable`. It is not an enum type and not `java.lang.Enum`.

## Keyword, superclass, legacy cursor

An `enum Coin { PENNY, NICKEL }` declaration is an enum class ([[How would you explain Java enum types]]). Its direct superclass is `Enum<Coin>`; there is no `extends` clause ([[Can a Java enum extend a class]]). `Coin.PENNY` is an instance of `Coin` and therefore of `Enum`. The language feature and `java.lang.Enum` arrived together in Java 5 ([[In which Java version were enums introduced]]).

`java.util.Enumeration<E>` is an **interface** from 1.0. An object that implements it yields a series of elements, one at a time. The documented loop is `for (Enumeration<E> e = v.elements(); e.hasMoreElements(); )` over a `Vector`. Hashtable keys/values and `SequenceInputStream` use the same interface. `StringTokenizer` implements it. None of that is an `enum` declaration.

The Collections Framework duplicated that cursor as `Iterator` (`hasNext` / `next`, optional `remove`). New code should prefer `Iterator`. `Enumeration.asIterator()` (Java 9) adapts the leftover 1.0 objects ([[What is the difference between Enumeration and Iterator in Java]]). Fail-fast vs fail-safe is a property of a concrete iterator, not of the word “enum” ([[Is Enumeration fail-fast]]).

```d2
direction: down
kw: "enum Coin { … }" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
base: "java.lang.Enum<Coin>\nsince 1.5, implicit superclass" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
cur: "java.util.Enumeration<E>\nsince 1.0, hasMoreElements / nextElement" {
  width: 340
  height: 70
  style.fill: "#fff3e0"
}

kw -> base: "every enum type"
kw -> cur: "unrelated"
```

**Fig. 1.** Same English root; three types in the platform.

```java
import java.util.Enumeration;
import java.util.Vector;

enum Coin { PENNY, NICKEL }

class Demo {
    static Enum<Coin> asBase() {
        return Coin.PENNY; // 1.5 superclass, not java.util.Enumeration
    }

    static String cursor() {
        Vector<String> v = new Vector<>();
        v.add("x");
        Enumeration<String> e = v.elements();
        return e.nextElement();
    }
}
```

**Listing 1.** `Coin` / `Enum<Coin>` vs `Enumeration<String>` from `Vector.elements()`. They do not implement each other.

> [!warning] `Vector.elements()` is not “an enum of the vector”
> Interview shorthand that “Enumeration enumerates a collection” is the 1.0 interface. An `enum` type is a closed set of constants. Walking `Coin.values()` is an array/`for`, not `java.util.Enumeration` ([[How do you iterate over all Java enum constants]]).

> [!warning] Do not `implements Enumeration` to invent enum constants
> That interface is a cursor. A typesafe set of named instances is `enum` ([[What is the advantage of a Java enum over int and String constant patterns]]). Mixing the two is a naming collision, not a design pattern.

> [!tip] Interview answer
> **`enum` is the keyword; `java.lang.Enum` is the superclass of every enum type (Java 5); `java.util.Enumeration` is a 1.0 iterator-style interface with `hasMoreElements` / `nextElement`.** They share an English root and nothing else. Prefer `Iterator` for new cursors; prefer `enum` for a fixed set of named constants.
