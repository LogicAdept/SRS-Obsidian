<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/String #Java/Arrays #SRS

# How do you compare objects for equality in Java?

> [!abstract] Short answer
> Use **`equals`** for logical equality, **`==`** only for “same reference or both null,” and **`Objects.equals`** when either side may be null. Compare array **contents** with `Arrays.equals` / `deepEquals`, not `==` or `array.equals`. Do not use `hashCode` or `compare` as a substitute for `equals`.

## Pick the operator that matches the question

```text
same object?           a == b          (also both null)
logical value?         a.equals(b)     (NPE if a is null)
null-safe value?       Objects.equals(a, b)
array contents?        Arrays.equals(a, b)  or deepEquals
ordered the same?      compare(a, b) == 0   (not Map/Set equality)
```

**Listing 1.** Dispatch. `Objects.equals` is: both `null` → `true`; else if `a != null` then `a.equals(b)`; else `false`.

For `String`, the language says `==` tests whether the operands are the same `String` object, even when the character sequences match. Content is `s.equals(t)`. Wrappers such as `Integer` override `equals`; `==` on two `Integer` instances is still identity (caching of small values is an implementation detail, not a comparison API).

```java
Objects.equals(user.getName(), "Ada");
Arrays.equals(left, right);
list.contains(key);   // uses equals on elements
map.containsKey(key); // hash then equals
```

**Listing 2.** Typical calls. `contains` / `get` do not use `==` except as a fast path inside `HashMap` before `equals`.

`List.equals` compares implementations by size and `Objects.equals` on corresponding elements, in order. That is why `ArrayList` and `LinkedList` with the same sequence compare equal.

## What not to use

`a.hashCode() == b.hashCode()` does not mean `equals`. [[What is the difference between equals and hashCode contracts]] is that one-way implication. `Comparator.compare` may return `0` for values that are not `equals`, and then a `TreeSet` violates the `Set` contract. Prefer a comparator consistent with `equals` unless you document otherwise.

For `float`/`double` fields inside your own `equals`, do not use primitive `==` (`NaN` is not equal to itself; `+0.0 == -0.0`). `Double.equals` uses representation equivalence. [[How do you override equals correctly in Java]] is the field-level recipe.

> [!warning] `array.equals(other)` is identity
> Arrays inherit `Object.equals`. Two `new int[]{1}` instances are not equal. Use `Arrays.equals`. `Objects.deepEquals` is for nested arrays or mixed nulls.

> [!tip] Interview answer
> **Value equality is `equals` (or `Objects.equals` if null is possible). `==` means the same object. Array contents need `Arrays.equals`. Hash maps already call `equals` after `hashCode`. Do not compare strings or domain objects with `==`, and do not treat `compare == 0` as `equals` unless the order is consistent with equals.**
