<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/OOP/Constructors #SRS

# Can you declare a constructor inside a Java enum?

> [!abstract] Short answer
> **Yes.** An enum body may declare constructors, fields, methods, and nested types. Constructors cannot be `public` or `protected`. A constructor written with **no** access modifier is `private`, not package-private. They run for each constant as the enum class initializes; you still cannot call them with `new` ([[Can you create a Java enum instance with new]]).

## How the constructor is tied to the constants

Constants may take an argument list. Those arguments are passed to a constructor of the enum, chosen by ordinary overload resolution. If a constant omits `(…)`, the empty argument list is assumed — so a no-arg constructor must exist (explicit, or the implicit private default when you declare none).

Once you add any member after the constant list, a semicolon must separate the constants from the rest of the body. A trailing comma before that semicolon is legal.

```d2
direction: down
c: "PENNY(1)" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
ctor: "Currency(int value)\nimplicitly private" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
f: "this.value = 1" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}

c -> ctor -> f
```

**Fig. 1.** `PENNY(1)` is a constructor invocation performed while the enum class initializes, not a `new` in application code.

```java
enum Currency {
    PENNY(1), NICKEL(5), DIME(10), QUARTER(25);

    private final int value;

    Currency(int value) { // no modifier ⇒ private
        this.value = value;
    }

    public int value() { return value; }
}
```

**Listing 1.** Legal constructor. `private Currency(int value)` is the same thing written explicitly. `public` / `protected` here would not compile.

You may overload constructors. Different constants can pass different argument lists. The implicit default constructor (`private`, no parameters, no `throws`) appears only when the enum declares **no** constructors.

A constructor must not contain `super(...)`. The compiler supplies the call to `Enum(String, int)`. Constant class bodies cannot declare constructors at all ([[Can a Java enum have abstract methods]]).

## When the constructor runs — and what it must not touch

Each constant’s constructor runs during initialization of the enum class, once per constant, in declaration order ([[When is a Java enum constructor invoked]]). It is a compile-time error to read a `static` field of that enum from a constructor, instance initializer, or instance-field initializer, unless the field is a constant variable (`static final` of a primitive or `String`, initialized by a constant expression). Ordinary `static` maps and caches are not ready yet.

```java
enum Color {
    RED, GREEN, BLUE;

    // Color() { colorMap.put(name(), this); } // compile error: colorMap is not a constant variable

    static final java.util.Map<String, Color> colorMap = new java.util.HashMap<>();
    static {
        for (Color c : Color.values()) {
            colorMap.put(c.name(), c);
        }
    }
}
```

**Listing 2.** Build lookups in a static initializer after `values()` exists. Do not register constants from the constructor.

```java
enum Bad {
    A,           // looks for a no-arg constructor
    B(1);
    Bad(int n) {}
    // public Bad(int n) {}     // compile error
    // protected Bad(int n) {}  // compile error
    // Bad(int n) { super("B", 1); } // compile error: no explicit super
}
```

**Listing 3.** Conceptual: `A` does not match `Bad(int)`; `public`/`protected`/`super(...)` are all illegal on an enum constructor.

> [!warning] No-modifier is `private`, not package-private
> Interview dumps split on this. There is no package-private enum constructor. Omitting the keyword makes the constructor `private`. The only legal explicit access modifier is `private`. `public` and `protected` are compile-time errors.

> [!warning] A parameterized constructor replaces the default
> After you declare `Currency(int value)`, a constant written `EURO` with no arguments needs a no-arg constructor as well. The implicit private default is **not** generated once any constructor is declared.

> [!tip] Interview answer
> **Yes — enums can have constructors, but they are private (explicitly or by omitting the modifier) and you cannot make them public or protected.** Constants call them with `NAME(args)` while the class initializes. You still cannot `new` the enum, cannot write `super(...)`, and must not touch ordinary static fields from that constructor.
