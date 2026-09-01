<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection/Members #Java/Immutability #SRS

# Can you change the value of a final field using reflection?

> [!abstract] Short answer
> **Sometimes, through `Field.set` under a tight write contract — not by stripping `FINAL` off `Field.modifiers`.** After `setAccessible(true)` succeeds, Java SE 21 grants write access only when the field is **non-static** and its declaring class is **neither a record nor a hidden class**. Static finals, record component fields, and hidden-class finals throw `IllegalAccessException`. A store that succeeds can still be invisible: constant variables are inlined, and the compiler may keep a `final` read in a register.

## Write access is four checks, not a modifiers hack

`Field.get` may read a `final` field, including the non-modifiable ones, once language access checks are suppressed ([[What does setAccessible do in the Reflection API]], [[What is the difference between getField and getDeclaredField]]). Write access is narrower. `Field.set` has write access **if and only if** all of these hold:

1. `setAccessible(true)` has succeeded on this `Field`
2. the field is **non-static**
3. the declaring class is **not hidden** (`Class.isHidden()`)
4. the declaring class is **not a record** (`Class.isRecord()`)

Any miss → `IllegalAccessException`. `AccessibleObject.setAccessible` states the same non-modifiable set: **static finals** in any class or interface, **finals in a hidden class**, **finals in a record**. For those, `accessible == true` enables **read** only.

That path is meant for deserialization / reconstruction of **blank** instance finals, before other code sees the object. Use anywhere else may have unpredictable effects, including other code still observing the old value.

```d2
direction: down
ask: "Field.set on a final" {
  width: 240
  height: 50
}
acc: "setAccessible(true)\nsucceeded?" {
  width: 220
  height: 70
}
st: "non-static?" {
  width: 180
  height: 50
}
kind: "not record,\nnot hidden?" {
  width: 180
  height: 70
}
ok: "write allowed" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
iae: "IllegalAccessException" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
ask -> acc
acc -> st: "yes"
acc -> iae: "no / InaccessibleObjectException"
st -> kind: "yes"
st -> iae: "static final"
kind -> ok: "yes"
kind -> iae: "record or hidden"
```

**Fig. 1.** Java SE 21 `Field.set` write access for `final` fields. The old `Field.modifiers` bit-twiddle is not in this contract.

```java
class Holder {
    private final String label;

    Holder(String label) {
        this.label = label;
    }

    String label() {
        return label;
    }
}

class Rewrite {
    static void setLabel(Holder holder, String value) throws Exception {
        var field = Holder.class.getDeclaredField("label");
        field.setAccessible(true);
        field.set(holder, value);
    }
}
```

**Listing 1.** Blank instance `final` (initialized in the constructor, not a constant variable). On Java SE 21 this `set` is the documented write. `getField` would not see `label` because it is private.

Private / package / protected members in another module still need the package **open** to the caller; otherwise `setAccessible` throws `InaccessibleObjectException` and you never reach `set` ([[What does setAccessible do in the Reflection API]]).

## What `Field.set` refuses

```java
class Demo {
    static final String CONST = "inlined";
    static final String LIVE = new String("not a constant variable");
}

record Point(int x, int y) {}
```

**Listing 2.** `CONST` is a constant variable (`final` `String` initialized with a constant expression). `LIVE` is `static final` but **not** a constant variable (`new String(...)` is not a constant expression). `Point.x` / `Point.y` are record component fields — `private final`, and not reflectively writable ([[Are Java record fields final]], [[How do you inspect a Java record with reflection]]).

`Field.set(null, …)` on `CONST` or `LIVE` throws `IllegalAccessException` because the field is static, regardless of `setAccessible` ([[How do you access static fields using reflection]]). `Field.set` on a `Point` component throws for the record check even after `setAccessible(true)` succeeded for **read**. Hidden classes (lookup-defined) are the same refusal.

`System.in` / `System.out` / `System.err` are a language special case: write-protected static finals changed only through `System.setIn` / `setOut` / `setErr`, not through application `Field.set`.

> [!warning] Do not strip `FINAL` on `Field.modifiers`
> Interview recipes call `Field.class.getDeclaredField("modifiers")`, `setAccessible(true)`, then `setInt(..., modifiers & ~Modifier.FINAL)`. On OpenJDK 21 that lookup fails: core reflection **filters every member** of `java.lang.reflect.Field` (internal `Reflection` field filter, wildcard). You get `NoSuchFieldException`, not a writable `modifiers` `Field`. You never needed that hack for ordinary instance finals; `setAccessible` plus `set` is the API. You cannot use it to unlock static / record / hidden finals either.

## Even a successful store may not be what you read

A **constant variable** is a `final` primitive or `String` initialized with a constant expression. Uses can be replaced at compile time with that value, so a later reflective store is not observed ([[What is a compile-time constant in Java]]). That applies to instance `final int n = 1` in the declaration as well as to `static final` constants.

JLS 17.5.3 also lets a compiler reorder a `final` read with a reflective write that is **not** in the constructor. Inside one thread, reading `x`, calling a method that reflectively sets `x`, then reading `x` again may still see the old value (the example in that section can yield `-1`, `0`, or `1`). The only pattern with reasonable semantics is: construct, update blank finals, then publish the object — the same freeze used after a constructor.

> [!warning] `final` is not a store you can rely on from other threads
> Reflective mutation is not a substitute for a constructor freeze you already published. Other threads, and even later reads in the same thread, may keep the original value. That is why this API exists for deserialization of blank finals, not for “make it mutable” ([[What are the drawbacks of using Java reflection]], [[Why is immutability valuable in Java programs]]).

> [!tip] Interview answer
> **Yes for an ordinary instance `final` after `setAccessible(true)`; no for static finals, records, and hidden classes — those `Field.set` calls throw `IllegalAccessException`.** Skip the `Field.modifiers` trick: on current JDKs `getDeclaredField("modifiers")` does not even see that field. **And a store that returns is not a guarantee you will read the new value** if the field was a compile-time constant or the JIT reused an old `final` load.
