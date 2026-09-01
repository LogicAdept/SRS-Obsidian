<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/OOP/Constructors #SRS

# How would you explain instance initializer blocks versus constructors?

> [!abstract] Short answer
> A **constructor** is the **class-named** initializer that **`new` actually invokes**: it has **parameters**, **overloads**, `this(...)` / `super(...)`, and access. An **instance initializer** is a **nameless `{ ... }` in the class body**. It runs **once per construction of that class**, in **textual order** with instance field initializers, **after** the **superclass** constructor returns and **before** this constructor’s **epilogue**. It **cannot** see constructor parameters. `this(...)` **does not** run the initializers a second time. Constructors: [[What is constructor]]. Blocks: [[How would you explain static and instance initializer blocks in Java]]. Order: [[What is the order of constructors and initializer blocks in a class hierarchy]].

## Arguments vs shared setup after `super`

**Constructor.** Looks like a method with **no result type**. Not a member: not inherited, not overridden. Default no-arg if you declare none ([[How would you explain the default constructor synthesized by the Java compiler]]). Its job is to take the **`new` arguments** and finish this object (and to chain `super` / `this`).

**Instance initializer.** Same `{ }` you might mistake for a block in a method, but it sits in the class. It **is** allowed `this` / `super`. It **must** complete normally; **`return` is illegal**. It is **not** `static { }` ([[How would you explain static and instance initializer blocks in Java]]). Several may appear; they interleave with field initializers **left to right in the source**.

**When each runs.** For `new C(args)`, the constructor that eventually calls `super(...)` (explicit or implicit) runs this class’s instance initializers, then its epilogue. A constructor that only does `this(...)` runs its prologue, delegates, then **only its epilogue** — initializers already ran in the delegated constructor.

**Use `{ }` when** every constructor of this class needs the same code that does **not** depend on which overload was called (including anonymous classes, which **cannot** declare a constructor). **Use a constructor when** you need arguments, overloads, or `super(args)`.

```d2
direction: down
nw: "new C(args)" {
  width: 160
  height: 36
  style.fill: "#e3f2fd"
}
sup: "super(...)  [or this(...) → skip to epilogue]" {
  width: 340
  height: 45
  style.fill: "#fff8e1"
}
ini: "{ } and instance field initializers\ntextual order" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
epi: "constructor epilogue\nuses parameters" {
  width: 260
  height: 45
}
nw -> sup
sup -> ini: "after superclass ctor"
ini -> epi
```

**Fig. 1.** Initializers sit between `super` returning and the rest of this constructor. `this()` skips that middle step for the current constructor.

```java
class Point {
    final String tag;
    int x, y;

    {
        tag = "p";
        y = -1;
    }

    Point() {
        this(0);
    }

    Point(int x) {
        this.x = x;
    }
}

class Use {
    static Point a = new Point();
    static Point b = new Point(3);

    static Runnable r = new Runnable() {
        {
            // anonymous class has no declared constructor
        }

        @Override
        public void run() {}
    };
}
```

**Listing 1.** Both `Point` constructors share `tag` and `y` from `{ }`. `Point()`’s `this(0)` does not run `{ }` twice. `this.x = x` needs the constructor parameter.

| | Constructor | Instance initializer |
| Invoked as | `new C(args)` / `this` / `super` | Never by name |
| Parameters | Yes | No |
| Overload | Yes | No |
| `this()` / `super()` | Yes | No |
| Runs | That constructor’s prologue/epilogue | After `super` of this class, with field initializers |

> [!warning] `{ }` cannot read the constructor’s parameters
> There is no `x` from `Point(int x)` inside the initializer. Assign from parameters in the constructor **epilogue**. Putting `this.x = x` in `{ }` will not compile.

> [!warning] `this(0)` does not double-run `{ }`
> Initializers run in the constructor that calls **`super`**. The no-arg constructor only wraps `this(0)`. Shared setup still happens **once**.

> [!warning] Instance `{ }` is not `static { }` and not a constructor
> `static { }` runs at **class** initialization, once. `{ }` runs per **object**. `void Point() {}` is a method. A constructor has **no** return type.

> [!tip] Interview answer
> A constructor is what new calls: it has a name, parameters, and this or super chaining. An instance initializer is a brace block in the class body that runs after the superclass constructor, in textual order with instance field initializers, before the rest of this constructor. Use it for setup common to every constructor that does not need those parameters; use constructors for arguments. this() does not run the initializers again.
