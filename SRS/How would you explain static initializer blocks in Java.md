<!--
reps: 0
priority: 0
-->
#Java/OOP/Initialization #Java/Language/Modifiers/Static #SRS

# How would you explain static initializer blocks in Java?

> [!abstract] Short answer
> A **static initializer** is a `static { }` block in a class body. It runs when the **class is initialized**, together with **class-variable** initializers, in **textual order**, **once**. It is a **static context**: no `this`, `super`, or instance members. You cannot `return`. vs instance `{ }`: [[How would you explain static and instance initializer blocks in Java]]. Order: [[How would you explain static initialization order in Java]]. When the class initializes: [[How would you explain static and instance initializer blocks in Java]].

## `static { }` is class initialization code

The block exists to initialize **class variables** when a single expression on the field is not enough: loops, `try`/`catch`, several fields that must be set together. You may write **more than one** `static { }` in a class; they interleave with `static` field initializers **top to bottom**.

**When it runs.** Class initialization—not class loading. Typical triggers: `new`, a `static` method, or use of a **non-constant** `static` field. Superclasses initialize first. A compile-time constant `static final` can be used without running this class’s static initializers.

**Rules.** The block must be able to complete normally. `return` is a compile-time error. Simple-name reads of a class variable declared **later** in the same class are illegal. If the block (or a static field initializer) throws, and the throwable is not already an `Error`, it is wrapped in `ExceptionInInitializerError`; the class stays **erroneous**.

Interfaces have constant-field initializers, **not** `static { }` blocks. Instance `{ }` is a different construct and runs per `new` after `super` ([[How would you explain instance initializer blocks versus constructors]]).

```d2
direction: down
t: "class initialization of C" {
  width: 240
  height: 36
  style.fill: "#eceff1"
}
s: "superclass static init" {
  width: 200
  height: 36
  style.fill: "#e3f2fd"
}
b: "C's static fields + static { }\ntextual order" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
t -> s
s -> b
```

**Fig. 1.** Each `static { }` is a slice of C’s class-initialization sequence.

```java
class Cache {
    static final int[] table = new int[4];

    static {
        for (int i = 0; i < table.length; i++) {
            table[i] = i * i;
        }
    }

    static int s = 1;

    static {
        s = s + table[2];
    }
}

class Use {
    static int go() {
        return Cache.s;
    }
}
```

**Listing 1.** First `static { }` fills `table`. Then `s = 1`. Then the second block sets `s` to `5`. First use of `Cache.s` runs that sequence once.

> [!warning] Not a constructor and not an instance `{ }`
> There is no instance. You cannot use constructor parameters. `static { }` does not run again on `new Cache()` if the class is already initialized. An instance initializer `{ }` without `static` is a different member and a common mix-up.

> [!warning] Failure poisons the class
> After `ExceptionInInitializerError`, later use of the class throws `NoClassDefFoundError`. Do not catch that and retry initialization; the class will not run `static { }` again.

> [!warning] `this` is illegal; forward reads are illegal
> Unqualified instance fields and methods are a compile-time error. `int a = b; static int b = 1;` in static initializers is a forward-reference error. Load still is not initialization.

> [!tip] Interview answer
> A static initializer is `static { }` code that runs once when the class is initialized, in source order with static field initializers, after the superclass is initialized. It is for class-level setup that is more than a field expression. It cannot `return` or use `this`, and a thrown exception makes later use of the class fail.
