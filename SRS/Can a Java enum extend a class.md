<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can a Java enum extend a class?

> [!abstract] Short answer
> **No.** The direct superclass of every enum type `E` is already `Enum<E>`. An enum declaration has no `extends` clause, so you cannot name another class — and you cannot even write `extends Enum<E>`. Each class has a single superclass; that slot is taken.

## The superclass is fixed

`java.lang.Enum` is the abstract common base of every enum class (since Java 5). The language sets the direct superclass of enum `E` to `Enum<E>`. The enum declaration form is `enum Name [implements …] { … }` — there is an optional `implements` list, and there is no `extends` list.

A normal class cannot take that slot either: writing `class Foo extends Enum<Foo>` is a compile-time error. Only an enum class may extend `Enum`.

```d2
direction: down
color: "enum Color" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
en: "Enum<Color>\n(fixed superclass)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
obj: "Object" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
base: "class Base\ncompile error" {
  width: 220
  height: 70
  style.fill: "#ffcdd2"
}

color -> en -> obj
```

**Fig. 1.** `Color` already extends `Enum<Color>`. There is no second superclass, and the declaration cannot name one.

```java
class Base {}

enum Status {
    OK, FAIL
}

// enum Status extends Base { OK, FAIL }     // compile error: no extends clause
// enum Status extends Enum<Status> { OK }   // compile error: still no extends clause
// class Fake extends Enum<Fake> {}          // compile error: only an enum class may extend Enum
```

**Listing 1.** Legal enum versus the three `extends` shapes that do not compile. Shared behavior belongs on an interface: [[Can a Java enum implement an interface]].

## What comes from `Enum` versus the compiler

Members of enum `E` include what you declare, what `E` inherits from `Enum<E>`, the implicit `public static final` constant fields, and two implicit static methods generated on `E` itself.

Inherited from `Enum` (not a complete list): `name()`, `ordinal()`, `compareTo`, `equals`, `hashCode`, `clone`, `getDeclaringClass()`, `toString`. Those are real instance methods on the base class. Several are `final`.

Not inherited from `Enum`:

- `public static E[] values()` — implicitly declared **on `E`**
- `public static E valueOf(String name)` — implicitly declared **on `E`**

`Enum` does have a different static helper: `Enum.valueOf(Class<T> enumClass, String name)`. That is not the same method as `Color.valueOf("RED")`.

```java
enum Color { RED, GREEN }

Color.class.getSuperclass();          // java.lang.Enum
Color.RED.name();                     // Enum
Color.RED.ordinal();                  // Enum
Color.values();                       // implicit on Color
Color.valueOf("RED");                 // implicit on Color
Enum.valueOf(Color.class, "RED");     // static helper on Enum
```

**Listing 2.** Superclass check and the `values` / `valueOf` split. Converting a name to a constant: [[How do you convert a String to a Java enum]]. What `ordinal` means: [[What does ordinal do on a Java enum]].

> [!warning] `values()` and `valueOf(String)` are not on `Enum`
> Interview lists often dump them next to `name()` and `ordinal()`. `name()` and `ordinal()` are inherited. `values()` and the one-argument `valueOf` are compiler-generated on the concrete enum type. Reflecting on `java.lang.Enum` will not show them as instance methods.

## Final versus sealed — still no extra constants

If no constant has a class body, the enum is implicitly `final`. If at least one constant has a class body, the enum is implicitly `sealed`: the only permitted subclasses are the anonymous classes those constants declare. You cannot write `final` / `sealed` / `non-sealed` / `abstract` on the enum declaration itself.

Those anonymous classes extend the enum type so they can override methods. They do **not** let you introduce a new named subclass or a new constant. You still cannot write `class Extra extends Status` or grow the constant set at runtime ([[Can you add constants to a Java enum at runtime]]). Constant-specific bodies are also how an enum carries abstract methods ([[Can a Java enum have abstract methods]]).

```java
enum Op {
    PLUS {
        int apply(int a, int b) { return a + b; }
    },
    MINUS {
        int apply(int a, int b) { return a - b; }
    };
    abstract int apply(int a, int b);
}

// Op.class.getSuperclass() is still Enum
// PLUS.getClass() is an anonymous subclass of Op, and that subclass is final
```

**Listing 3.** Constant class bodies subclass the enum; they do not change the enum’s own superclass. That sealed-with-fixed-constants shape is one reason to reach for a sealed class hierarchy instead ([[When would you use a sealed class instead of an enum]]).

> [!warning] Constant bodies are not a back door to `extends Foo`
> `PLUS { … }` looks like subclassing, so it is easy to assume `enum Op extends Calculator`. The anonymous class extends `Op`, and `Op` still extends only `Enum<Op>`. Put shared protocol on an interface; put shared state in the enum body or in composition.

> [!tip] Interview answer
> **No — every enum already extends `Enum`, and the declaration has no `extends` clause.** Classes have one superclass, so you cannot also extend `Foo`. Share API with `implements`. `values()` and `valueOf(String)` are generated on the enum type; they are not inherited from `Enum`.
