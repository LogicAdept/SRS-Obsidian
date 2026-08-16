<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/OOP #SRS

# How are `hashCode` and `equals` implemented in `java.lang.Object`?

> [!abstract] Short answer
> `Object.equals` is **reference equality**: for non-null `x` and `y` it is `true` if and only if `x == y`. Each object is its own equivalence class. `Object.hashCode` returns an `int` that, as far as is reasonably practical, is **distinct for distinct objects**. `System.identityHashCode(x)` returns that same default hash even if `x`’s class overrode `hashCode`; for `null` it returns `0`.

## `equals`: the most discriminating relation

The implementation requirement on `Object.equals` is identity. Distinct instances are never equal under this method, even when every field matches.

```java
x.equals(y)  // Object: true iff x == y  (x non-null)
x.equals(null)  // false
```

**Listing 1.** Conceptual `Object.equals`. This satisfies the five-clause contract: it is reflexive, symmetric, transitive, consistent, and false for `null`. [[How would you explain the Object equals method contract]] is that contract in general.

## `hashCode`: distinct when practical

The general `hashCode` contract still applies (stable in one run, equal objects equal hashes, collisions allowed). On class `Object` the extra implementation requirement is: as far as reasonably practical, distinct objects get distinct integers. That matches identity `equals`: each instance is unequal to the others, so distinct hashes are the quality goal, not a language guarantee of uniqueness.

The JVM is **not** required to publish the formula. Do not recite “it’s the memory address”; the spec does not say that. `System.identityHashCode` is specified only as “the hash the default `hashCode()` would return,” plus `0` for `null`.

```java
Object a = new Object();
Object b = new Object();
a.equals(b);                 // false
a.hashCode() == b.hashCode(); // usually false; not a uniqueness theorem
System.identityHashCode(a);  // default hash, even if a later subclass overrides
```

**Listing 2.** Conceptual default pair. Collisions of identity hashes remain legal; “reasonably practical” is not “always unique.” [[What is a hash collision]] still applies.

`toString` on `Object` uses the class name, `@`, and the unsigned hex of **that object’s** `hashCode()`. After you override `hashCode`, default `toString` shows the new hash unless you override `toString` too.

> [!warning] `identityHashCode` is not `hashCode` after an override
> Once a class overrides `hashCode`, `x.hashCode()` and `System.identityHashCode(x)` can disagree. Identity-based maps (`IdentityHashMap`) use identity hashes and `==`, not your value `equals`/`hashCode`. [[What is the difference between HashMap and IdentityHashMap]] is that split.

These two `Object` methods already obey “equal objects, equal hashes”: the only equal pair is the same reference, which obviously shares one hash. [[Where do default equals and hashCode implementations come from in Java]] is why every class starts here.

> [!tip] Interview answer
> **`Object.equals` is `==`. `Object.hashCode` aims at a distinct `int` per instance, as far as practical, and is what `System.identityHashCode` still reports after you override. The algorithm is not specified as an address. Together they are a consistent identity pair; value classes replace both.**

> [!warning] Черновик без доверия
> Текст скопирован из внешнего дампа вопросов. Не сверен с официальной документацией. Не считать ответом для ревью.

**Что будет, если переопределить только equals, но не hashCode?**

Сломаются hash-структуры: HashMap, HashSet, Hashtable. Положили объект — посчитался один hashCode, переопределённый equals говорит «они равны», но другой hashCode значит другой бакет. Не найдёшь, что положил. Поэтому при переопределении equals — обязательно переопределяй hashCode.
