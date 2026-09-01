<!--
reps: 0
priority: 0
-->
#Patterns/GoF/Creational #Java/OOP/Constructors #Java/Library/Lombok #SRS

# What are the advantages of the Builder pattern over constructors?

> [!abstract] Short answer
> Java constructors have **positional** parameters and **overloads**, not names ([[What is constructor overloading in Java]]). A **builder** holds the arguments, exposes **named** methods, then `build()` calls a **private constructor** once ([[How would you explain private constructors and common patterns that use them in Java]]). That gives optional fields without a telescope of overloads, less `int`/`int` mix-ups, validation before the product exists, and an **immutable** result ([[How would you explain immutable classes in Java]]). Pattern: [[How would you explain the Builder design pattern]]. Platform example: `Locale.Builder` versus `Locale` constructors / `Locale.of`. Not `StringBuilder` ([[How would you explain java.lang.StringBuilder]]).

## Named steps vs a positional parameter list

**What constructors do badly.** Each extra optional field wants another overload, or callers pass `null`/sentinel values. Two `int` parameters swap silently. You cannot skip the middle argument. Telescoping `this(...)` chains duplicate the same assignments. A public constructor that leaves fields to later setters publishes a **half-initialized** object.

**What a construction builder does.** The builder stores constructor arguments in **its** fields, then creates the **immutable** product in one shot. Callers write `new Locale.Builder().setLanguage("sr").setScript("Latn").setRegion("RS").build()`. `Locale.Builder` is documented as checking syntax **unlike** the constructors and `Locale.of()`: the `Locale` you get is well-formed. Setters return the builder so calls chain. `clear()` reuses the same builder.

**Also vs constructors.** You can validate combinations only at `build()` (width and height both positive). Required values can sit on the builder’s constructor; optionals stay as methods. The product’s constructor stays `private` and tiny. Nested `Builder` is in the same nest, so it may call that constructor.

**Cost.** An extra type and extra allocations. Pointless for two required fields. Lombok `@Builder` only **generates** this shape; it is not a different pattern. vs Facade: [[What is the difference between the Builder and Facade design patterns]].

```d2
direction: down
ctor: "C(int, int, int, String)\nposition, overloads" {
  width: 260
  height: 50
  style.fill: "#ffebee"
}
b: "Builder\nnamed setters, then build()" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
p: "immutable product" {
  width: 180
  height: 36
  style.fill: "#e3f2fd"
}
b -> p
```

**Fig. 1.** Constructors pass a list. A builder names each part and constructs once.

```java
final class Box {
    private final int width;
    private final int height;
    private final String label;

    private Box(int width, int height, String label) {
        this.width = width;
        this.height = height;
        this.label = label;
    }

    static final class Builder {
        private int width = 1;
        private int height = 1;
        private String label = "";

        Builder width(int width) {
            this.width = width;
            return this;
        }

        Builder height(int height) {
            this.height = height;
            return this;
        }

        Builder label(String label) {
            this.label = label;
            return this;
        }

        Box build() {
            if (width <= 0 || height <= 0) {
                throw new IllegalStateException();
            }
            return new Box(width, height, label);
        }
    }
}

class Use {
    static Box go() {
        return new Box.Builder().width(2).height(3).label("a").build();
    }
}
```

**Listing 1.** `new Box(2, 3, "a")` would not say which `int` is width. The builder does. `Box` itself has no setters.

> [!warning] `StringBuilder` is not this pattern
> `StringBuilder` is a **mutable buffer** for characters. Construction Builder is a **draft of constructor arguments** for an immutable (or otherwise finished) product. `Locale.Builder` is the JDK type to cite.

> [!warning] Setters on the product are not a builder
> JavaBeans-style `setX` after `new C()` leaves a visible incomplete object and fights immutability. The product should appear only from `build()`.

> [!warning] Do not use a builder for every class
> Two parameters: write a constructor. A builder shines when many optionals, same types, or cross-field checks belong together. `@Builder` without understanding `build()` still allows invalid states if you skip validation.

> [!tip] Interview answer
> Constructors take a positional list and scale poorly when many fields are optional or the same type. A builder names each assignment, can validate at `build()`, and then calls a private constructor so the product can be immutable. `Locale.Builder` does that in the JDK; Lombok `@Builder` is only a generator for the same idea.
