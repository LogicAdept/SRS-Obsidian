<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS

# Which Java language constructs are not subclasses of `java.lang.Object`?

> [!abstract] Short answer
> **Primitives** (`int`, `boolean`, …) are not classes and not subclasses of `Object`. **Interfaces** are not classes either — they do not `extend Object` (they may *implicitly declare* `Object`’s public instance methods as `abstract`). The nameless **null type** is not a class. **`Object` itself** has no superclass. **Arrays are objects**: every array type acts as if its direct superclass is `Object` (`int[]` assigns to `Object`). Wrappers (`Integer`) are ordinary classes and **do** extend `Object`.

## Subclass is a class relation

Every class except `Object` is an extension of one existing class; that relation bottoms out at `Object`. Enums extend `Enum`, records extend `Record`, both of which sit under `Object`. An interface has **superinterfaces**, not a superclass; a class **implements** interfaces. Primitives are a different kind of type altogether: no `extends`, no `getClass()` on an `int` value. Boxing exists so an `int` can become an `Integer` that *is* an `Object`. [[Why cannot a Java primitive variable be null]] is why `int` is not a reference; [[What is the difference between int and Integer in Java]] is the wrapper that *is* an `Object`; [[What are autoboxing and unboxing in Java]] is the bridge; [[Is a Java array a primitive or an object]] is the array exception people miss.

```d2
direction: down
obj: "java.lang.Object" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
cls: "classes / enums / records" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
arr: "array types\n(act as if superclass Object)" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
not: "primitives, interfaces,\nnull type, Object itself" {
  width: 300
  height: 70
  style.fill: "#ffebee"
}

obj -> cls
obj -> arr
```

**Fig. 1.** “Subclass of `Object`” applies to classes and (as if) arrays. Not to `int`, and not to `interface I`.

An `int[]` is an object you can `synchronize` on and call `toString` on; its **components** are still primitives. `Integer.TYPE.getSuperclass()` is `null` — the `Class` that represents `int` is not a class type in the `extends Object` sense. `Runnable.class.getSuperclass()` is also `null`. `int[].class.getSuperclass()` is `Object.class`. [[What are the wrapper types for Java primitives]] is `Integer` et al.; [[What is the difference between char and String in Java]] is primitive vs `Object` subclass.

```java
public final class NotSubclassesOfObject {
    public static void main(String[] args) {
        Object boxed = Integer.valueOf(1);     // Integer extends Object
        Object array = new int[] { 1 };        // int[] is an Object
        // Object p = 1;                       // autoboxes; the int itself is not an Object
        // Object n = null;                    // null reference, not a class

        System.out.println(int[].class.getSuperclass().getName()); // java.lang.Object
        System.out.println(Integer.TYPE.getSuperclass());          // null
        System.out.println(Runnable.class.getSuperclass());        // null
        System.out.println(Object.class.getSuperclass());          // null
        System.out.println(boxed);
        System.out.println(array);
    }
}
```

**Listing 1.** `int[]` reports superclass `Object`. `int` (`Integer.TYPE`) and interfaces do not. `Object` has no superclass.

> [!warning] `int[]` is an object; `int` is not
> Interviews collapse “arrays of primitives” into “primitives.” The array is a reference; the component is a primitive. Do not answer “everything except primitives” — **interfaces** are not subclasses of `Object` either, even though you can write `Object o = (Runnable) x` when `x` is a class instance. That conversion is from the **implementing class**, not from the interface type as a subclass.

> [!tip] Interview answer
> Primitives are not subclasses of `Object`; they are not classes. Interfaces are not classes, so they are not subclasses either. Every class except `Object` is, and arrays behave as if their superclass is `Object`. `Integer` is a class; `int` is not.
