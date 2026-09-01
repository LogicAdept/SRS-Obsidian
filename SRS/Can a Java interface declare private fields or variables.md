<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP/Interfaces #SRS

# Can a Java interface declare private fields or variables?

> [!abstract] Short answer
> **No.** Every field in an interface is implicitly **`public static final`**. The only field modifiers you may write are `public`, `static`, and `final` (plus annotations). `private` and `protected` are not in that set, so `private int n = 1;` is a compile-time error. **Methods** may be `private` (Java 9); that does not extend to fields. Implied modifiers: [[How would you explain default modifiers for fields and methods inside interfaces]]. Private methods: [[Can a Java interface declare private methods]]. Access in general: [[How do Java access modifiers work]].

## Constants only; `private` is not a field modifier

Interface fields are constant declarations. Each declarator **must** have an initializer. At run time the initializer runs once, when the interface is initialized — a static context, so `this` / `super` are illegal. There is no instance field and no uninitialized field.

A **class** field may be `public`, `protected`, `private`, or package-private, and may be instance or `static`. An interface field cannot: omitting the modifiers still yields `public static final`, **not** package-private. Writing `private` or `protected` on the field is illegal even if you also write `static final`.

```d2
direction: down
field: "interface field" {
  width: 200
  height: 45
  style.fill: "#e3f2fd"
}
mods: "public static final only" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
priv: "private / protected / package" {
  width: 240
  height: 45
  style.fill: "#ffcdd2"
}
field -> mods
field -> priv: "illegal"
```

**Fig. 1.** Interface “variables” are public constants. Access narrower than `public` is not a field option.

```java
interface Limits {
    int MAX = 100;                 // public static final
    public static final int MIN = 0; // redundant, legal
}

class UsesLimits {
    static int cap = Limits.MAX;   // visible everywhere MAX is
}
```

**Listing 1.** Both fields are public constants. `Limits.MAX` is accessible from any package that can see `Limits`.

```java
// Conceptual: does not compile
interface Limits {
    private int hidden = 1;
    protected int mid = 2;
    int unset;                     // no initializer
}
```

**Listing 2.** Conceptual. `private` / `protected` are not constant modifiers. A missing initializer is a separate compile-time error.

## Private methods, nested types, and local variables

A method in an interface **may** be `private` or `private static` (Java 9). Those methods have a block body, are not inherited, and exist so `default` / `static` methods can share code. That is a **method** rule. It does not add private fields.

```java
interface Limits {
    int MAX = 100;

    private static int clamp(int n) {
        return n < 0 ? 0 : Math.min(n, MAX);
    }

    static int bounded(int n) {
        return clamp(n);
    }
}
```

**Listing 3.** `clamp` is a private method. `MAX` is still a public constant. There is no private companion field.

Member **classes** declared in an interface are implicitly `public` and `static`. The nested **type** cannot itself be `private` or `protected`. Inside that class, ordinary class field rules apply, including `private` instance fields:

```java
interface Limits {
    class Holder {
        private final int n;

        Holder(int n) {
            this.n = n;
        }

        int get() {
            return n;
        }
    }
}
```

**Listing 4.** `Holder.n` is a private field of a nested **class**, not of `Limits`. `private class Holder` on the interface would not compile.

Local variables in `default`, `private`, or `static` methods are not fields and do not take access modifiers. You cannot write `private int x = 1;` in a method body. The cue’s “variables” that live on the interface type are the constant fields.

Abstract classes **can** declare `private` fields; implementing classes cannot see them, and constructors can initialize them. That is a class rule, not an interface rule: [[What is the difference between a Java interface and an abstract class]]. Nested types as members: same idea as constructors on nested classes — [[Can a Java interface declare a constructor]].

> [!warning] “Java 9 added private members” does not mean private fields
> Java 9 added **private methods** so non-abstract interface methods can share code. Fields were already, and still are, `public static final` only. An answer that says “interfaces can have private members now” is incomplete.

> [!warning] Dropping `public` does not hide the field
> `int MAX = 100;` is still `public`. Package-private is a **class** default, not an interface default. Same trap as methods: omitted access is `public`, not package-private.

> [!warning] A private field inside `interface I { class C { private int x; } }` is not `I`’s field
> Nested classes follow class field modifiers. The enclosing interface still cannot declare `private int x`.

> [!tip] Interview answer
> No. Interface fields are implicitly public, static, and final constants; `private` and `protected` are not legal field modifiers, and every field needs an initializer. Private methods on interfaces are legal since Java 9, but that is methods only. A nested class inside the interface may have private fields of its own — those belong to the class, not to the interface.
