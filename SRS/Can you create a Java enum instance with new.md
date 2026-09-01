<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can you create a Java enum instance with `new`?

> [!abstract] Short answer
> **No.** A class-instance creation expression must not name an enum class, so `new Week()` and `new Week() {}` do not compile — even inside the enum itself. The only instances are the constants declared in the enum body. Constructors exist, but they are `private` (they cannot be `public` or `protected`) and are invoked by the compiler for those constants, not by application `new`.

## `new` is illegal; constants are the instances

An enum class has no instances other than its enum constants. Each constant is an implicit `public static final` field. Want another value? Add another constant in the declaration — you cannot allocate one later ([[Can you add constants to a Java enum at runtime]]).

```d2
direction: down
decl: "enum Week { SUN, MON, … }" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
ok: "Week.SUN\n(the instance)" {
  width: 220
  height: 60
  style.fill: "#e8f5e9"
}
bad: "new Week()\ncompile error" {
  width: 220
  height: 60
  style.fill: "#ffcdd2"
}

decl -> ok
decl -> bad
```

**Fig. 1.** You refer to a constant. You never construct an enum type with `new`.

```java
enum Week { SUN, MON, TUE, WED, THU, FRI, SAT }

Week today = Week.MON;     // the instance is the constant
// Week w = new Week();    // compile error: cannot instantiate an enum class
// Week w = new Week() {}; // compile error: not even an anonymous subclass
```

**Listing 1.** Qualified `new`, inner-class `new`, and anonymous `new Type() {}` are all rejected when `Type` is an enum class.

## Constructors still exist — they are not for `new`

You may declare constructors in the enum body ([[Can you declare a constructor inside a Java enum]]). They cannot be `public` or `protected`; with no modifier they are `private`. The implicit default constructor is also `private`. A constructor must not contain `super(...)`; the compiler supplies the call to `Enum(String, int)`. That `Enum` constructor is `protected` and is documented as not for programmers to invoke.

Constants pass arguments in the constant list. The compiler instantiates each constant while the enum class initializes ([[When is a Java enum constructor invoked]]).

```java
enum Coin {
    PENNY(1), NICKEL(5);

    Coin(int cents) { this.cents = cents; } // implicitly private

    private final int cents;
    int cents() { return cents; }
}

// Coin.PENNY is created as if PENNY(1) ran that constructor
// new Coin(1) still does not compile
```

**Listing 2.** A constructor is how constants get state, not how callers allocate instances.

`java.lang.Enum` also closes the remaining holes: `clone` is `final` and throws `CloneNotSupportedException`; `Constructor.newInstance` throws `IllegalArgumentException` if the constructor belongs to an enum class; deserialization reuses the declared constant ([[How does Java serialization treat enum constants]]). That singleton property is why an enum constant is a valid singleton ([[How does an enum provide a Singleton]]).

> [!warning] “No public constructor” is true, but `new` is banned first
> Even a `private` constructor does not make `new Week()` legal inside `Week`. The `new` expression is a compile-time error because the type is an enum class, not because the constructor is out of reach. Accessibility is a second line of defense.

> [!warning] Reflection does not get you an extra instance
> `Constructor.newInstance` rejects enum constructors (`IllegalArgumentException`). `clone` cannot copy a constant. Those rules keep the instance set equal to the constant list, not merely “don’t call `new` in source.”

> [!tip] Interview answer
> **No — you cannot write `new` on an enum type; the only instances are the constants in the declaration.** Constructors may exist but are private and used by the compiler when each constant is created. Reflection and `clone` are blocked too, so you cannot manufacture another instance at run time.
