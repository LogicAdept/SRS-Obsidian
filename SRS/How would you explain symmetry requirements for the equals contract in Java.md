<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/OOP #Java/Language/Records #SRS

# How would you explain symmetry requirements for the `equals` contract in Java?

> [!abstract] Short answer
> For non-null `x` and `y`, **`x.equals(y)` and `y.equals(x)` must be the same boolean**. If `x` thinks `y` is equal, `y` must think `x` is equal. The usual break is a subclass that adds identity state and uses `instanceof`: the base instance accepts the subclass, the subclass rejects the base.

## The rule

The contract: `x.equals(y)` is `true` if and only if `y.equals(x)` is `true`. Together with reflexivity and transitivity this keeps a single partition. [[What properties does an equivalence relation induced by equals have]] is that partition.

```java
x.equals(y) == y.equals(x)  // required, both true or both false
```

**Listing 1.** Symmetry. It must hold for every pair your `equals` can see, including mixed subclass pairs.

```d2
direction: down
p: "Point(1,2)" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
cp: "ColorPoint(1,2,RED)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
yes: "p.equals(cp) true\n(instanceof Point)" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
no: "cp.equals(p) false\n(not a ColorPoint)" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}

p -> yes
cp -> no
```

**Fig. 1.** Conceptual mixed-type break. One direction uses the superclass test; the other demands the extra field.

## How implementations fail it

A superclass `equals` that returns true for `o instanceof Point` will accept a `ColorPoint` with the same coordinates. The subclass `equals` that also requires `color` returns false for a plain `Point`. Symmetry is gone. Transitivity then fails with two colors of the same coordinates: each color equals the plain point, but not each other.

Mitigations that restore symmetry:

- Make the value class **`final`** (or a `record`) so there is no subclass with extra state.
- Compare `getClass() == o.getClass()` so a subclass instance is never equal to a base instance. Cross-class equality is refused in both directions.
- If you keep `instanceof`, subclasses must **not** tighten equality with new fields. They may only add state that does not participate in `equals`.

`Objects.equals(a, b)` is symmetric for nulls: both null is true; exactly one null is false. Your override still owes symmetry among non-null values. Comparing your type to a `String` or another unrelated class must be false **both** ways; a sloppy `o instanceof String` branch that returns true from one type only is another symmetry bug.

> [!warning] `instanceof` is not automatically symmetric
> It correctly rejects `null` and unrelated types. It does **not** protect you from a subclass that overrides `equals`. Interview answers that stop at “use `instanceof`, never `getClass`” skip this axiom. [[How do you override equals correctly in Java]] is where to pick the policy.

> [!tip] Interview answer
> **Symmetry means `x.equals(y)` and `y.equals(x)` agree. The classic failure is `Point`/`ColorPoint` with `instanceof` and an extra field. Fix it by forbidding subclasses, by using `getClass()`, or by not putting subclass fields into `equals`. Collections will otherwise treat the same pair as equal or not depending on which object is the receiver.**
