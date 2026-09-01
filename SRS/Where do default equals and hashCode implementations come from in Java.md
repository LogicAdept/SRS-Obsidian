<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals/Contract #Java/OOP #Java/Language/Records #Java/Versions/16 #SRS

# Where do default `equals` and `hashCode` implementations come from in Java?

> [!abstract] Short answer
> From **`java.lang.Object`**. Every class and every array type inherits those methods. You do not write them unless you **override**. Until then, `equals` and `hashCode` are the implementations defined on `Object`, not copies pasted into your source file.

## `Object` is the root

The class `Object` is a superclass of all other classes. All class types and array types inherit its methods, including `equals` and `hashCode`. The language summary of `hashCode` is that it is useful together with `equals` in hash tables such as `HashMap`.

```d2
direction: down
obj: "java.lang.Object\nequals / hashCode" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
cls: "Your class\n(no override)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
arr: "Array types\nT[]" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
use: "Calls use Object's methods" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

obj -> cls -> use
obj -> arr -> use
```

**Fig. 1.** Defaults arrive by inheritance from `Object`. Arrays are not exempt.

A class that never mentions `equals` still has `public boolean equals(Object)`. The compiler does not generate a value-based pair from your fields (except a `record`, which does declare both from its components). [[How would you explain default equals and hashCode inherited from Object]] is what those inherited bodies do. [[How are hashCode and equals implemented in java.lang.Object]] is the `Object` code’s semantics.

## What is *not* the source

Interfaces do not supply `Object.equals` / `hashCode`; a class still inherits them from `Object` (or from a superclass that already overrode them). `Objects.equals` and `Objects.hashCode` are static helpers, not the default instance methods. `System.identityHashCode` is a way to obtain the **default** hash even after an override; it is not where the inherited method “lives.”

If a superclass already overrode the pair, subclasses inherit **that** override, not `Object`’s, until they override again. That is ordinary inheritance, and it is how a broken `equals` in a parent poisons children.

> [!warning] “The compiler writes equals from my fields”
> Ordinary classes do not. Two `new Point(1, 2)` instances use identity `equals` until you override. Only records (and similar generated types) provide component-based `equals`/`hashCode` without a hand-written pair.

> [!tip] Interview answer
> **The defaults come from `java.lang.Object` and are inherited by every class and array. You keep identity equality by doing nothing. You get value equality only by overriding both methods (or by using a `record`). Helpers like `Objects.hash` are not the inherited implementation.**
