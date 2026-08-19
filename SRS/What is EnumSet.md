<!--
reps: 0
priority: 0
-->
#Java/Collections/Set/EnumSet #Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: specialized `Set` for **enum** types. Extends `AbstractSet`, implements `Set`.

Features in the dump:

- only enum values, **all the same enum**
- **no null** — `NullPointerException` if you add null
- **not thread-safe** — synchronize externally if needed
- iteration order = **enum declaration order**
- iterator described as **fail-safe** (works on a **copy**), so no `ConcurrentModificationException` if the set is modified during iteration

Dump: using an enum with `EnumSet` is **far better** than `HashSet` or `LinkedHashSet`. Created via factories, not `new`:

```java
enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

EnumSet<Day> work = EnumSet.range(Day.MON, Day.FRI);
EnumSet<Day> weekend = EnumSet.complementOf(work); // [SAT, SUN]
EnumSet<Day> none = EnumSet.noneOf(Day.class);
EnumSet<Day> all  = EnumSet.allOf(Day.class);
```

> [!warning] Unverified traps from the dump
> - “Fail-safe copy iterator” is dump wording; do not treat it as javadoc.
> - Empty vault stub `Why does Java provide EnumSet…` is the “why bit vector” cue; this card is the type’s feature list.
