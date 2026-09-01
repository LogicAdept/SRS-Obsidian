<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/Language/Modifiers/Static #Java/Exceptions/Checked #SRS

# How would you explain static and instance initializer blocks in Java?

> [!abstract] Short answer
> A **`static { }`** block runs when the **class is initialized**, together with `static` field initializers, in **textual order**, once per class. An instance **`{ }`** block runs when an **object is created**, together with instance field initializers, in textual order, **after** `super(...)` returns and **before** the rest of that constructor. `this(...)` **skips** the initializers in that constructor; they run in the constructor that actually calls `super`. vs constructors: [[How would you explain instance initializer blocks versus constructors]]. Field sites: [[Where may static and instance fields be initialized in Java]]. Order: [[What is the order of constructors and initializer blocks in a class hierarchy]]. Static-only: [[How would you explain static initializer blocks in Java]]. Constructors: [[What is constructor]].

## Two times, two `{ }` forms

**Static initializer (`static { }`).** Executed as part of **class initialization**, along with initializers of class variables. Superclasses initialize first. Triggers include `new`, a `static` method call, or use of a non-constant `static` field—not mere loading of the class, and not use of a **constant variable**. `this` and `super` are forbidden (static context). Interfaces initialize their constant fields; they do not have `static { }` blocks.

**Instance initializer (`{ }` in the class body).** Executed as part of **instance creation** for **this** class: memory is zeroed, constructors recurse to `Object`, then this class’s instance initializers and instance-variable initializers run left-to-right, then the constructor body after `super`. Every `new` runs them again. `this` is allowed. They do not see constructor parameters. Fields: [[How would you explain kinds of variables in Java such as local and instance]].

**Shared compile-time rules.** Neither kind may contain `return`. Both must be able to complete normally. Simple-name reads of a field that is declared **textually later** in the same class (in a field or `{ }` initializer) are illegal. If a constructor starts with `this(...)`, this class’s instance `{ }` blocks do **not** run in that constructor; they run once on the path that invokes `super`. Use a block when initialization needs **statements** (loops, `try`/`catch`), not only `field = expr`. Anonymous classes cannot declare a constructor, so instance `{ }` is their shared setup.

```d2
direction: down
c: "class initialization\nstatic fields + static { }" {
  width: 280
  height: 45
  style.fill: "#e3f2fd"
}
s: "super(...) finishes" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
i: "instance fields + { }" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
b: "constructor body" {
  width: 180
  height: 36
  style.fill: "#f3e5f5"
}
c -> s: "then new"
s -> i
i -> b
```

**Fig. 1.** Class `{ }` runs at class init. Instance `{ }` runs after `super`, before the constructor epilogue.

```java
class Demo {
    static int s;
    int n;

    static {
        s = 1;
    }

    {
        n = 2;
    }

    Demo() {}

    Demo(boolean chain) {
        this();
    }
}

class Use {
    static void go() {
        Demo a = new Demo();
        Demo b = new Demo(true);
        int x = Demo.s;
    }
}
```

**Listing 1.** `s` is set once, when `Demo` initializes. `n` is set to `2` for both `a` and `b`. `Demo(boolean)` does not run `{ }` itself; `Demo()` does, after `super()`.

> [!warning] `this()` does not run instance `{ }` a second time
> Initializers attach to the constructor that invokes `super` (explicit or implicit). Chaining with `this(...)` shares one run. You cannot pass constructor arguments into `{ }`.

> [!warning] Forward reference by simple name is a compile-time error
> `static int a = b; static int b = 1;` and the instance analogue fail if the use is a read to the left of the declaration. `this.b` or a qualified name can still see a default `0` at run time—do not rely on that.

> [!warning] Load is not initialization
> A compile-time constant `static final` can be used without initializing the class. A static initializer that throws completes class initialization **abruptly**; later use of the class fails the same way. Instance initializer failure fails that `new`. A checked exception from an **instance** `{ }` must be listed on **every** constructor ([[How would you explain what happens if in block initialization occurs exceptional situation]]). A **static** `{ }` must not throw a checked exception ([[Can a static initializer throw a checked exception]]).

> [!tip] Interview answer
> `static { }` initializes the class once, in source order with static field initializers, when the class is first used in a way that requires initialization. `{ }` initializes each instance, in source order with instance field initializers, after the superclass constructor returns. Neither may `return`. A constructor that calls `this(...)` does not run this class’s instance initializers itself.
