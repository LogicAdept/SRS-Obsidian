<!--
reps: 0
priority: 0
-->
#Java/Arrays #Java/Language/Primitives #SRS

# Is an array a primitive type in Java?

> [!abstract] Short answer
> **No.** An array is a **reference type** and an **object**. Primitive types are only `boolean` and the numeric types (`byte`, `short`, `int`, `long`, `char`, `float`, `double`). An array’s *elements* may be primitives (`int[]`), but the array value itself is still a reference to an array object.

## Where arrays sit in the type system

```d2
direction: down
types: "Java types" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
prim: "Primitive\nboolean, byte, short,\nint, long, char,\nfloat, double" {
  width: 260
  height: 110
  style.fill: "#e8f5e9"
}
ref: "Reference\nclass, interface,\narray, type variable" {
  width: 260
  height: 110
  style.fill: "#fff3e0"
}
obj: "Object =\nclass instance or array" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}

types -> prim
types -> ref
ref -> obj
```

**Fig. 1.** Arrays are reference types; every array is an object, never a primitive value.

A variable of array type holds a **reference** (or `null`), not a primitive bit pattern. You create the array with `new …[]` (or an array initializer). The array can be assigned to `Object`, and you can call `Object` methods on it (`equals`, `getClass`, …).

```java
int[] nums = new int[] {1, 2, 3};
Object asObject = nums;                 // legal: array is an Object
System.out.println(nums.getClass());  // class [I
System.out.println(nums instanceof Object); // true
```

**Listing 1.** Even `int[]` is an object you can widen to `Object` and reflect on.

## Primitive *component* vs primitive *array*

`int` is primitive. `int[]` is an array type whose **component type** is `int`. Reflection makes the split obvious:

```java
System.out.println(int.class.isPrimitive());   // true
System.out.println(int[].class.isPrimitive());  // false
System.out.println(int[].class.isArray());      // true
System.out.println(int[].class.getComponentType() == int.class); // true
```

**Listing 2.** `Class.isPrimitive` is true only for the eight primitives and `void`; array classes report `isArray()`.

Collections still cannot store bare `int` values — they need wrappers — which is why [[How does adding an int to an ArrayList of Integer autobox]] matters. Fixed-length primitive buffers stay on arrays; growable lists use [[What is the difference between an array and an ArrayList]].

> [!warning] “`int[]` looks primitive, so it is”
> The `int` in `int[]` names the **element** type only. The value of `nums` is a reference. `nums = null` is legal; that would be nonsense for a true primitive local like `int x`.

> [!tip] Interview answer
> **Arrays are not primitives.** Java’s primitives are only `boolean` and the numeric types; array types are reference types, and every array is an object. A primitive array such as `int[]` stores primitive components, but the array itself is still a reference you can put in an `Object` variable or call `getClass` on.
