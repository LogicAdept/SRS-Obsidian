<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/OOP #SRS

# How would you explain the `Object.equals` method contract?

> [!abstract] Short answer
> `equals` answers whether two object references represent the same **logical value**. The implementation inherited from `Object` uses identity, so it returns `true` only for two references to the same instance. An override may define value equality, but it must remain reflexive, symmetric, transitive, consistent while relevant state is unchanged, and return `false` for `null`.

## Default identity equality

For a non-null `left` whose class does not override `equals`, these expressions have the same result:

```java
left.equals(right)
left == right
```

**Listing 1.** Conceptual behavior of `Object.equals`: distinct instances are not equal even when all their fields contain identical values.

This default is appropriate when each instance has its own identity. Value classes usually override it so distinct instances can be equivalent by content. [[Where do default equals and hashCode implementations come from in Java]] covers the inherited behavior in more detail.

## The five required properties

For non-null references `x`, `y`, and `z`:

1. **Reflexive:** `x.equals(x)` is `true`.
2. **Symmetric:** `x.equals(y)` and `y.equals(x)` have the same result.
3. **Transitive:** if `x.equals(y)` and `y.equals(z)` are `true`, then `x.equals(z)` is also `true`.
4. **Consistent:** repeated comparisons give the same result while equality-relevant state remains unchanged.
5. **Non-null:** `x.equals(null)` is `false`.

These rules make equality an equivalence relation: objects are partitioned into groups whose members are interchangeable for the semantics represented by that class. See [[What properties does an equivalence relation induced by equals have]].

> [!warning] Consistency is conditional
> The contract does not require an object to remain equal forever. It requires stable results only while information used by `equals` is unchanged. Mutating equality state is still dangerous when an object is stored in a hash-based collection; [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] shows why.

## A correct final value class

```java
import java.util.HashSet;
import java.util.Set;

public class Main {
    static final class Coordinate {
        private final int x;
        private final int y;

        Coordinate(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Coordinate)) return false;

            Coordinate other = (Coordinate) o;
            return x == other.x && y == other.y;
        }

        @Override
        public int hashCode() {
            int result = Integer.hashCode(x);
            result = 31 * result + Integer.hashCode(y);
            return result;
        }
    }

    public static void main(String[] args) {
        Coordinate a = new Coordinate(1, 2);
        Coordinate b = new Coordinate(1, 2);
        Coordinate c = new Coordinate(1, 2);
        Coordinate different = new Coordinate(1, 3);

        boolean firstComparison = a.equals(b);
        boolean secondComparison = a.equals(b);

        System.out.println("reflexive=" + a.equals(a));
        System.out.println("symmetric=" + (a.equals(b) && b.equals(a)));
        System.out.println(
                "transitive=" + (a.equals(b) && b.equals(c) && a.equals(c))
        );
        System.out.println(
                "consistent=" + (firstComparison == secondComparison)
        );
        System.out.println("equalsNull=" + a.equals(null));
        System.out.println("unequal=" + a.equals(different));
        System.out.println(
                "equalObjectsSameHash=" + (a.hashCode() == b.hashCode())
        );

        Set<Coordinate> coordinates = new HashSet<>();
        coordinates.add(a);
        coordinates.add(b);
        System.out.println("setSize=" + coordinates.size());
    }
}
```

**Listing 2.** Java 8+ implementation exercising all five properties with representative values. `Coordinate` is final and immutable, and equal coordinates have equal hashes, so `HashSet` keeps one logical value.

The implementation follows a deliberate order:

1. The identity fast path handles the same reference immediately.
2. `instanceof` rejects `null` and incompatible types without a cast failure.
3. The cast is safe after the type check.
4. Only fields that define logical identity are compared.
5. `hashCode` is derived compatibly from those fields, as required by [[How would you explain the equals and hashCode contract together in Java]].

The contract determines the required properties, but it does **not** decide which fields define identity. That is a semantic decision for the class: coordinates may use both axes, while an entity may use a stable identifier. [[How do you override equals correctly in Java]] focuses on that implementation choice.

> [!warning] Override the correct signature
> The method must be `public boolean equals(Object o)`. A method such as `equals(Coordinate other)` merely overloads `equals`; collections still call the inherited `equals(Object)`. Use `@Override` so the compiler detects the wrong signature.

> [!warning] Inheritance needs an equality policy
> `instanceof` allows comparisons with subclasses. If a subclass adds identity state and changes `equals`, symmetry or transitivity can fail. A final value class avoids this issue. For an extensible hierarchy, decide explicitly whether equality may cross class boundaries; using `getClass()` rejects cross-class equality, while `instanceof` requires subclasses to preserve the base relation.

> [!tip] Interview answer
> **`Object.equals` uses reference identity by default. An override defines logical equality and must be reflexive, symmetric, transitive, consistent while relevant state is unchanged, and false for `null`. Override the exact `equals(Object)` signature, compare the fields that define identity, and provide a compatible `hashCode` whenever equal objects can be distinct instances.**
