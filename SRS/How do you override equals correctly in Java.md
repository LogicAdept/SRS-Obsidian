<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Java/OOP #Java/Language/Records #SRS

# How do you override `equals` correctly in Java?

> [!abstract] Short answer
> Override the exact signature `public boolean equals(Object o)`, keep the five contract properties, compare only the fields that define logical identity, and provide a compatible `hashCode`. Prefer a final, immutable value class. If the class is extensible, choose an equality policy (`instanceof` versus `getClass()`) and keep subclasses from breaking symmetry.

## Decide whether value equality is needed

Keep the inherited identity equality when each instance is unique. Override `equals` when distinct instances should represent the same logical value, for example a coordinate, a money amount, or an identifier. That choice is semantic; the contract only constrains how the chosen equality must behave. See [[When should you override equals in Java]] and [[How would you explain the Object equals method contract]].

## Required implementation steps

1. Declare `@Override public boolean equals(Object o)`. A method such as `equals(Name)` has a different signature, so it is an overload: the class still inherits `Object.equals(Object)`.
2. Return `true` immediately when `this == o`. That matches the identity relation used by the inherited implementation and satisfies reflexivity for the same reference.
3. Reject incompatible types. For `o instanceof T`, a `null` left operand yields `false`, so a separate `o == null` check is unnecessary. `getClass()` compared with `==` also rejects a subclass instance.
4. Cast only after the type check succeeds; otherwise the cast can throw `ClassCastException`.
5. Compare the fields that define identity. Use `==` for integral and `boolean` primitives. For `float` and `double`, do not use `==`: it is not an equivalence relation (`NaN != NaN`, while `+0.0 == -0.0`). Use representation equivalence, for example `Double.compare(a, b) == 0` or `Double.doubleToLongBits`. For nullable references, `Objects.equals` is null-safe. For arrays, use `Arrays.equals` or `Arrays.deepEquals`, not `==`.
6. Override `hashCode` from a compatible set of fields, as required by [[How would you explain the equals and hashCode contract together in Java]].

```java
import java.util.HashSet;
import java.util.Set;

public class Main {
    static class Name {
        final String value;

        Name(String value) {
            this.value = value;
        }

        public boolean equals(Name other) {
            return other != null && value.equals(other.value);
        }
    }

    public static void main(String[] args) {
        Set<Name> names = new HashSet<>();
        names.add(new Name("Ada"));

        System.out.println("containsAda=" + names.contains(new Name("Ada")));
        System.out.println(
                "directEquals=" + new Name("Ada").equals(new Name("Ada"))
        );
    }
}
```

**Listing 1.** Java 8+ overload trap. `equals(Name)` is legal overloading, not overriding, so `Name` still inherits identity equality from `Object`. `HashSet.contains` reports a hit only when `Objects.equals(o, e)` is true for some stored element `e`; that path uses `equals(Object)`, not `equals(Name)`. A compile-time call `new Name("Ada").equals(new Name("Ada"))` can still select the overload and print `true`.

> [!warning] `@Override` is what makes the compiler reject the trap
> Annotating `equals(Name)` with `@Override` is a compile-time error, because that method does not override a supertype method and is not override-equivalent to `Object.equals(Object)`. Without the annotation the overload compiles, and hash-based collections keep treating equal values as distinct.

## Inheritance can break symmetry

```java
public class Main {
    static class Point {
        final int x;
        final int y;

        Point(int x, int y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof Point)) return false;
            Point other = (Point) o;
            return x == other.x && y == other.y;
        }

        @Override
        public int hashCode() {
            return 31 * Integer.hashCode(x) + Integer.hashCode(y);
        }
    }

    static class ColorPoint extends Point {
        final String color;

        ColorPoint(int x, int y, String color) {
            super(x, y);
            this.color = color;
        }

        @Override
        public boolean equals(Object o) {
            if (!(o instanceof ColorPoint)) return false;
            ColorPoint other = (ColorPoint) o;
            return super.equals(other) && color.equals(other.color);
        }

        @Override
        public int hashCode() {
            return 31 * super.hashCode() + color.hashCode();
        }
    }

    public static void main(String[] args) {
        Point point = new Point(1, 2);
        ColorPoint colored = new ColorPoint(1, 2, "red");

        System.out.println("pointEqualsColored=" + point.equals(colored));
        System.out.println("coloredEqualsPoint=" + colored.equals(point));
    }
}
```

**Listing 2.** Java 8+ symmetry failure. `Point.equals` accepts a `ColorPoint` through `instanceof`, but `ColorPoint.equals` rejects a plain `Point`. The two directions disagree, which violates the contract. [[How would you explain symmetry requirements for the equals contract in Java]] isolates that rule.

```d2
direction: down
point: "Point.equals(ColorPoint)\ninstanceof Point -> true\ncompare x, y" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
color: "ColorPoint.equals(Point)\ninstanceof ColorPoint -> false" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
break: "x.equals(y) != y.equals(x)\nsymmetry is broken" {
  width: 280
  height: 85
  style.fill: "#ffebee"
}

point -> break: true
color -> break: false
```

**Fig. 1.** `instanceof` plus extra subclass identity state is a common way to break symmetry.

Safer policies:

- Make the value class `final` so no subclass can add identity state.
- Use `getClass()` instead of `instanceof` if mixed-class equality must be rejected.
- Keep subclasses from changing equality; they may add behavior, not identity fields.

`getClass()` is not automatically “more correct”. It rejects mixed-class comparisons, which restores symmetry for this example, but it also means a subclass instance is never equal to a parent instance with the same coordinates. Choose that outcome deliberately.

## Field selection and mutability

Compare every field that participates in the logical identity, and only those fields. For `double`/`float` identity, representation equivalence treats every `NaN` as equal to every other `NaN` and treats `+0.0` as different from `-0.0`. Primitive `==` does the opposite on both points. Arrays compare by contents through `Arrays.equals`; nested arrays need `Arrays.deepEquals`. Array `==` is only reference identity.

If a field can change after construction, do not use that object as a `HashMap` key or `HashSet` element. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] shows the lookup failure. Prefer `final` primitives, `String`, or records whose components are themselves immutable.

> [!tip] Interview answer
> **Override `equals(Object)`, not a tighter overload. Check identity, then type, then identity fields, and write a matching `hashCode`. Prefer a final immutable class. If you use `instanceof` in an extensible hierarchy, a subclass that adds identity state can break symmetry; `getClass()` or a final class avoids that trap.**
