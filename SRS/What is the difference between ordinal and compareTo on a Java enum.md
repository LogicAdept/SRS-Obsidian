<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

> [!abstract] Short answer
> **`ordinal()` is the constant’s zero-based place in the declaration. `compareTo` asks how two constants of **that same enum type** sit relative to each other.** Both follow declaration order and both are `final` on `java.lang.Enum`. `compareTo` returns a negative int, `0`, or a positive int — not the ordinal itself.

## Index vs comparison result

`ordinal()` returns the `int` stored on the constant (`0` for the first name, `1` for the next, …). It exists for structures such as `EnumMap` / `EnumSet`, not as a business key ([[What does ordinal do on a Java enum]]).

`compareTo` is `Enum`’s `Comparable` implementation: `this.ordinal - other.ordinal`, after checking that both constants share a declaring enum class. `0` means the same constant (same ordinal). Negative means the receiver was declared earlier. Positive means it was declared later. That is the natural order `TreeSet` / `TreeMap` use ([[Can you use a Java enum with TreeSet or TreeMap]]).

The method is `final`. You cannot override it to sort by a field ([[Can you override compareTo on a Java enum]]). A `Comparator` on `TreeSet`/`TreeMap` is a separate ordering; it does not change `compareTo` or `ordinal()`.

Because `compareTo` is `compareTo(E o)` on `Enum<E extends Enum<E>>`, two different enum types do not compile. `==` between those types does not compile either. `equals(Object)` compiles and returns `false` — identity, not ordinals ([[What is the difference between comparing enums with == and equals]]).

```d2
direction: down
src: "enum Level { LOW, MEDIUM, HIGH }" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
ord: "ordinal(): LOW→0  MEDIUM→1  HIGH→2" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}
cmp: "compareTo: MEDIUM vs HIGH → negative" {
  width: 320
  height: 50
  style.fill: "#fff3e0"
}

src -> ord -> cmp: "same order, different return"
```

**Fig. 1.** One declaration list. `ordinal()` names a slot. `compareTo` names a relation.

```java
enum Level { LOW, MEDIUM, HIGH }

class Demo {
    static int demo() {
        int slot = Level.MEDIUM.ordinal();           // 1
        int rel  = Level.MEDIUM.compareTo(Level.HIGH); // negative (1 - 2)
        return slot + rel;
        // Level.MEDIUM.compareTo(someOtherEnum) does not compile
    }
}
```

**Listing 1.** `ordinal()` is `1`. `compareTo` is not `1`; it is the signed gap to the other constant.

> [!warning] `compareTo` returning `0` does not mean “first constant”
> Every constant compared with **itself** yields `0`. Only `ordinal() == 0` means first in the source file. Do not persist either number as a column: insert a constant and both shift ([[Can you add constants to a Java enum at runtime]]).

> [!warning] You cannot customise enum order by overriding `compareTo`
> Interview follow-up: keep declaration order, or pass a `Comparator`. `compareTo` stays the source order forever.

> [!tip] Interview answer
> **`ordinal()` is the zero-based declaration index; `compareTo` is that index compared with another constant of the same enum (`this.ordinal - other.ordinal`).** Same natural order, both `final`. Cross-type `compareTo` is a compile error; use a `Comparator` if you need a different sort.
